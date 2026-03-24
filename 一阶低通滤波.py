# class LPF(object):
#     def __init__(self):
#         self.reset()
#
#     def process(self, yaw):
#         if self.yaw_hist1 is None:
#             self.yaw_hist1 = yaw
#             self.yaw_hist2 = yaw
#         ret_val = yaw / 2 + self.yaw_hist1 / 3 + self.yaw_hist2 / 4
#         self.yaw_hist1 = yaw
#         self.yaw_hist2 = self.yaw_hist1
#         return ret_val
#
#     def reset(self):
#         self.yaw_hist1 = None
#         self.yaw_hist2 = None
#
# next_yaw = LPF()
# gimbal_yaw = next_yaw.process(yaw)
#
# next.reset()


import math
x = math.acos(2.09/2.20)
y = math.atan(0.1/2.76)

print((x-y) * 2* math.pi / 180)
