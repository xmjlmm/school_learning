# 定义模型结构（必须和训练时完全一致）
def build_resnet18(num_classes=2):
    model = torchvision.models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = torch.nn.Linear(num_features, num_classes)
    return model

# 三个模型：公交标识、斑马线标识、停车标识
model_1 = build_resnet18().to(device)
model_2 = build_resnet18().to(device)
model_3 = build_resnet18().to(device)

# 加载权重
model_1.load_state_dict(torch.load('B.pth', map_location=device))
model_2.load_state_dict(torch.load('Cross.pth', map_location=device))
model_3.load_state_dict(torch.load('P.pth', map_location=device))

# 如果需要推理时不用梯度
model_1.eval()
model_2.eval()
model_3.eval()

# TRT 加载
model_trt_1 = TRTModule()
model_trt_1.load_state_dict(torch.load('road_following_model_trt_0513_1054.pth'))
#######################################
#########################################
model_1 = model_1.to(device)
model_2 = model_2.to(device)
model_3 = model_3.to(device)
# time.sleep(10)  #停3秒
########################
###################
from jetcam.csi_camera import CSICamera
camera = CSICamera(width=224, height=224, capture_fps=65)
#camera.running = True
# time.sleep(3)  #停3秒

#################
##################
PORT = 115200
HOST = '192.168.1.114'#主机ip地址
# HOST = '192.168.1.68'
# HOST = '123.56.221.105'
BUFSIZE = 1024
portname = '/dev/ttyTHS1'
nonomame = 'AICAR3:'
# testmydict = 'mydi'
lightstate = 'LIG1SA'
senddata = ['AICAR32TAILIG2:SETLIG2_5', 'AICAR32TAILIG3:SETLIG3_7']
senddata_car = ['AICAR32TAICAR1:LEDON', 'AICAR32TAICAR2:BUZON']
mydict = {}
#kalman滤波参数
X_last_time = 0
P_last_time = 1 
R = 0.01    #超参数
Q = 0   #超参数
        
#PD参数
X_last = 0.0
X_integral_err = 0
X_last = 0.0
X_err = 0 
P = 1.1    #默认值不为0才有输出
I = 0.08
D = 1.1
# 打开串口
def open_seri(portx, bps, timeout):
    ret = False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)

        # 判断是否成功打开
        if (ser.is_open):
            ret = True
    except Exception as e:
        print("open port error!", e)

    return ser, ret


# 读数据
def read_data(ser, mydict):
    # 循环接收数据（此为死循环，可用线程实现）
    while True:
        if ser.in_waiting:
            DATA = ser.read(ser.in_waiting)
            # print("\n>> receive: ", DATA, "\n>>", end ="")
            serdata = DATA.decode('utf-8') #字节流转换成字符串
            print("ser receive: ", serdata)

            # tcpclient.send(DATA)  # 发送消息
            if 'REVOF' in serdata:
                mydict['REVOF'] = 1  #设置倒车完成标志
            elif 'LIGSA_' in serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = str(data[0])
                print('LIG value is:',ligvalue)
                mydict['LIGSA'] = ligvalue
            elif 'LINEVALUE_' in  serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = int(data[0])
                print('line value is:', ligvalue)
                mydict['LINEVALUE'] = ligvalue
            elif 'BUSVALUE_' in serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = int(data[0])
                print('bus value is:', ligvalue)
                mydict['BUSVALUE'] = ligvalue
            elif 'PARKVALUE_' in serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = int(data[0])
                print('park value is:', ligvalue)
                mydict['PARKVALUE'] = ligvalue
            elif 'ZEBRAVLAUE_' in serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = int(data[0])
                print('zerba value is:', ligvalue)
                mydict['ZEBRAVLAUE'] = ligvalue
            elif 'STOPVALUE_' in serdata:
                nametype = '_([\s\S])'
                data = re.findall(nametype, serdata)
                ligvalue = int(data[0])
                print('stop value is:', ligvalue)
                mydict['STOPVALUE'] = ligvalue
            else:
                print('error ser message')

# 写数据
def write_to_seri(ser, text):
    res = ser.write(text)  # 写
    return res


# 关闭串口
def close_seri(ser):
    ser.close()

#人工智能识别的结果float转成串口接收的指令，舵机函数
def steerfun(steervalue):
    if steervalue<0:
        cmd ='SN'
        intstree = int(-steervalue * 32768)
    else:
        cmd ='SP'
        intstree = int(steervalue * 32768)
    tempstree = hex(intstree)
#     print('tempstree is ',tempstree)
    str_stree = tempstree[2:]
    ret_stree = cmd+str_stree+'T'
    return ret_stree

#人工智能识别的结果float转成串口接收的指令，油门函数
def gainfun(gainvalue):
    if gainvalue<0:
        cmd ='GN'
        intgain = int(-gainvalue * 32768)
    else:
        cmd ='GP'
        intgain = int(gainvalue * 32768)
    tempgain = hex(intgain)
    str_gain = tempgain[2:]
    ret_gain = cmd+str_gain+'T'
    return ret_gain


# def Communicationfunc(tcpclient,ser,mydict):
    
def tcpserprocess(ser, mydict):
    # global mydict
    th = threading.Thread(target=read_data, args=(ser, mydict))
    th.start()
    
    while True:
        pass
    #tcpclient.close()
    close_seri(ser)    

def preprocess_obs(camera_value,device,normalize):
    x1 = camera_value
    x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2RGB)#将输入的图片从BGR转化为RGB值，
    x1 = x1.transpose((2, 0, 1))#BGR转化为RGB后，三维空间内的矩阵也需要更改，原本为0,1,2，转化为2,0,1
    x1 = torch.from_numpy(x1).float()#转化像素值的格式，将numpy类型转化为tensor类型
    x1 = normalize(x1)#x数据的归一化操作
    x1 = x1.to(device)
    x1 = x1[None, ...]#增加矩阵维度
    return x1

def obstacle_identify(image,model):
    y1 = model(image)
    y1 = F.softmax(y1, dim=1)
    prob_blocked = float(y1.flatten()[0])
    return prob_blocked

def line_identify(image,model):
    output_1 = model(image).detach().cpu().numpy().flatten()  # 从这个地方开始更改巡线问题，
    linevalue = float(output_1[0])
    return linevalue

def kalman(X):
    global X_last_time, P_last_time
    #Predict
    X_now_time = X
    X_now_predicted = X_last_time
    P_now_predicted = P_last_time + Q

    #Update
    K = P_now_predicted / (P_now_predicted + R)
    X_now_time = X_last_time + K * ( X_now_time - X_now_predicted)
    P_now_time = ( 1 - K ) * P_last_time

    X_last_time = X_now_time
    P_last_time = P_now_time
    return X_now_time

def PID_control(X):   #离散PID
    global X_last, X_integral_err
                        # X是PID控制器中的误差量
    X_now_err = X - X_last    #微分量 注意减的顺序--大于零时舵机应该向右打
    X_integral_err = X_integral_err + X_now_err    #离散PID积分 
    if(X_integral_err > 1): #积分限幅
        X_integral_err = 1
    if(X_integral_err < -1):
        X_integral_err = -1
    X_now = P * X + I * X_integral_err + D *X_now_err
    X_last = X       #保留这次的X的值  方便下次求误差
    if(X_now>1):  #结果限幅
        X_now = 1
    if(X_now<-1):
        X_now = -1
    return X_now
#################
################
# #     import multiprocessing
# #     from socket import *
# #     import threading
# #     import serial
# #     import time
# #     import re
# #     import numpy as np
# #     from utils import preprocess
# #     import torch.nn.functional as F
# #     import torch
# #     import torchvision
    
#     #tcpclient = socket(AF_INET, SOCK_STREAM)
#     #tcpclient.connect((HOST, PORT))
#     ser, ret = open_seri(portname, 115200, None)
#     with multiprocessing.Manager() as MG:
#         mydict = MG.dict()

#         mydict['LIGSA'] = '3' #初始状态设置为绿灯 1：红 2：黄 3：绿
#         mydict['REVOF'] = 0  #设置倒车状态 0：未完成倒车 1：完成倒车

#         p1 = multiprocessing.Process(target=tcpserprocess, args=(ser, mydict))
#         p1.start()

#         runstate = 1 #主进程运行的3种状态
#         runflag =1  #是否运行识别模型
#         runcount = 0 #运行次数统计
#         runendcount =15 #结束运行统计
        
# #         #kalman滤波参数
# #         X_last_time = 0
# #         P_last_time = 1 
# #         R = 0.01    #超参数
# #         Q = 0   #超参数
        
# #         #PD参数
# #         X_integral_err = 0
# #         X_last = 0.0
# #         X_err = 0 
# #         P = 1.1    #默认值不为0才有输出
# #         I = 0.08
# #         D = 1.1
        
#         gainvalue = 1.5  #油门调整
#         STEERING_BIAS =0.0
        
#         #图像预处理参数初始化
#         mean = 255.0 * np.array([0.485, 0.456, 0.406])
#         stdev = 255.0 * np.array([0.229, 0.224, 0.225])
#         normalize = torchvision.transforms.Normalize(mean, stdev)

#         #车的初始化参数
#         STEERING_GAIN = 1
#         #car.throttle_gain = 0.2
#         #car.throttle = 0.51
#         strgain = gainfun(gainvalue)
#         write_to_seri(ser, strgain.encode('utf-8')) # 设置初始油门为0.4

#         while True:
#             print('running')
#             #################学生编程区间###############
#             #Task2 获取实时图片，注意保存一个副本，转换成物体识别的预处理图片
#             image = camera.read()
#             image_obs = camera.value.copy()
#             image_preproc = preprocess_obs(image_obs,device,normalize)
            
#             if (1==runstate): #公交和红绿灯线路 识别线，公交站和斑马线
#                 print('runstate is : ',runstate)
#                 if(0 == runflag):
#                     runcount = runcount+1
#                     if(runcount>runendcount):
#                         runflag = 1
#                         runcount =0 #清标志位
#                         print('count end,contiue identify bus')
#                 busvalue = obstacle_identify(image_preproc,model_1)  # 人工智能识别结果
#                 #print('busvlue',busvalue)
#                 if(busvalue > 0.94) and (1==runflag) : #识别公交车站成功
#                     runstate =1  #继续公交线路，直到识别停车场
#                     runflag =0  #停止识别，等待计数
#                     #car.throttle = 0
#                     strgain = gainfun(0)
#                     write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0
#                     print('send ser stop')
#                     count = write_to_seri(ser,'BUSON'.encode('utf-8'))
#                     print('send ser find bus')
#                     time.sleep(3)  #停3秒
#                     #car.throttle = 0.51
#                     strgain = gainfun(gainvalue)
#                     write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0.4
#                     print('send ser continue run')
#                     write_to_seri(ser, 'BUSOF'.encode('utf-8'))
#                     print('send ser bus go')
#                 else:
#                     zebravalue = obstacle_identify(image_preproc,model_2)  # 人工智能识别结果
#                     if(zebravalue > 0.9):
#                         print('find zebra')
#                         ligvalue = mydict['LIGSA']
#                         if '3' == ligvalue:
#                             #car.throttle = 0.51
#                             strgain = gainfun(gainvalue)
#                             write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0.4
#                             print('green,send ser can run')
#                             count = write_to_seri(ser,'ZEBON'.encode('utf-8'))
#                             print('send ser find zebra')
#                             runstate = 2  # 红绿灯线路结束，进入停车场线路
#                         else:
#                             #car.throttle = 0
#                             strgain = gainfun(0)
#                             write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0
#                             print('send ser stop，wait green light')
#                             count = write_to_seri(ser,'ZEBON'.encode('utf-8'))
#                             print('send ser find zebra')

#                     else:
#                         image_line = preprocess(image).half()
#                         linevalue = line_identify(image_line,model_trt_1)  # 人工智能识别结果
# #                         if linevalue > 0.5:
# #                             linevalue = 0.8
# #                         linevalue = kalman(linevalue)
#                         linevalue = PID_control(linevalue)
#                         strline = steerfun(linevalue+STEERING_BIAS)
#                         write_to_seri(ser, strline.encode('utf-8'))
#                         print('send ser stree value',linevalue)
#                         #car.steering = linevalue * STEERING_GAIN + STEERING_BIAS

#             elif(2==runstate):#停车场线路 识白线，停车场
#                 print('runstate is : ', runstate)
#                 parkvalue = obstacle_identify(image_preproc,model_3)  # 人工智能识别结果
#                 if(parkvalue >0.99):
#                     #runstate = 1 #识别到停车场，进入等待倒车结束
#                     #car.throttle = 0
#                     strgain = gainfun(0)
#                     write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0
#                     print('send ser stop')
#                     count = write_to_seri(ser,'PAKON'.encode('utf-8'))
#                     print('send ser find park')
#                     time.sleep(3)  #停3秒
#                     runstate = 1 #识别到停车场，进入等待倒车结束
#                     strgain = gainfun(gainvalue)
#                     write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0.4
#                     #count = write_to_seri(ser, 'REVON'.encode('utf-8'))
#                     #print('send ser reversing begin')
#                 else:
#                     image_line = preprocess(image).half()
#                     linevalue = line_identify(image_line, model_trt_1)
# #                     if linevalue > 0.5:
# #                         linevalue = 0.8

# #                     linevalue = kalman(linevalue)
#                     linevalue = PID_control(linevalue)
#                     strline = steerfun(linevalue + STEERING_BIAS)
#                     write_to_seri(ser, strline.encode('utf-8'))
#                     print('send ser stree value', linevalue)
#                     # 设置偏转
#                     #car.steering = linevalue * STEERING_GAIN + STEERING_BIAS
#             elif(3==runstate):#等待倒车结束
#                 print('runstate is : ', runstate)
#                 revalue = mydict['REVOF']
#                 if revalue>0:
#                     runstate =1  #倒车结束，进入公交车站红绿灯线路
#                     mydict['REVOF'] =0 #清倒车结束标志
#                     print('reversing over')
#                     strgain = gainfun(gainvalue)
#                     write_to_seri(ser, strgain.encode('utf-8')) # 设置油门为0.4
#                     #car.throttle = 0.51
#                 print('wait reversing')
#             else:
#                 print('error runstate')
                
                
                
                
                
                
                
                
#     import multiprocessing
#     from socket import *
#     import threading
#     import serial
#     import time
#     import re
#     import numpy as np
#     from utils import preprocess
#     import torch.nn.functional as F
#     import torch
#     import torchvision
    
    #tcpclient = socket(AF_INET, SOCK_STREAM)
    #tcpclient.connect((HOST, PORT))
    ser, ret = open_seri(portname, 115200, None)
    with multiprocessing.Manager() as MG:
        mydict = MG.dict()

        mydict['LIGSA'] = '3' #初始状态设置为绿灯 1：红 2：黄 3：绿
        mydict['REVOF'] = 0  #设置倒车状态 0：未完成倒车 1：完成倒车

        p1 = multiprocessing.Process(target=tcpserprocess, args=(ser, mydict))
        p1.start()

        runstate = 1 #主进程运行的3种状态
        runflag =1  #是否运行识别模型
        runcount = 0 #运行次数统计
        runendcount =15 #结束运行统计
        
#         #kalman滤波参数
#         X_last_time = 0
#         P_last_time = 1 
#         R = 0.01    #超参数
#         Q = 0   #超参数
        
#         #PD参数
#         X_integral_err = 0
#         X_last = 0.0
#         X_err = 0 
#         P = 1.1    #默认值不为0才有输出
#         I = 0.08
#         D = 1.1
        
        gainvalue = 1.5  #油门调整
        STEERING_BIAS =0.0
        
        #图像预处理参数初始化
        mean = 255.0 * np.array([0.485, 0.456, 0.406])
        stdev = 255.0 * np.array([0.229, 0.224, 0.225])
        normalize = torchvision.transforms.Normalize(mean, stdev)

        #车的初始化参数
        STEERING_GAIN = 1
        #car.throttle_gain = 0.2
        #car.throttle = 0.51
        strgain = gainfun(gainvalue)
        write_to_seri(ser, strgain.encode('utf-8')) # 设置初始油门为0.4

        # 添加一个标志位来防止识别到停车场后再识别公交站
        park_detected = False

        while True:
            print('running')

            # Task2 获取实时图片，注意保存一个副本，转换成物体识别的预处理图片
            image = camera.read()
            image_obs = camera.value.copy()
            image_preproc = preprocess_obs(image_obs, device, normalize)

            if (1 == runstate):  # 公交和红绿灯线路 识别线，公交站和斑马线
                print('runstate is : ', runstate)
                if (0 == runflag):
                    runcount = runcount + 1
                    if (runcount > runendcount):
                        runflag = 1
                        runcount = 0  # 清标志位
                        print('count end, continue identify bus')
                busvalue = obstacle_identify(image_preproc, model_1)  # 人工智能识别结果
                if (busvalue > 0.6) and (1 == runflag):  # 识别公交车站成功
                    runstate = 1  # 继续公交线路，直到识别停车场
                    runflag = 0  # 停止识别，等待计数
                    # 停车
                    strgain = gainfun(0)
                    write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0
                    print('send ser stop')
                    # 播报找到公交车站
                    count = write_to_seri(ser, 'BUSON'.encode('utf-8'))
                    print('send ser find bus')
                    time.sleep(3)  # 停3秒
                    # 继续行驶
                    strgain = gainfun(gainvalue)
                    write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0.4
                    print('send ser continue run')
                    write_to_seri(ser, 'BUSOF'.encode('utf-8'))
                    print('send ser bus go')
                else:
                    zebravalue = obstacle_identify(image_preproc, model_2)  # 人工智能识别结果
                    if (zebravalue > 0.6):
                        print('find zebra')
                        ligvalue = mydict['LIGSA']
                        if '3' == ligvalue:
                            # 播报找到斑马线
                            count = write_to_seri(ser, 'ZEBON'.encode('utf-8'))
                            print('send ser find zebra')
                            # 停车
                            strgain = gainfun(0)
                            write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0
                            print('send ser stop')
                            time.sleep(3)  # 停3秒
                            # 继续行驶
                            strgain = gainfun(gainvalue)
                            write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0.4
                            print('green, send ser can run')
                            runstate = 2  # 红绿灯线路结束，进入停车场线路
                        else:
                            # 停车等待绿灯
                            strgain = gainfun(0)
                            write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0
                            print('send ser stop, wait green light')
                            count = write_to_seri(ser, 'ZEBON'.encode('utf-8'))
                            print('send ser find zebra')

                    else:
                        image_line = preprocess(image).half()
                        linevalue = line_identify(image_line, model_trt_1)  # 人工智能识别结果
                        linevalue = PID_control(linevalue)
                        strline = steerfun(linevalue + STEERING_BIAS)
                        write_to_seri(ser, strline.encode('utf-8'))
                        print('send ser stree value', linevalue)

            elif (2 == runstate):  # 停车场线路 识别白线，停车场
                print('runstate is : ', runstate)
                parkvalue = obstacle_identify(image_preproc, model_3)  # 人工智能识别结果
                if (parkvalue > 0.6):  # 识别到停车场
                    # 停止汽车
                    strgain = gainfun(0)
                    write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0
                    print('send ser stop')

                    # 播报停车场找到
                    count = write_to_seri(ser, 'PAKON'.encode('utf-8'))
                    print('send ser find park')

                    # 停止3秒
                    time.sleep(3)  # 停3秒

                    # 更新状态，回到公交车线路
                    runstate = 1  # 识别到停车场，进入等待倒车结束
                    strgain = gainfun(gainvalue)
                    write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0.4

                    # 继续循环运行
                    print('Continuing after detecting parking lot...')

                else:
                    # 处理未识别到停车场的情况
                    image_line = preprocess(image).half()
                    linevalue = line_identify(image_line, model_trt_1)
                    linevalue = PID_control(linevalue)
                    strline = steerfun(linevalue + STEERING_BIAS)
                    write_to_seri(ser, strline.encode('utf-8'))
                    print('send ser stree value', linevalue)

            elif (3 == runstate):  # 等待倒车结束
                print('runstate is : ', runstate)
                revalue = mydict['REVOF']
                if revalue > 0:
                    runstate = 1  # 倒车结束，进入公交车站红绿灯线路
                    mydict['REVOF'] = 0  # 清倒车结束标志
                    print('reversing over')
                    strgain = gainfun(gainvalue)
                    write_to_seri(ser, strgain.encode('utf-8'))  # 设置油门为0.4
                print('wait reversing')
            else:
                print('error runstate')
