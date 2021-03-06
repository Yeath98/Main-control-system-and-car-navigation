#三个Collect的py数据文件都是一样的，只不过在执行各功能的时候的操作按键和收集的画面数据不一样
import RPi.GPIO as GPIO
import time  
import smtplib
from time import sleep
from pip._vendor import requests
import sys
import pygame
from pygame.locals import *
import numpy as np
import cv2
import os


class CollectData(object):
    def __init__(self):
        # GPIO.cleanup()
        pygame.init()
        screen=pygame.display.set_mode((75,75))  #windows size

        # 小车电机引脚定义
        self.IN1 = 18 # 左前轮
        self.IN2 = 23 # 左后轮
        self.IN3 = 24  # 右前轮
        self.IN4 = 25 # 右后轮
        self.ENA = 25 # 左电机控速PWMA 连接Raspberry
        self.ENB = 23 # 右电机控速PWMB 连接Raspberry
 
        # 设置GPIO 口为BCM 编码方式
        GPIO.setmode(GPIO.BCM)
        # 忽略警告信息
        GPIO.setwarnings(False)
        
        GPIO.setup(self.ENA,GPIO.OUT,initial=GPIO.HIGH) 
        GPIO.setup(self.IN1,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.ENB,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.IN3,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN4,GPIO.OUT,initial=GPIO.LOW)
        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        # 启动PWM设置占空比为100（0--100）
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

        self.save_img = True
        self.cap = cv2.VideoCapture(0)  # 调用video1
        self.cap.set(3,320)  # 像素宽度
        self.cap.set(4,240)  # 像素高度

        # create labels
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 3), 'float')
 
        screen=pygame.display.set_mode((75,75))

        self.collect_image()

# 电机引脚初始化操作
    def motor_init(self):
        # global pwm_ENA
        # global pwm_ENB
        GPIO.setup(self.ENA,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.IN1,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.ENB,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.IN3,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN4,GPIO.OUT,initial=GPIO.LOW)
        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(ENA, 2000)
        self.pwm_ENB = GPIO.PWM(ENB, 2000)
        # 启动PWM设置占空比为100（0--100）
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    #小车前进
    def t_up(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)


    #小车后退
    def t_down(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)


    #小车左转
    def t_left(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)


    #小车右转
    def t_right(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    """
    #暂时没有用到
    #小车原地左转
    def spin_left(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)


    #小车原地右转
    def spin_right(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)
    """

    #小车停止
    def t_stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(0)
        self.pwm_ENB.ChangeDutyCycle(0)


    def collect_image(self):
        frame = 1
        saved_frame = 0
        total_frame = 0
        label_0 =0
        label_1 =1
        label_2 =2
        # collect images for training
        print('Start collecting images...')

        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 3), 'float')

        # collect cam frames
        try:
            while self.save_img:
                ret, cam = self.cap.read()    
                roi = cam[120:240, :]  # 120:240
                #print("roi", roi.shape)
                cv2.imshow("roi", roi)
                # while True:
                #     if cv2.waitKey(1) & 0xFF == ord('q'):
                #         break
                
                #image = cv2.imdecode(np.fromstring(cam,dtype=np.uint8),cv2.CV_LOAD_IMAGE_GRAYSCALE)
                gauss = cv2.GaussianBlur(roi,(5,5),0)
                # print("gauss", gauss.shape)
                gray = cv2.cvtColor(gauss,cv2.COLOR_RGB2GRAY)
                # print("gray", gray.shape)
                #dst = cv2.Canny(gray,50,50)
                #ret,thresh1 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY)  
                ret,th3 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)                
                # print("th3", th3.shape)
                cv2.imshow("th3", th3)
                # while True:
                #     if cv2.waitKey(1) & 0xFF == ord('q'):
                #         breakw
                
                #cv2.imwrite('./training_images/frame{:>05}.jpg'.format(frame),dst)

                temp_array = th3.reshape(1,38400).astype(np.float32)
                frame += 1          
                total_frame += 1
 
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    print("exit")
                    print('========================')
                    break
                #wasdzc以及上下左右按键操作
                for event in pygame.event.get():
                    #print("for")
                    if event.type == KEYDOWN:
                        #print("if1")
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w]:                          
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            saved_frame += 1
                            self.t_up(33,33)
                            time.sleep(0.05)
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_0,saved_frame),th3)                          
                            print("forward")
                            print(saved_frame)

                        elif keys[pygame.K_a]:
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            saved_frame += 1
                            self.t_up(20,70)
                            time.sleep(0.05)
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_1,saved_frame),th3)
                            print("left")
                            print(saved_frame)

                        elif keys[pygame.K_d]:
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[2]))
                            saved_frame += 1
                            self.t_up(70,20)
                            time.sleep(0.05)
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_2,saved_frame),th3)
                            print("right")
                            print(saved_frame)

                        elif keys[pygame.K_UP]:                                                     
                            self.t_up(25,25)
                            time.sleep(0.05)
                            print("forward")
 
                        elif keys[pygame.K_s]:
                            self.t_down(25,25)
                            time.sleep(0.05)
                            print("back")
                            
                        elif keys[pygame.K_DOWN]:
                            self.t_down(25,25)
                            time.sleep(0.05)
                            print("back")
 
                        elif keys[pygame.K_LEFT]:
                            self.t_up(12,25)
                            time.sleep(0.05)
                            print("left")
 
                        elif keys[pygame.K_RIGHT]:
                            self.t_up(25,12)
                            time.sleep(0.05)
                            print("right")                      

                        elif keys[pygame.K_a]:
                            self.t_left(25,25)
                            time.sleep(0.05)
                            print("turn left")

                        elif keys[pygame.K_d]:
                            self.t_right(25,25)
                            time.sleep(0.05)
                            print("turn right")

                        elif keys[pygame.K_z]:
                            self.t_down(12,25)
                            time.sleep(0.05)
                            print("left back")

                        elif keys[pygame.K_c]:                          
                            self.t_down(25,12)
                            time.sleep(0.05)
                            print("right back")
 
                        elif keys[pygame.K_p]:
                            print('exit')
                            self.save_img = False                               
                            break

                    elif event.type == KEYUP:
                        self.t_stop()
                        time.sleep(0.05) 
                        print("stop")

            # save training images and labels 
 
            train = image_array[1:, :]
            train_labels = label_array[1:, :]
            # save training data as a numpy file

            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez('./'+directory+'/' + 'train_unloading'+file_name, train=train, train_labels=train_labels)
            except IOError as e:
                print(e)
            e2 = cv2.getTickCount()
 
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Video duration:', time0)
            print('Streaming duration:', time0)

            print((train.shape))
            print((train_labels.shape))
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:                     
            self.cap.release()
            cv2.destroyAllWindows()    
 
if __name__ == '__main__':
    CollectData()
    