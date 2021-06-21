from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mainwindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import numpy as np
import cv2
import sys
import time
import math
#import RPi.GPIO as GPIO
import pygame



class MainCode(QMainWindow, mainwindow.Ui_MainWindow):
 returnSignal = pyqtSignal()
 def __init__(self,parent=None):
    QMainWindow.__init__(self)
    mainwindow.Ui_MainWindow.__init__(self)
    self.timer_camera = QTimer() #初始化定时器
    self.cap = cv2.VideoCapture() #初始化摄像头
    self.CAM_NUM = 0
    self.setupUi(self)

    self.slot_init()


 def slot_init(self):
     self.timer_camera.timeout.connect(self.show_camera)
        #信号和槽连接
     self.startButton.clicked.connect(self.slotCameraButton)

 def show_camera(self):
     #调用摄像头，根据HSV判断圣女果
     ret, self.Img = self.cap.read()
     kernel_4 = np.ones((4, 4), np.uint8)  # 4x4的卷积核
     if self.Img is not None:  # 判断图片是否读入
         HSV = cv2.cvtColor(self.Img, cv2.COLOR_BGR2HSV)  # 把 BGR 图像转换为 HSV 格式
         # 红色2
         Lower = np.array([0, 43, 46])
         Upper = np.array([10, 255, 255])
         maturity = cv2.inRange(HSV, Lower, Upper)
         erosion = cv2.erode(maturity, kernel_4, iterations=1)
         erosion = cv2.erode(erosion, kernel_4, iterations=1)
         dilation = cv2.dilate(erosion, kernel_4, iterations=1)
         dilation = cv2.dilate(dilation, kernel_4, iterations=1)
         ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
         contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
         maxArea = 0
         maxContour = contours
         for i in contours:  # 遍历所有的轮廓
             area = cv2.contourArea(i);
             if area > maxArea:
                 maxArea = area
                 maxContour = i + 1
             x, y, w, h = cv2.boundingRect(maxContour)  # 将轮廓分解为识别对象的左上角坐标和宽、高
             cv2.rectangle(self.Img, (x, y), (x + w, y + h), (0, 255, 255), 3)
             font = cv2.FONT_HERSHEY_DUPLEX
             cv2.putText(self.Img, "Red", (x, y), font, 1.0, (0, 0, 255), 0)

             # 绘制矩形
             #cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
             # pt1：左上角坐标， pt2：右下角坐标
             # color：线条颜色，如 (255, 0, 255) 蓝色，BGR
             # thickness：线条宽度（int）

             # 添加文本
             #cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
             # text：要绘制的文字， org：文字在图像中的左下角坐标
             # fontFace：字体， fontScale：字体大小，该值和基础大小相乘得到字体大小
             # color：文字颜色， thickness：字体线条宽度
             # bottomLeftOrigin：为 true，图像数据原点在左下角；否则，图像数据原点在左上角


         show = cv2.resize(self.Img, (700, 700))

         show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
         showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
         self.vidoewidget.setPixmap(QPixmap.fromImage(showImage))

    #仅实现摄像头调用
    # flag,self.image = self.cap.read()
    # show = cv2.resize(self.image,(700,700))
    # show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
    # showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
    # self.vidoewidget.setPixmap(QPixmap.fromImage(showImage))

 #打开关闭摄像头控制
 def slotCameraButton(self):
    if self.timer_camera.isActive() == False:
        #打开摄像头并显示图像信息
        self.openCamera()
    else:
        #关闭摄像头并清空显示信息
        self.closeCamera()


 #打开摄像头
 def openCamera(self):
    flag = self.cap.open(self.CAM_NUM)
    if flag == False:
        msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确')
    else:
        CamDataHandle()
        self.timer_camera.start(30)
        self.statuslabel.setText('状态：' + 'Camera is working')


    #关闭摄像头
 def closeCamera(self):
    self.timer_camera.stop()
    self.cap.release()
    self.vidoewidget.clear()
    self.statuslabel.setText('状态：' + 'Camera has closed')


"""
class Carctrl(object):

    def __init__(self):
        # 小车电机引脚定义
        self.IN1 = 18 # 左前轮20(
        self.IN2 = 23 # 左后轮21(
        self.IN3 = 24  # 右前轮19(
        self.IN4 = 25 # 右后轮26(
        self.ENA = 25 # 左电机控速PWMA 连接Raspberry16
        self.ENB = 23 # 右电机控速PWMB 连接Raspberry13

        # 设置GPIO 口为BCM 编码方式
        GPIO.setmode(GPIO.BCM)
        # 忽略警告信息
        GPIO.setwarnings(False)

        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)
        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        # 启动PWM设置占空比为100（0--100）
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    # 小车前进
    def t_up(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车后退
    def t_down(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车左转
    def t_left(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车右转
    def t_right(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)


    #小车原地左转
    # def spin_left(leftspeed, rightspeed):
    #     GPIO.output(IN1, GPIO.LOW)
    #     GPIO.output(IN2, GPIO.HIGH)
    #     GPIO.output(IN3, GPIO.HIGH)
    #     GPIO.output(IN4, GPIO.LOW)
    #     pwm_ENA.ChangeDutyCycle(leftspeed)
    #     pwm_ENB.ChangeDutyCycle(rightspeed)
    # 
    # 
    # #小车原地右转
    # def spin_right(leftspeed, rightspeed):
    #     GPIO.output(IN1, GPIO.HIGH)
    #     GPIO.output(IN2, GPIO.LOW)
    #     GPIO.output(IN3, GPIO.LOW)
    #     GPIO.output(IN4, GPIO.HIGH)
    #     pwm_ENA.ChangeDutyCycle(leftspeed)
    #     pwm_ENB.ChangeDutyCycle(rightspeed)


    # 小车停止
    def t_stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(0)
        self.pwm_ENB.ChangeDutyCycle(0)

    #模仿手动操作的方法，将方向的控制权交给计算机：
    def self_driving(self, prediction):
        if prediction == 0:
            self.t_up(10, 10)
            print("Forward")
        elif prediction == 1:
            self.t_up(5, 10)
            print("Left")
        elif prediction == 2:
            self.t_up(10, 5)
            print("Right")
        else:
            self.t_stop(0)


#接下来读取模型，将之前训练好的xml文件加载到程序中：
class NeuralNetwork(object):

    def __init__(self):
        self.annmodel = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.annmodel.predict(samples)
        return resp.argmax(-1)  # find max
#现在模型、控制方向的方法也有了
#接下来该打开我们的摄像头，让小车看到前方的道路。
#同样，初始化神经网络和摄像头参数：
class CamDataHandle(object):

    def __init__(self):

        self.model = NeuralNetwork()
        print('load ANN model.')
        #self.obj_detection = ObjectDetection()
        self.car = Carctrl()

        print('----------------Caminit completed-----------------')
        self.handle()

    def handle(self):

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)

        #获取图像并处理：
        try:
            while True:
                ret, cam = self.cap.read()
                gray = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
                gray = cv2.resize(self.Img, (700, 700))
                ret, th3 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                roi = th3[120:240, :]

                image_array = roi.reshape(1, 38400).astype(np.float32)
                prediction = self.model.predict(image_array)
                # cv2.imshow('roi',roi)
                #cv2.imshow('cam', cam)               
                showImage = QImage(gary.data, gray.shape[1],gray.shape[0],QImage.Format_RGB888)
                self.vidoewidget.setPixmap(QPixmap.fromImage(showImage))


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                else:
                    self.car.self_driving(prediction)

        finally:
            cv2.destroyAllWindows()
            print('Shut down')

"""



if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()
    md.show()
    sys.exit(app.exec_())
