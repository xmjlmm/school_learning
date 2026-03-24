import os
from collections import OrderedDict, deque

import message_filters
import rclpy
from bboxes_ex_msgs.msg import BoundingPolygonBox2D, BoundingPolygonBoxes2D
from game_msgs.msg import GameStatus, RobotHP
from geometry_msgs.msg import Point32
from rcl_interfaces.msg import (FloatingPointRange, IntegerRange,
                                ParameterDescriptor, SetParametersResult)
from rclpy.node import Node
from rmctrl_msgs.msg import Chassis, Gimbal, Shooter
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, Float32, Int8
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from visualization_msgs.msg import Marker
from bubble_aiming.aimingProcess import *
from auto_aim_interfaces.msg import Target, TargetRune
from rclpy.qos import qos_profile_sensor_data
import math
import time

class DPNode(Node):
    def __init__(self):
        super().__init__("autoaiming")
        # init param
        self.init_protocol_param()
        self.init_debug_params()
        if (os.getenv('ROS_DISTRO') == "dashing") or (os.getenv('ROS_DISTRO') == "eloquent"):
            self.set_parameters_callback(self.parameters_callback)
        else:
            self.add_on_set_parameters_callback(self.parameters_callback)

        # robot state subscriber
        self.gimbal_sub = self.create_subscription(
            Gimbal, '/status/gimbal', self.gimbal_callback, 10)
        self.game_status_sub = self.create_subscription(
            GameStatus, '/status/game', self.game_status_callback, 10)
        self.hp_sub = self.create_subscription(
            RobotHP, '/status/robotHP', self.hp_callback, 10)
        self.bullet_sub = self.create_subscription(
            Shooter, '/status/barrel', self.bullet_vel_callback, 10)
        self.chassis_sub = self.create_subscription(
            Chassis, '/status/chassis', self.chassis_callback, 10)

        # armour subscriber
        if self.use_synchronize:
            # sync gimbal and armour masseges
            gimbal_sub = message_filters.Subscriber(
                self, Gimbal, "/status/gimbal")
            armour_sub = message_filters.Subscriber(
                self, BoundingPolygonBoxes2D, "/cv/armour")
            ts = message_filters.ApproximateTimeSynchronizer(
                [armour_sub, gimbal_sub], 10, 0.1)
            ts.registerCallback(self.synchronizeData)
        else:
            # use armour massege directly
            self.EKFtarget_sub = self.create_subscription(
                Target, '/tracker/target', self.EKFtarget_callback, qos_profile_sensor_data)
            self.newRune_sub = self.create_subscription(
                TargetRune, '/predict/targetRune', self.newRuneTarget_callback, qos_profile_sensor_data)

        # rune subscriber
        self.rune_sub = self.create_subscription(
            BoundingPolygonBoxes2D, '/cv/rune', self.rune_callback, 1)

        # init publisher
        self.rune_gimbal_pub = self.create_publisher(
            Gimbal, '/decision/gimbal_api', 10)

        self.pred_armour_pub = self.create_publisher(
            BoundingPolygonBoxes2D, '/debug/predict', 10)
        self.arg_pub = self.create_publisher(Float32, '/debug/arg', 10)
        # fps = 100
        # self.create_timer(1/fps, self.pub_timer) # lock frame number to fps
        self.gimbal_pub = self.create_publisher(
            Gimbal, '/core/gimbal_api', 10)
        self.shooter_pub = self.create_publisher(
            Shooter, '/core/shooter_api', 1)
        self.mode_pub = self.create_publisher(
            Int8, '/core/mode_api', 10)
        # robot state setting
        self.gimbal_info = GimbalInfo()
        self.bullet_vel = 27.2
        self.image_weight = 1280
        self.image_hight = 1024

        self.armourProcess = ArmourProcess(
            self, self.gimbal_info, self.bullet_vel, self.image_weight, self.image_hight)
        self.runeProcess = RuneProcess(
            self, self.gimbal_info, self.bullet_vel, self.image_weight, self.image_hight)
        self.runePrevious = []

        # tf trasform
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.last_target_list = []

        self._joint_state_pub_ = self.create_publisher(
            JointState, "/joint_states", rclpy.qos.QoSProfile(depth=1))
        self.marker_pub_ = self.create_publisher(
            Marker, "/aiming_point", 10)

        self.aiming_point_ = Marker()
        self.aiming_point_.header.frame_id = "odom"
        self.aiming_point_.ns = "aiming_point"
        self.aiming_point_.type = Marker.SPHERE
        self.aiming_point_.action = Marker.ADD
        self.aiming_point_.scale.x = self.aiming_point_.scale.y = self.aiming_point_.scale.z = 0.12
        self.aiming_point_.color.r = 1.0
        self.aiming_point_.color.g = 1.0
        self.aiming_point_.color.b = 1.0
        self.aiming_point_.color.a = 1.0
        self.aiming_point_.lifetime = rclpy.duration.Duration(
            seconds=0.1).to_msg()

        self.mode = 0

        self.g = 9.78
        # self.x_static=0.01
        # self.z_static=-0.01
        # self.k  = 0.01

        self.notShootCount = 0

        self.create_timer(1.0, self.publish_test_gimbal_data)


# 时间戳

    def getShootingThreshold(self, package):
        if package.armors_num == 2:
            e = 0.225 / 2
        elif package.armors_num == 4 or package.armors_num == 3:
            if package.id == "1":
                e = 0.225 / 2
            else:
                e = 0.135 / 2
        else:
            raise Exception("Unknown armour type,armors_num->{},id->{}".format(package.armors_num, package.id))
        Xa = package.Xc - package.r1 * math.cos(package.yaw)
        Ya = package.Yc - package.r1 * math.sin(package.yaw)
        c = np.linalg.norm(np.array([Xa, Ya]))
        a = np.linalg.norm(np.array([package.Xc, package.Yc]))
        b = np.linalg.norm(np.array([package.Xc, package.Yc]) - np.array([Xa, Ya]))
        theta = math.acos((a * a + b * b - c * c) / (2 * a * b))
        beta = math.asin(b * math.sin(theta) / c)

        phi_1 = math.pi / 2 - beta - theta
        d = math.sqrt(c * c + e * e - 2 * c * e * math.cos(phi_1))
        psai_1 = math.asin(e * sin(phi_1) / d)

        phi_2 = math.pi - phi_1
        f = math.sqrt(c * c + e * e - 2 * c * e * math.cos(phi_2))
        psai_2 = math.asin(e * sin(phi_1) / f)

        return [psai_1 + psai_2, theta]

    def GimbalControlBulletModel(self, x, v, angle):

        t = (math.exp(self.k * x) - 1) / (self.k * v * math.cos(angle))
        C = math.atan(math.sqrt(self.k / self.g) * math.sin(angle) * v) / math.sqrt(self.k * self.g)
        y_max = math.log(1 + (self.k / self.g) * math.pow(math.sin(angle) * v, 2)) / (2 * self.k)
        if C > t and angle >= 0:
            y = (1 / self.k) * math.log(
                math.cos(math.sqrt(self.k * self.g) * (C - t)) / math.cos(math.sqrt(self.k * self.g) * C))
        elif angle < 0:
            y = (1 / self.k) * math.log(
                math.cos(math.sqrt(self.k * self.g) * (C - t)) / math.cos(math.sqrt(self.k * self.g) * C))
        else:
            y = (math.log(math.tanh(math.sqrt(self.g * self.k) * (t - C)) + 1)) / (
                self.k) - math.sqrt(self.g / self.k) * (t - C) + y_max
        return y

    def GimbalControlGetPitch(self, x, y, v):
        # print(x, y, v)
        y_temp = y
        direct_pitch = math.atan2(y_temp, x)
        for i in range(20):
            angle_pitch = math.atan2(y_temp, x)
            try:
                y_actual = self.GimbalControlBulletModel(x, v, angle_pitch)
            except:
                print("math error", x, v, angle_pitch)
                angle_pitch = direct_pitch
                break

            dy = 0.61 * (y - y_actual)
            # print("dy:", dy, "\ty:", y, "\ty_actual", y_actual)
            y_temp = y_temp + dy
            if abs(dy) < 0.003:
                break
        # print(direct_pitch,"\t",angle_pitch,"\t",dy)
        return angle_pitch

    def autochange(self, package, pi, limittheta):
        Xa = package.Xc - package.r1 * math.cos(package.yaw)
        Ya = package.Yc - package.r1 * math.sin(package.yaw)
        c = np.linalg.norm(np.array([Xa, Ya]))
        a = np.linalg.norm(np.array([package.Xc, package.Yc]))
        b = np.linalg.norm(np.array([package.Xc, package.Yc]) - np.array([Xa, Ya]))

        theta = math.acos((a * a + b * b - c * c) / (2 * a * b))

        judgeValue = ((math.atan2(Ya, Xa)) - (math.atan2(package.Yc, package.Xc)))
        # Vyaw为负时顺时针，顺时针时前半圈judgeValue为负，后为正
        if package.Vyaw > 0 and judgeValue <= 0 and theta < limittheta:
            # print("unchange",theta,(math.atan2(Ya ,Xa)),(math.atan2(package.Yc ,package.Xc)),((math.atan2(Ya ,Xa))-(math.atan2(package.Yc ,package.Xc))))
            return package.r1, package.Za, package.yaw
        elif package.Vyaw < 0 and judgeValue >= 0 and theta < limittheta:
            # print("unchange",theta,(math.atan2(Ya ,Xa)),(math.atan2(package.Yc ,package.Xc)))
            return package.r1, package.Za, package.yaw
        else:
            # print("change",theta,(math.atan2(Ya ,Xa)),(math.atan2(package.Yc ,package.Xc)),((math.atan2(Ya, Xa))-(math.atan2(package.Yc, package.Xc))))
            # print("change",theta,(math.atan2(Ya ,Xa)),(math.atan2(package.Yc ,package.Xc)),((math.atan2(Ya ,Xa))-(math.atan2(package.Yc ,package.Xc))))
            return package.r2, package.Za + package.dz, package.yaw + pi

        # time.sleep(100)

    def predict(self, package, latency):
        # echelons控制自动瞄准系统的不同阶段或模式
        if self.echelons == 2:
            if self.bullet_vel > 20:
                self.k = self.k1
            else:
                self.k = self.k2
        elif self.echelons == 1:
            if self.bullet_vel > 13:
                self.k = self.k1
            else:
                self.k = self.k2

        X = math.sqrt(package.Xc * package.Xc + package.Yc * package.Yc) - self.x_static
        latency = latency + (math.exp(self.k * X) - 1) / (
                    self.k * self.bullet_vel * math.cos(math.atan2(package.Za, X)))

        package.Xc = package.Xc + package.VXc * latency
        package.Yc = package.Yc + package.VYc * latency
        package.Za = package.Za + package.VZ * latency
        package.yaw = package.yaw + package.Vyaw * latency

        if (package.Vyaw < -0.5 and abs(package.Vyaw) < 5.0):
            if package.armors_num == 4:
                package.r1, package.Za, package.yaw = self.autochange(package, math.pi / 2, 0.785399)
            elif package.armors_num == 2:
                package.r1, package.Za, package.yaw = self.autochange(package, math.pi, 0.785399)
            elif package.armors_num == 3:
                package.r2, package.Za, package.yaw = self.autochange(package, math.pi * 2 / 3, 0.785399)
                package.r1 = 0.2765
            # print(package.Vyaw,package.yaw,"clockwise_rotation")
        elif (package.Vyaw > 0.5 and abs(package.Vyaw) < 5.0):
            # elif( True):
            if package.armors_num == 4:
                package.r1, package.Za, package.yaw = self.autochange(package, -math.pi / 2, 0.785399)
            elif package.armors_num == 2:
                package.r1, package.Za, package.yaw = self.autochange(package, -math.pi, 0.785399)
            elif package.armors_num == 3:
                package.r2, package.Za, package.yaw = self.autochange(package, -math.pi * 2 / 3, 0.785399)
                package.r1 = 0.2765
        elif (package.Vyaw < -5.0):
            if package.armors_num == 4:
                package.r1, package.Za, package.yaw = self.autochange(package, math.pi / 2, 0.785399)
            elif package.armors_num == 2:
                package.r1, package.Za, package.yaw = self.autochange(package, math.pi, 0.785399)
            elif package.armors_num == 3:
                package.r2, package.Za, package.yaw = self.autochange(package, math.pi * 2 / 3, 0.785399)
                package.r1 = 0.2765
            self.echelons = 3
        elif (package.Vyaw > 5.0):
            if package.armors_num == 4:
                package.r1, package.Za, package.yaw = self.autochange(package, -math.pi / 2, 0.785399)
            elif package.armors_num == 2:
                package.r1, package.Za, package.yaw = self.autochange(package, -math.pi, 0.785399)
            elif package.armors_num == 3:
                package.r2, package.Za, package.yaw = self.autochange(package, -math.pi * 2 / 3, 0.785399)
                package.r1 = 0.2765
            self.echelons = 3
            # print(package.Vyaw,package.yaw,"clockwise_rotation")

        Xc_hat = package.Xc
        Yc_hat = package.Yc
        Za_hat = package.Za
        yaw_hat = package.yaw

        Xa_hat = Xc_hat - package.r1 * math.cos(yaw_hat)
        Ya_hat = Yc_hat - package.r1 * math.sin(yaw_hat)
        # print(latency,np.linalg.norm(np.array([Xa_hat,Ya_hat,package.Za]))/self.bullet_vel)
        if self.echelons == 3:
            target = ArmourInfo()

            Xa_hat = Xc_hat - package.r1 * math.cos(yaw_hat)
            Ya_hat = Yc_hat - package.r1 * math.sin(yaw_hat)

            target.yaw_angle = (math.atan2(Yc_hat, Xc_hat))

            Xa_hat_cross_center = Xc_hat - package.r1 * math.cos(target.yaw_angle)

            Ya_hat_cross_center = Yc_hat - package.r1 * math.sin(target.yaw_angle)

            # print(np.linalg.norm(np.array([Xc_hat,Yc_hat])-np.array([Xa_hat_cross_center,Ya_hat_cross_center])))
            target.yaw_angle = (math.atan2(Ya_hat_cross_center, Xa_hat_cross_center))

            target.armor_yaw_for_hero = (math.atan2(Ya_hat, Xa_hat))
            # print(self.k)
            target.pitch_angle = -self.GimbalControlGetPitch(math.sqrt(
                Xa_hat_cross_center * Xa_hat_cross_center + Ya_hat_cross_center * Ya_hat_cross_center) - self.x_static
                                                             , Za_hat + self.z_static
                                                             , self.bullet_vel)
            if abs(target.yaw_angle - target.armor_yaw_for_hero) < (self.getShootingThreshold(package)[0]):
                self.aiming_point_.header.stamp = self.get_clock().now().to_msg()
                self.aiming_point_.pose.position.x = Xa_hat_cross_center
                self.aiming_point_.pose.position.y = Ya_hat_cross_center
                self.aiming_point_.pose.position.z = Za_hat
                self.marker_pub_.publish(self.aiming_point_)
        elif self.echelons == 2:
            target = ArmourInfo()
            target.yaw_angle = (math.atan2(Ya_hat, Xa_hat))
            # print(self.k)
            target.pitch_angle = -self.GimbalControlGetPitch(
                math.sqrt(Xa_hat * Xa_hat + Ya_hat * Ya_hat) - self.x_static
                , Za_hat + self.z_static
                , self.bullet_vel)  # target.yaw_angle = 0
            if abs(Xc_hat) > 0.01:
                self.aiming_point_.header.stamp = self.get_clock().now().to_msg()
                self.aiming_point_.pose.position.x = Xa_hat
                self.aiming_point_.pose.position.y = Ya_hat
                self.aiming_point_.pose.position.z = Za_hat
                self.marker_pub_.publish(self.aiming_point_)

        return target

    def newRuneTarget_callback(self, target_msg):
        # print(666666666)
        target = ArmourInfo()
        target.yaw_angle = (math.atan2(target_msg.position.y, target_msg.position.x))
        target.pitch_angle = math.atan2(target_msg.position.z + 0.7, math.sqrt(
            target_msg.position.y * target_msg.position.y + target_msg.position.x * target_msg.position.x) - self.x_static)
        target.roll_angle = 0
        self.pub_gimbal_data(target, rune_mode=True)

    def EKFtarget_callback(self, target_msg):
        # print(target_msg.tracking)
        # print(self.shootcount)
        if target_msg.tracking:
            self.mode = 1

            mode_msg = Int8()
            mode_msg.data = 1
            self.mode_pub.publish(mode_msg)

            package = StatusInfo()
            package.Xc = target_msg.position.x
            package.Yc = target_msg.position.y
            package.Za = target_msg.position.z
            package.yaw = target_msg.yaw
            package.VXc = target_msg.velocity.x
            package.VYc = target_msg.velocity.y
            package.VZ = target_msg.velocity.z
            package.Vyaw = target_msg.v_yaw
            package.r1 = target_msg.radius_1
            package.r2 = target_msg.radius_2
            package.dz = target_msg.dz
            package.armors_num = target_msg.armors_num
            package.id = target_msg.id

            target = self.predict(package, self.latencyTime)
            self.pub_gimbal_data(target, package=package)
        elif self.mode:

            mode_msg = Int8()
            mode_msg.data = 0
            self.mode_pub.publish(mode_msg)
            # print(66666666666666666666666666)
            self.mode = 0
            gimbal_msg = Gimbal()
            gimbal_msg.mode = self.mode
            self.gimbal_pub.publish(gimbal_msg)

            shooter_msg = Shooter()
            shooter_msg.is_shoot = False
            self.shooter_pub.publish(shooter_msg)

    def synchronizeData(self, armour_msg, gimbal_msg):
        self.gimbal_callback(gimbal_msg)
        self.rune_callback(armour_msg)
        self.process()

    # def armour_callback(self, armour_msg):
    #     armour_list, strip_list = self.parse_armour(armour_msg)
    #     if not armour_list:
    #         return
    #     armour = self.armourProcess.process(armour_list, strip_list)

    #     # publish gimbal control data
    #     if not self.use_regular_send:
    #         self.last_target_list.append(armour)
    #     else:
    #         self.pub_gimbal_data(armour)

    #     # for debug
    #     if self.debug_mode:
    #         # publish predict data
    #         self.pub_predict_data(armour)

    def rune_callback(self, rune_msg):
        rune_list = self.parse_rune(rune_msg)
        if not rune_list:
            return
        rune_info, pred_rect_point_info = self.runeProcess.process(rune_list)

        # 清除上一次记录的数据
        self.runePrevious.append(rune_info)
        if len(self.runePrevious) > 10:
            self.runePrevious.pop(0)
            time_1, time_2 = self.runePrevious[-10].stamp, self.runePrevious[-1].stamp
            # print(time_1, time_2)
            # 大于三秒丢失目标时，重新实例化
            if time_2 - time_1 > 3:
                self.runeProcess = RuneProcess(
                    self, self.gimbal_info, self.bullet_vel, self.image_weight, self.image_hight)
                print("clear successfully!")

        if self.use_regular_send:
            self.last_target_list.append(rune_info)
        else:
            self.pub_gimbal_data(rune_info, rune_mode=True)

        if self.debug_mode:
            self.pub_predict_data(pred_rect_point_info)

    def pub_gimbal_data(self, armour, package=None, rune_mode=False):
        assert not (package == None and rune_mode == False)
        gimbal_msg = Gimbal()
        gimbal_msg.mode = 1
        gimbal_msg.header.stamp = self.get_clock().now().to_msg()

        if rune_mode:
            # gimbal_msg.pitch = -0.3
            # print(armour.pitch_angle,self.gimbal_info.get_pitch(),gimbal_msg.pitch)
            # 相对坐标
            # print(armour.yaw_angle)

            gimbal_msg.yaw = float(armour.yaw_angle)
            gimbal_msg.pitch = -float(armour.pitch_angle)
            gimbal_msg.roll = float(armour.roll_angle)
            self.gimbal_pub.publish(gimbal_msg)
        else:
            # print("yaw:{}\tpitch:{}\tgimbalyaw:{}\tgimbalpitch:{}".format(armour.yaw_angle,armour.pitch_angle,self.gimbal_info.yaw,self.gimbal_info.pitch))
            # print(self.echelons)
            gimbal_msg.pitch = float(armour.pitch_angle)
            gimbal_msg.yaw = float(armour.yaw_angle)
            shootJudge = self.getShootingThreshold(package)
            shootingThreshold = (shootJudge[0] / 2)

            # print(abs(armour.yaw_angle - self.gimbal_info.yaw),shootingThreshold)
            if self.echelons == 2:
                if abs(armour.yaw_angle - self.gimbal_info.yaw) < shootingThreshold and shootJudge[1] < 1.047198:
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = True
                    print("shooot", time.time())
                    # self.shootcount = self.shootcount+1
                    self.shooter_pub.publish(shooter_msg)
                    self.notShootCount = 0
                elif self.notShootCount > 2:
                    print("not shoot", time.time())
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = False
                    self.shooter_pub.publish(shooter_msg)
                else:
                    self.notShootCount = self.notShootCount + 1
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = True
                    print("shooot", time.time())
                    # self.shootcount = self.shootcount+1
                    self.shooter_pub.publish(shooter_msg)
                gimbal_msg.roll = float((armour.roll_angle))
            elif self.echelons == 3:
                if abs(armour.yaw_angle - armour.armor_yaw_for_hero) < shootingThreshold and abs(
                        armour.yaw_angle - self.gimbal_info.yaw) < shootingThreshold and shootJudge[1] < 1.047198:
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = True
                    print("shooot", time.time())
                    # self.shootcount = self.shootcount+1
                    self.shooter_pub.publish(shooter_msg)
                    self.notShootCount = 0
                elif self.notShootCount > 2:
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = False
                    print("not shoot", time.time())
                    self.shooter_pub.publish(shooter_msg)
                else:
                    self.notShootCount = self.notShootCount + 1
                    shooter_msg = Shooter()
                    shooter_msg.is_shoot = True
                    print("shooot", time.time())
                    # self.shootcount = self.shootcount+1
                    self.shooter_pub.publish(shooter_msg)
                gimbal_msg.roll = float((armour.roll_angle))
                self.echelons = 2

            self.gimbal_pub.publish(gimbal_msg)



    def publish_test_gimbal_data(self):
        gimbal_msg = Gimbal()
        gimbal_msg.mode = 1
        gimbal_msg.header.stamp = self.get_clock().now().to_msg()

        gimbal_msg.yaw = math.sin(time.time())
        gimbal_msg.pitch = 0.0

        # 发布gimbal_msg到'/core/gimbal_api'
        self.gimbal_pub.publish(gimbal_msg)




    def pub_predict_data(self, armour):
        box = BoundingPolygonBox2D()
        for j in range(4):
            point = armour[j]
            pointMsg = Point32()
            pointMsg.x = float(point[0])
            pointMsg.y = float(point[1])
            box.pose.points.append(pointMsg)

        msg = BoundingPolygonBoxes2D()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.bounding_boxes = [box]
        self.pred_armour_pub.publish(msg)

    def parse_armour(self, data: BoundingPolygonBoxes2D):
        armour_list = []
        strip_list = []

        target_time_stamp = data.image_header.stamp.sec + \
                            data.image_header.stamp.nanosec * 1e-9
        for target in data.bounding_boxes:
            if target.class_id == "Armour":
                armour = ArmourInfo()
                armour.set_data(target_time_stamp,
                                target.pose.points, target.type)
                armour_list.append(armour)

            elif target.class_id == "Strip":
                # TODO add light strip parse
                pass
        return armour_list, strip_list

    def parse_rune(self, data: BoundingPolygonBoxes2D):
        temp_rune = [None, None]  # tar and center
        rune_list = []
        target_time_stamp = data.image_header.stamp.sec + \
                            data.image_header.stamp.nanosec * 1e-9
        rune = RuneInfo()

        for target in data.bounding_boxes:
            if target.class_id == "Rune":
                if target.type == "armour" and [[int(pose.x), int(pose.y)] for pose in target.pose.points] != [[0, 0],
                                                                                                               [0, 0],
                                                                                                               [0, 0],
                                                                                                               [0, 0]]:
                    for pose in target.pose.points:
                        if pose.x > 0:
                            temp_rune[0] = target.pose.points
                elif target.type == "center" and [[int(pose.x), int(pose.y)] for pose in target.pose.points] != [[0, 0],
                                                                                                                 [0, 0],
                                                                                                                 [0, 0],
                                                                                                                 [0,
                                                                                                                  0]]:
                    temp_rune[1] = target.pose.points
        if temp_rune[0] is not None and temp_rune[1] is not None:
            rune.set_data(target_time_stamp, temp_rune[0], temp_rune[1], 0, 3)
            rune_list.append(rune)

        return rune_list

    def bullet_vel_callback(self, data: Shooter):

        # print(data.bullet_vel,"-------------------------")
        # print(self.bullet_vel)
        if data.bullet_vel > 10:
            self.bullet_vel = data.bullet_vel
        # if self.echelons == 2:
        #     self.bullet_vel = data.bullet_vel
        # else:
        #     if data.bullet_vel<10 or abs(self.bullet_vel-data.bullet_vel)<3:
        #         pass
        #     else:
        #         self.bullet_vel = data.bullet_vel
        #     if self.bullet_vel == 0:
        #         self.bullet_vel = 28

    def gimbal_callback(self, data: Gimbal):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['pitch_joint', 'yaw_joint']
        joint_state.position = [data.pitch, data.yaw]
        self._joint_state_pub_.publish(joint_state)

        self.gimbal_info.set_data(
            data.header.stamp.sec + data.header.stamp.nanosec * 1e-9,
            data.yaw, data.pitch, data.roll
        )
        self.gimbal_info.set_ros_stamp(data.header.stamp)

    def chassis_callback(self, data: Chassis):
        self.game_param["chassis_info"]['chassis_target_linear_x'] = data.chassis_target_linear_x
        self.game_param["chassis_info"]['chassis_target_linear_y'] = data.chassis_target_linear_y
        self.game_param["chassis_info"]['chassis_target_linear_z'] = data.chassis_target_linear_z
        self.game_param["chassis_info"]['chassis_target_angular_x'] = data.chassis_target_angular_x
        self.game_param["chassis_info"]['chassis_target_angular_y'] = data.chassis_target_angular_y
        self.game_param["chassis_info"]['chassis_target_angular_z'] = data.chassis_target_angular_z

    def game_status_callback(self, data):
        self.game_param["game_status_info"]["game_type"] = data.game_type
        self.game_param["game_status_info"]["game_progress"] = data.game_progress
        self.game_param["game_status_info"]["stage_remain_time"] = data.stage_remain_time
        self.runeProcess.remain_time = self.game_param["game_status_info"]["stage_remain_time"]

    def hp_callback(self, data):
        self.game_param["robot_HP_info"]["red_1_robot_HP"] = data.red_1_robot_hp
        self.game_param["robot_HP_info"]["red_2_robot_HP"] = data.red_2_robot_hp
        self.game_param["robot_HP_info"]["red_3_robot_HP"] = data.red_3_robot_hp
        self.game_param["robot_HP_info"]["red_4_robot_HP"] = data.red_4_robot_hp
        self.game_param["robot_HP_info"]["red_5_robot_HP"] = data.red_5_robot_hp
        self.game_param["robot_HP_info"]["red_7_robot_HP"] = data.red_7_robot_hp
        self.game_param["robot_HP_info"]["red_outpost_HP"] = data.red_outpost_hp
        self.game_param["robot_HP_info"]["red_base_HP"] = data.red_base_hp
        self.game_param["robot_HP_info"]["blue_1_robot_HP"] = data.blue_1_robot_hp
        self.game_param["robot_HP_info"]["blue_2_robot_HP"] = data.blue_2_robot_hp
        self.game_param["robot_HP_info"]["blue_3_robot_HP"] = data.blue_3_robot_hp
        self.game_param["robot_HP_info"]["blue_4_robot_HP"] = data.blue_4_robot_hp
        self.game_param["robot_HP_info"]["blue_5_robot_HP"] = data.blue_5_robot_hp
        self.game_param["robot_HP_info"]["blue_7_robot_HP"] = data.blue_7_robot_hp
        self.game_param["robot_HP_info"]["blue_outpost_HP"] = data.blue_outpost_hp
        self.game_param["robot_HP_info"]["blue_base_HP"] = data.blue_base_hp

    def init_protocol_param(self):
        """
        Initialize the communication params
        """
        robot_HP_info = OrderedDict()
        robot_HP_info["red_1_robot_HP"] = 0
        robot_HP_info["red_2_robot_HP"] = 0
        robot_HP_info["red_3_robot_HP"] = 0
        robot_HP_info["red_4_robot_HP"] = 0
        robot_HP_info["red_5_robot_HP"] = 0
        robot_HP_info["red_7_robot_HP"] = 0
        robot_HP_info["red_outpost_HP"] = 0
        robot_HP_info["red_base_HP"] = 0
        robot_HP_info["blue_1_robot_HP"] = 0
        robot_HP_info["blue_2_robot_HP"] = 0
        robot_HP_info["blue_3_robot_HP"] = 0
        robot_HP_info["blue_4_robot_HP"] = 0
        robot_HP_info["blue_5_robot_HP"] = 0
        robot_HP_info["blue_7_robot_HP"] = 0
        robot_HP_info["blue_outpost_HP"] = 0
        robot_HP_info["blue_base_HP"] = 0

        game_status_info = OrderedDict()
        game_status_info["game_type"] = []
        game_status_info["game_progress"] = []
        game_status_info["stage_remain_time"] = []

        chassis_info = OrderedDict()
        chassis_info['chassis_target_linear_x'] = 0
        chassis_info['chassis_target_linear_y'] = 0
        chassis_info['chassis_target_linear_z'] = 0
        chassis_info['chassis_target_angular_x'] = 0
        chassis_info['chassis_target_angular_y'] = 0
        chassis_info['chassis_target_angular_z'] = 0

        self.game_param = OrderedDict()
        self.game_param["game_status_info"] = game_status_info
        self.game_param["robot_HP_info"] = robot_HP_info
        self.game_param["chassis_info"] = chassis_info

    def init_debug_params(self):
        """
        Initialize the debug params
        """

        self.declare_parameter('use_synchronize', False)
        self.use_synchronize = self.get_parameter('use_synchronize').value
        self.declare_parameter('use_regular_send', False)
        self.use_regular_send = self.get_parameter('use_regular_send').value
        self.declare_parameter('debug_mode', False)
        self.debug_mode = self.get_parameter('debug_mode').value

        # Rune parameter descriptor
        angleFloatDescriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=45.0, step=0.1)])
        timeFloatDescriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=1.0, step=0.01)])

        # Rune debug param
        self.rune_debug_info = OrderedDict()
        self.rune_debug_info["ahead_time"] = 0.0
        self.rune_debug_info["ahead_angle"] = 0.0
        self.declare_parameter('ahead_time', 0.0, timeFloatDescriptor)
        self.declare_parameter('ahead_angle', 0.0, angleFloatDescriptor)

        # Anti-gyro parameter descriptor
        gyroFloatDescriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=1.0, step=0.1)])
        gyroLowDescriptor = ParameterDescriptor(
            integer_range=[IntegerRange(from_value=0, to_value=100, step=1)])
        gyroHighDescriptor = ParameterDescriptor(
            integer_range=[IntegerRange(from_value=100, to_value=1000, step=1)])

        # Anti-gyro debug param
        self.gyro_debug_info = OrderedDict()
        self.gyro_debug_info["magnification"] = 0
        self.gyro_debug_info["moving_alter_thres"] = 0
        self.gyro_debug_info["gyro_thres"] = 0
        self.gyro_debug_info["tolerance_thres"] = 0
        self.gyro_debug_info["armour_alter_thres"] = 0
        self.gyro_debug_info["height_differ_min_thres"] = 0
        self.gyro_debug_info["height_differ_max_thres"] = 0
        self.gyro_debug_info["width_differ_min_thres"] = 0
        self.gyro_debug_info["width_alter_min_thres"] = 0
        self.gyro_debug_info["width_differ_max_thres"] = 0
        self.declare_parameter('moving_alter_thres', 0, gyroLowDescriptor)
        self.declare_parameter('gyro_thres', 0, gyroLowDescriptor)
        self.declare_parameter('tolerance_thres', 0, gyroLowDescriptor)
        self.declare_parameter('armour_alter_thres', 0, gyroLowDescriptor)
        self.declare_parameter('height_differ_min_thres', 0, gyroLowDescriptor)
        self.declare_parameter('height_differ_max_thres', 0, gyroLowDescriptor)
        self.declare_parameter('width_differ_min_thres', 0, gyroLowDescriptor)
        self.declare_parameter('width_differ_max_thres', 10, gyroHighDescriptor)
        self.declare_parameter('width_alter_min_thres', 10, gyroHighDescriptor)
        self.declare_parameter('gyro_iou_thres', 0.0, gyroFloatDescriptor)

        # Read params value from config
        self.declare_parameter('magnification', 0, descriptor=ParameterDescriptor(
            integer_range=[IntegerRange(from_value=0, to_value=10, step=1)]))
        self.gyro_debug_info["magnification"] = self.get_parameter(
            'magnification').value
        self.gyro_debug_info["moving_alter_thres"] = self.get_parameter(
            'moving_alter_thres').value
        self.gyro_debug_info["gyro_thres"] = self.get_parameter(
            'gyro_thres').value
        self.gyro_debug_info["tolerance_thres"] = self.get_parameter(
            'tolerance_thres').value
        self.gyro_debug_info["armour_alter_thres"] = self.get_parameter(
            'armour_alter_thres').value
        self.gyro_debug_info["height_differ_min_thres"] = self.get_parameter(
            'height_differ_min_thres').value
        self.gyro_debug_info["height_differ_max_thres"] = self.get_parameter(
            'height_differ_max_thres').value
        self.gyro_debug_info["width_differ_min_thres"] = self.get_parameter(
            'width_differ_min_thres').value
        self.gyro_debug_info["width_alter_min_thres"] = self.get_parameter(
            'width_alter_min_thres').value
        self.gyro_debug_info["width_differ_max_thres"] = self.get_parameter(
            'width_differ_max_thres').value
        self.gyro_debug_info["gyro_iou_thres"] = self.get_parameter(
            'gyro_iou_thres').value

        # camera offset and intrtnsic params
        self.gimbal_offset_info = OrderedDict()
        self.gimbal_offset_info["x_offset"] = 0
        self.gimbal_offset_info["y_offset"] = 0
        self.gimbal_offset_info["z_offset"] = 0

        camera_offset_descriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=-1.0, to_value=1.0, step=0.0001)])
        self.declare_parameter(
            'x_offset', 0.0, descriptor=camera_offset_descriptor)
        self.declare_parameter(
            'y_offset', 0.0, descriptor=camera_offset_descriptor)
        self.declare_parameter(
            'z_offset', 0.0, descriptor=camera_offset_descriptor)
        self.gimbal_offset_info["x_offset"] = self.get_parameter(
            'x_offset').value
        self.gimbal_offset_info["y_offset"] = self.get_parameter(
            'y_offset').value
        self.gimbal_offset_info["z_offset"] = self.get_parameter(
            'z_offset').value

        self.declare_parameter('camera_intrinsic_config_path', "")
        self.camera_intrinsic = self.get_parameter(
            'camera_intrinsic_config_path').value
        with open(self.camera_intrinsic, 'r') as f:
            self.camera_intrinsic = f.read()
        self.camera_intrinsic = eval(self.camera_intrinsic)

        self.rune_debug_info["ahead_time"] = self.get_parameter(
            'ahead_time').value
        self.rune_debug_info["ahead_angle"] = self.get_parameter(
            'ahead_angle').value

        gimbal_sense_descriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=1.0, step=0.01)])
        self.declare_parameter('yaw_sense', 0.0, descriptor=gimbal_sense_descriptor)
        self.declare_parameter('pitch_sense', 0.0, descriptor=gimbal_sense_descriptor)

        self.yaw_sense = self.get_parameter('yaw_sense').value
        self.pitch_sense = self.get_parameter('pitch_sense').value
        # alpha
        self.alphaYaw = 0.3
        alpha_descriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=-5.0, to_value=5.0, step=0.0001)])
        self.declare_parameter(
            'alphaYaw', 0.3, descriptor=alpha_descriptor)
        self.alphaYaw = self.get_parameter(
            'alphaYaw').value

        self.alphaPitch = 0.225
        self.declare_parameter(
            'alphaPitch', 0.225, descriptor=alpha_descriptor)
        self.alphaPitch = self.get_parameter(
            'alphaPitch').value

        self.alphaBPitch = 0.6
        self.declare_parameter(
            'alphaBPitch', 0.6, descriptor=alpha_descriptor)
        self.alphaBPitch = self.get_parameter(
            'alphaBPitch').value

        self.alphaBYaw = 0.55
        self.declare_parameter(
            'alphaBYaw', 0.55, descriptor=alpha_descriptor)
        self.alphaBYaw = self.get_parameter(
            'alphaBYaw').value
        # alpha
        alpha_descriptor = ParameterDescriptor(
            floating_point_range=[FloatingPointRange(from_value=-5.0, to_value=5.0, step=0.0001)])
        self.declare_parameter(
            'latencyTime', 0.0, descriptor=alpha_descriptor)
        self.latencyTime = self.get_parameter(
            'latencyTime').value
        self.declare_parameter(
            'z_static', 0.0, descriptor=alpha_descriptor)
        self.z_static = self.get_parameter(
            'z_static').value
        self.declare_parameter(
            'x_static', 0.0, descriptor=alpha_descriptor)
        self.x_static = self.get_parameter(
            'x_static').value
        self.declare_parameter(
            'k1', 0.0, descriptor=alpha_descriptor)
        self.k1 = self.get_parameter(
            'k1').value
        self.declare_parameter(
            'k2', 0.0, descriptor=alpha_descriptor)
        self.k2 = self.get_parameter(
            'k2').value
        self.declare_parameter(
            'echelons', 1)
        self.echelons = self.get_parameter(
            'echelons').value

    def parameters_callback(self, data):
        for param in data:
            if param.name == "magnification":
                self.gyro_debug_info["magnification"] = param.value
            elif param.name == "moving_alter_thres":
                self.gyro_debug_info["moving_alter_thres"] = param.value
            elif param.name == "gyro_thres":
                self.gyro_debug_info["gyro_thres"] = param.value
            elif param.name == "tolerance_thres":
                self.gyro_debug_info["tolerance_thres"] = param.value
            elif param.name == "armour_alter_thres":
                self.gyro_debug_info["armour_alter_thres"] = param.value
            elif param.name == "height_differ_min_thres":
                self.gyro_debug_info["height_differ_min_thres"] = param.value
            elif param.name == "height_differ_max_thres":
                self.gyro_debug_info["height_differ_max_thres"] = param.value
            elif param.name == "width_differ_min_thres":
                self.gyro_debug_info["width_differ_min_thres"] = param.value
            elif param.name == "width_alter_min_thres":
                self.gyro_debug_info["width_alter_min_thres"] = param.value
            elif param.name == "width_differ_max_thres":
                self.gyro_debug_info["width_differ_max_thres"] = param.value
            elif param.name == "gyro_iou_thres":
                self.gyro_debug_info["gyro_iou_thres"] = param.value
            elif param.name == "x_offset":
                self.gimbal_offset_info["x_offset"] = param.value
            elif param.name == "y_offset":
                self.gimbal_offset_info["y_offset"] = param.value
            elif param.name == "z_offset":
                self.gimbal_offset_info["z_offset"] = param.value
            elif param.name == "debug_mode":
                self.debug_mode = param.value
            elif param.name == "ahead_time":
                self.rune_debug_info["ahead_time"] = param.value
            elif param.name == "ahead_angle":
                self.rune_debug_info["ahead_angle"] = param.value
            elif param.name == "latencyTime":
                self.latencyTime = param.value
            elif param.name == "z_static":
                self.z_static = param.value
            elif param.name == "x_static":
                self.x_static = param.value
            elif param.name == "k1":
                self.k1 = param.value
            elif param.name == "k2":
                self.k2 = param.value
            elif param.name == "alphaBYaw":
                self.alphaBYaw = param.value
            elif param.name == "alphaYaw":
                self.alphaYaw = param.value
            elif param.name == "alphaPitch":
                self.alphaPitch = param.value
            elif param.name == "alphaBPitch":kkiik
                self.alphaBPitch = param.value

        return SetParametersResult(successful=True)


class LPF(object):
    def __init__(self):
        self.reset()

    def process(self, yaw):
        if (self.yaw_hist1 is None):
            self.yaw_hist1 = yaw
            self.yaw_hist2 = yaw
        ret_val = yaw / 2 + self.yaw_hist1 / 3 + self.yaw_hist2 / 6
        self.yaw_hist2 = self.yaw_hist1
        self.yaw_hist1 = yaw
        return ret_val

    def reset(self):
        self.yaw_hist1 = None
        self.yaw_hist2 = None


def main(args=None):
    rclpy.init(args=args)
    data_publisher = DPNode()
    rclpy.spin(data_publisher)
    data_publisher.destroy_node()
    rclpy.shutdown()
    # para = LPF()
    # gimbal_yaw  = para.process(yaw)


if __name__ == '__main__':
    main()


    // 抬枪补偿和预测
    float distance =
        sqrtf(temp_data.xa * temp_data.xa + temp_data.ya * temp_data.ya +
              aim_data->z * aim_data->z);
    float p_pitch = atan2(temp_data.za, temp_data.xa * temp_data.xa +
                                            temp_data.ya * temp_data.ya);
    float a = 9.8 * 9.8 * 0.25;
    float b = -robot_speed_mps_ * robot_speed_mps_ -
              distance * 9.8 * cos(M_PI_2 + p_pitch);
    float c = distance * distance;
    float t_2 = (-sqrt(b * b - 4 * a * c) - b) / (2 * a);
    float fly_time = sqrt(t_2) + aim_data->letency_time;  // 子弹飞行时间（单位:s）
    // 解出抬枪高度，即子弹下坠高度
    float height = 0.5 * 9.8 * t_2;
