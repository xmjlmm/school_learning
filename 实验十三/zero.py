import time
import os
import cv2
import numpy as np
from numpy.linalg import inv

# 进行滑动窗口处理，固定窗口大小，行间隔为50，获取左上角位置
def sliding_window(img1, img2, patch_size=(100, 302), istep=50):
    Ni, Nj = (int(s) for s in patch_size)
    for i in range(0, img1.shape[0] - Ni + 1, istep):
        patch = (img1[i:i + Ni, 39:341], img2[i:i + Ni, 39:341])
        yield (i, 39), patch

# 预测斑马线，1为斑马线，0为背景
def predict(patches, DEBUG):
    labels = np.zeros(len(patches))
    index = 0
    for Amplitude, theta in patches:
        # 过滤梯度太小的点
        mask = (Amplitude > 25).astype(np.float32)
        # 修复：将 np.bool 改为 np.bool_ 或 bool
        h, b = np.histogram(theta[mask.astype(np.bool_)], bins=range(0, 80, 5))
        low, high = b[h.argmax()], b[h.argmax() + 1]
        # 统计直方图峰值方向的点数
        newmask = ((Amplitude > 25) * (theta <= high) * (theta >= low)).astype(np.float32)
        value = ((Amplitude * newmask) > 0).sum()

        # 进行阈值设置，根据不同的场景进行调节
        if value > 1500:
            labels[index] = 1
        index += 1
        # 调试模式下，打印相关的参数
        if DEBUG:
            print(h)
            print(low, high)
            print(value)
            cv2.imshow("newAmplitude", Amplitude * newmask)
            cv2.waitKey(0)
    return labels

# 图片预处理，获取蓝色通道信息，进行中值滤波、开运算和闭运算
def preprocessing(img):
    kernell = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    gray = img[:, :, 0]  # 获取蓝色通道
    # 中值滤波
    gray = cv2.medianBlur(gray, 5)
    # 开运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernell, iterations=4)
    # 闭运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel2, iterations=3)
    return gray

# 计算x轴和y轴的导数，来计算梯度和方向
def getGD(canny):
    # 计算x轴和y轴的sobel因子
    sobelx = cv2.Sobel(canny, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(canny, cv2.CV_32F, 0, 1, ksize=3)
    # 计算梯度和方向
    theta = np.arctan(np.abs(sobely / (sobelx + 1e-10))) * 180 / np.pi
    Amplitude = np.sqrt(sobelx**2 + sobely**2)
    mask = (Amplitude > 30).astype(np.float32)
    Amplitude = Amplitude * mask
    return Amplitude, theta

# 计算斑马线的位置，如果存在斑马线，将合并所有的滑动窗口得到最终的斑马线位置
def getlocation(indices, labels, Ni, Nj):
    # 判断是否有斑马线
    zc = indices[labels == 1]
    if len(zc) == 0:
        return 0, None
    else:
        # 合并所有的滑动窗口得到最终的斑马线位置
        xmin = int(min(zc[:, 1]))
        ymin = int(min(zc[:, 0]))
        xmax = int(xmin + Nj)
        ymax = int(max(zc[:, 0]) + Ni)
        return 1, ((xmin, ymin), (xmax, ymax))

if __name__ == "__main__":
    # 调试模式开关
    DEBUG = False
    # 滑动窗口的大小
    Ni, Nj = (100, 302)
    # 获取图片一定区间的位置，计算位置
    M = np.array([[-1.86073726e-01, -5.02678929e-01, 4.72322899e+02],
                  [-1.39150388e-02, -1.50260445e+00, 1.00507430e+03],
                  [-1.77785988e-05, -1.65517173e-03, 1.00000000e+00]])

    iM = inv(M)
    xy = np.zeros((640, 640, 2), dtype=np.float32)
    for py in range(640):
        for px in range(640):
            xy[py, px] = np.array([px, py], dtype=np.float32)
    ixy = cv2.perspectiveTransform(xy, iM)
    mpx, mpy = cv2.split(ixy)
    mapx, mapy = cv2.convertMaps(mpx, mpy, cv2.CV_16SC2)

    # 导入视频
    cap = cv2.VideoCapture("F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4")
    time.sleep(1)
    NUM_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for ii in range(NUM_FRAMES):
        print("frame:", ii)
        ret, frame = cap.read()
        if not ret:
            break
        # 图片映射时，得原始图片的指定位置映射为所的图片
        img = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        img = cv2.resize(img, (400, 400))
        gray = preprocessing(img)
        
        # 计算梯度和方向
        Amplitude, theta = getGD(gray)
        
        # 生成滑动窗口并预测
        indices_patches = list(sliding_window(Amplitude, theta, patch_size=(Ni, Nj)))
        if indices_patches:
            indices, patches = zip(*indices_patches)
            labels = predict(patches, DEBUG)
            indices = np.array(indices)
            ret, location = getlocation(indices, labels, Ni, Nj)
            # 画图
            if ret:
                cv2.rectangle(img, location[0], location[1], (255, 0, 255), 3)
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()