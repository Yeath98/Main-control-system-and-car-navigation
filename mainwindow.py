# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys#获取参数的api
import cv2,glob
import numpy as np
from urllib import parse, request
import json,time
import sys
from sklearn.model_selection import train_test_split

import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        # 无任何标题栏和边框
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        self.changeFlag = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.maturitylabel = QtWidgets.QLabel(self.centralwidget)
        self.maturitylabel.setGeometry(QtCore.QRect(9, 9, 60, 16))
        self.maturitylabel.setObjectName("maturitylabel")

        self.videolable = QtWidgets.QLabel(self.centralwidget)
        self.videolable.setGeometry(QtCore.QRect(260, 10, 24, 16))
        self.videolable.setObjectName("videolable")

        self.maturityframe = QtWidgets.QFrame(self.centralwidget)
        #self.maturityframe = QtWidgets.QLabel(self.centralwidget)
        #self.maturityframe.setScaledContents(True)  # 让图片自适应label大小
        self.maturityframe.setGeometry(QtCore.QRect(10, 40, 60, 350))
        self.maturityframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.maturityframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.maturityframe.setObjectName("maturityframe")


        #状态栏
        self.status = self.statusBar()
        # 状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        #self.status.showMessage('圣女果采摘机器', 0)
        self.statuslabel = QLabel()
        self.timelable = QLabel('')
        self.status.addPermanentWidget(self.statuslabel, stretch=0)
        self.status.addPermanentWidget(self.timelable, stretch=0)
        timer = QtCore.QTimer(self.timelable)
        timer.timeout.connect(self.showtime)
        timer.start()
        #测试用例，后期根据状态实时反馈
        self.statuslabel.setText('状态：'+'No Action')



        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(130, 40, 81, 81))
        self.startButton.setText("")
        self.startButton.setObjectName("startButton")
        #/ home / yzh1998 / School2 /
        self.startButton.setIcon(QIcon(QPixmap('F:\Py_experiment\School2\开始.png')))
        self.startButton.setIconSize(QtCore.QSize(64, 64))
        self.startButton.setFlat(True)
        # 点击信号与槽函数进行连接
        self.startButton.clicked.connect(self.btnstate)



        self.vidoewidget = QtWidgets.QLabel(self.centralwidget)
        self.vidoewidget.setGeometry(QtCore.QRect(300, 30, 750, 500))
        self.vidoewidget.setObjectName("vidoewidget")


        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(130, 190, 81, 81))
        self.trainButton.setText("")
        self.trainButton.setObjectName("trainButton")
        self.trainButton.setIcon(QIcon(QPixmap('F:\Py_experiment\School2\采摘.png')))
        self.trainButton.setIconSize(QtCore.QSize(64, 64))
        self.trainButton.setFlat(True)





        menu = QMenu(self)
        # 设置连接槽
        Picking = QAction('采摘导航', self)
        Picking.triggered.connect(self.onPicking)
        menu.addAction(Picking)

        Unloading = QAction('卸货导航', self)
        Unloading.triggered.connect(self.Unloading)
        menu.addAction(Unloading)

        Charge = QAction('充电导航', self)
        Charge.triggered.connect(self.Charge)
        menu.addAction(Charge)



        self.trainButton.setMenu(menu)
        # 去掉默认的向下箭头
        self.trainButton.setStyleSheet("QPushButton::menu-indicator{image:none;}")



        self.framelabel = QtWidgets.QLabel(self.centralwidget)
        self.framelabel.setGeometry(QtCore.QRect(10, 550, 60, 16))#10, 570, 60, 16
        self.framelabel.setObjectName("framelabel")

        self.traintextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.traintextEdit.setEnabled(True)
        self.traintextEdit.setGeometry(QtCore.QRect(70, 540, 61, 31))#70, 560, 61, 31
        self.traintextEdit.setAcceptDrops(True)
        self.traintextEdit.setObjectName("traintextEdit")
        self.traintextEdit.setReadOnly(True)  # 设置为只读，即可以在代码中向textEdit里面输入，但不能从界面上输入,没有这行代码即可以从界面输入



        self.cherrylabel = QtWidgets.QLabel(self.centralwidget)
        self.cherrylabel.setGeometry(QtCore.QRect(160, 550, 72, 16))#160, 570, 72, 16
        self.cherrylabel.setObjectName("cherrylabel")


        self.cherrytextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.cherrytextEdit.setGeometry(QtCore.QRect(240, 540, 61, 31))#240, 560, 61, 31
        self.cherrytextEdit.setObjectName("cherrytextEdit")
        self.cherrytextEdit.setReadOnly(True)  #设置为只读，即可以在代码中向textEdit里面输入，但不能从界面上输入,没有这行代码即可以从界面输入
        # 进制100个==1框
        # 显示数字到textEdit：数字必须要转换成字符串
        count1 = 0
        count2 = 0
        str1 = str(count1)
        str2 = str(count2)

        self.cherrytextEdit.setText(str1)
        # textEdit 用toPlainText()方法
        # linEdit 直接用self.lineEdit.text()即可获取
        str3 = self.cherrytextEdit.toPlainText()
        if str3 == str1:
            self.traintextEdit.setText(str2)



        self.trainlabel = QtWidgets.QLabel(self.centralwidget)
        self.trainlabel.setGeometry(QtCore.QRect(160, 290, 24, 16))
        self.trainlabel.setObjectName("trainlabel")

        self.startlabel = QtWidgets.QLabel(self.centralwidget)
        self.startlabel.setGeometry(QtCore.QRect(160, 140, 24, 16))
        self.startlabel.setObjectName("startlabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.maturitylabel.setText(_translate("MainWindow", "成熟度选择"))
        self.videolable.setText(_translate("MainWindow", "视频"))
        self.framelabel.setText(_translate("MainWindow", "采摘框数："))
        self.cherrylabel.setText(_translate("MainWindow", "圣女果个数："))
        self.trainlabel.setText(_translate("MainWindow", "模式"))
        self.startlabel.setText(_translate("MainWindow", "开始"))

        # 选择成熟度
        class CColorSlider(QSlider):

            TypeAlpha = 0  # 透明颜色类型
            TypeRainbow = 1  # 彩虹色

            colorChanged = pyqtSignal(QColor)  # 颜色, 透明度

            def __init__(self, types, parent=None, color=Qt.black):

                super(CColorSlider, self).__init__(Qt.Vertical, parent)
                self.setObjectName('Custom_Color_Slider')

                self.setCursor(Qt.PointingHandCursor)
                self.valueChanged.connect(self.onValueChanged)
                self._types = types
                self._color = color
                self._isFirstShow = True
                self._imageRainbow = None  # 彩虹背景图
                self._imageAlphaColor = None  # 带颜色透明图

                self._imageCircle = None  # 圆形滑块图
                self._imageCircleHover = None  # 圆形滑块悬停图
                self.setToolTip('彩虹色' if self._types == self.TypeRainbow else '透明度')

            def reset(self):
                self.setValue(0 if self._types == self.TypeRainbow else self.maximum())

            def updateAlpha(self, color):
                self.blockSignals(True)
                self.blockSignals(False)

            def showEvent(self, event):
                super(CColorSlider, self).showEvent(event)
                if self._isFirstShow:
                    self._isFirstShow = False
                    self.setRange(0, max(1, self.width() - 1))
                    if self._types == self.TypeAlpha:
                        self.blockSignals(True)
                        self.setValue(self.maximum())
                        self.blockSignals(False)
                    self.gradientCirclePixmap()
                    self.gradientPixmap(self._types, self._color)

            def pick(self, pt):
                return pt.y() if self.orientation() == Qt.Vertical else pt.x()

            def pixelPosToRangeValue(self, pos):
                option = QStyleOptionSlider()
                self.initStyleOption(option)
                gr = self.style().subControlRect(QStyle.CC_Slider,
                                                 option, QStyle.SC_SliderGroove, self)
                sr = self.style().subControlRect(QStyle.CC_Slider,
                                                 option, QStyle.SC_SliderHandle, self)
                if self.orientation() == Qt.Horizontal:

                    sliderLength = sr.width()
                    sliderMin = gr.x()
                    sliderMax = gr.right() - sliderLength + 1
                else:
                    sliderLength = sr.height()
                    sliderMin = gr.y()
                    sliderMax = gr.bottom() - sliderLength + 1

                return QStyle.sliderValueFromPosition(
                    self.minimum(), self.maximum(), pos - sliderMin,
                                                    sliderMax - sliderMin, option.upsideDown)

            def mousePressEvent(self, event):
                # 获取上面的拉动块位置
                event.accept()
                option = QStyleOptionSlider()
                self.initStyleOption(option)
                rect = self.style().subControlRect(
                    QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
                rect.setX(max(min(rect.y(), self.width() - self.height()), 0))
                rect.setWidth(self.width())
                rect.setHeight(self.width())
                center = rect.center() - rect.topLeft()
                self.setSliderPosition(self.pixelPosToRangeValue(self.pick(event.pos() - center)))
                self.setSliderDown(True)

            def mouseMoveEvent(self, event):
                event.accept()
                self.setSliderPosition(
                    self.pixelPosToRangeValue(self.pick(event.pos())))

            def paintEvent(self, event):
                if not (self._imageRainbow or self._imageAlpha):
                    return super(CColorSlider, self).paintEvent(event)

                option = QStyleOptionSlider()
                self.initStyleOption(option)

                # 背景Rect
                groove = self.style().subControlRect(
                    QStyle.CC_Slider, option, QStyle.SC_SliderGroove, self)

                groove.adjust(3, 5, -3, -5)

                # 滑块Rect
                handle = self.style().subControlRect(
                    QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
                handle.setX(max(min(handle.x(), self.width() - self.height()), 0))
                handle.setWidth(self.width())
                handle.setHeight(self.width())
                radius = self.width() / 2
                painter = QPainter(self)
                painter.setPen(Qt.NoPen)
                painter.drawImage(groove, self._imageRainbow if self._imageRainbow else self._imageAlpha)

                if not self._imageCircle or not self._imageCircleHover:
                    painter.setBrush(QColor(245, 245, 245) if option.state &
                                                              QStyle.State_MouseOver else QColor(254, 254, 254))
                    painter.drawRoundedRect(handle, radius, radius)
                else:
                    painter.drawImage(handle, self._imageCircleHover if option.state &
                                                                        QStyle.State_MouseOver else self._imageCircle)

            def gradientCirclePixmap(self):
                xy = self.height() / 2
                radius = self.height() * 0.8

                # 绘制普通状态下圆形的滑块
                circleColor = QRadialGradient(xy, xy, radius, xy, xy)
                circleColor.setColorAt(0.5, QColor(254, 254, 254))
                circleColor.setColorAt(0.7, QColor(0, 0, 0, 60))
                circleColor.setColorAt(0.7, QColor(0, 0, 0, 30))
                circleColor.setColorAt(0.9, QColor(0, 0, 0, 0))
                self._imageCircle = QImage(
                    self.height(), self.height(), QImage.Format_ARGB32)
                self._imageCircle.fill(Qt.transparent)
                painter = QPainter()
                painter.begin(self._imageCircle)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                painter.setPen(Qt.NoPen)
                painter.setBrush(circleColor)
                painter.drawRoundedRect(0, 0, self.height(), self.height(), xy, xy)
                painter.end()

                # 绘制悬停状态下圆形的滑块
                circleColorHover = QRadialGradient(xy, xy, radius, xy, xy)
                circleColorHover.setColorAt(0.5, QColor(245, 245, 245))
                circleColorHover.setColorAt(0.7, QColor(0, 0, 0, 30))
                circleColorHover.setColorAt(0.9, QColor(0, 0, 0, 0))
                self._imageCircleHover = QImage(
                    self.height(), self.height(), QImage.Format_ARGB32)
                self._imageCircleHover.fill(Qt.transparent)
                painter = QPainter()
                painter.begin(self._imageCircleHover)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                painter.setPen(Qt.NoPen)
                painter.setBrush(circleColorHover)
                painter.drawRoundedRect(0, 0, self.height(), self.height(), xy, xy)
                painter.end()

            def gradientPixmap(self, types, color):
                #生成渐变图片

                pixSize = 5

                if True:
                    gradient = QLinearGradient(self.width(), 0, self.width(), 255)
                    # QLinearGradient ( qreal x1, qreal y1, qreal x2, qreal y2 )
                    # 其中x1,y1表示渐变起始坐标, x2,y2表示渐变终点坐标
                    # 如果只有x相等,则表示垂直线性渐变,如果只有y相等,则表示平行线性渐变,否则就是斜角线性渐变
                    #gradient.setColorAt(0, QColor('#ff0000'))
                    gradient.setColorAt(0.01, QColor('#ffff00'))
                    gradient.setColorAt(0.45, QColor('#00ff00'))
                    #gradient.setColorAt(0.5, QColor('#00ffff'))
                    #gradient.setColorAt(0.67, QColor('#0000ff'))
                    #gradient.setColorAt(0.83, QColor('#ff00ff'))
                    gradient.setColorAt(0.99, QColor('#ff0000'))
                    self._imageRainbow = QImage(self.width(), self.height(), QImage.Format_ARGB32)#self.width(), self.height()
                    painter = QPainter()
                    painter.begin(self._imageRainbow)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                    painter.fillRect(0, 0, self.width(), self.height(), gradient)
                    painter.end()

            def onValueChanged(self, value):
                hh = int(self.height() / 2)
                color = self.colorFromPoint(value, hh)
                self.colorChanged.emit(color)

            def colorFromPoint(self, x, y):
                if not self._imageRainbow:
                    return QColor(Qt.red)
                print(self.value())
                return self._imageRainbow.pixelColor(x, y)

        layout = QGridLayout(self.maturityframe)

        slider1 = CColorSlider(CColorSlider.TypeRainbow, self.maturityframe)
        slider1.setStyle(QStyleFactory.create('windows'))

        # slider1.colorChanged.connect(lambda c: print('TypeRainbow:', c.name()))

        layout.addWidget(slider1)


    #按钮变化
    def btnstate(self):
        if self.changeFlag == 0:
            self.startButton.setIcon(QIcon(QPixmap('F:\Py_experiment\School2\暂停.png')))
            self.startlabel.setText('结束')
            self.changeFlag = 1
        elif self.changeFlag == 1:

            self.startButton.setIcon(QIcon(QPixmap('F:\Py_experiment\School2\开始.png')))
            self.startlabel.setText('开始')
            self.changeFlag = 0


    #背景
    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("backimage.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)




    #QAction触发函数

    #卸货导航训练
    def Unloading(self):
        QMessageBox.information(self, 'Tips', 'Loading training data...')
        self.statuslabel.setText('状态：' + 'Loading training data...')
        print('Loading training data...')
        e0 = cv2.getTickCount()

        # 读取训练数据
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 3), 'float')
        training_data = glob.glob('./training_data/train_unloading*.npz')  # 在本工程目录中找到training_data目录并读取里面的所有npz文件

        #无数据退出
        if not training_data:
            print("No training data in directory, exit")
            sys.exit()

        for single_npz in training_data:
            with np.load(single_npz) as data:
                train_temp = data['train']
                train_labels_temp = data['train_labels']
            image_array = np.vstack((image_array, train_temp))
            label_array = np.vstack((label_array, train_labels_temp))

        X = image_array[1:, :]
        y = label_array[1:, :]
        print('Image array shape: ', X.shape)
        print('Label array shape: ', y.shape)

        e00 = cv2.getTickCount()
        time0 = (e00 - e0) / cv2.getTickFrequency()
        print('Loading image duration:', time0)

        # 训练测试 split, 8:2
        train, test, train_labels, test_labels = train_test_split(X, y, test_size=0.2)

        # 设置开始
        e1 = cv2.getTickCount()

        # 创建MLP（神经网络）

        model = cv2.ml.ANN_MLP_create()
        # 创建人工网络神经层
        model.setLayerSizes(np.int32([38400, 64, 3]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.001))
        # BP方法
        model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        # 速度
        model.setBackpropWeightScale(0.01)
        #最低部分不要
        model.setBackpropMomentumScale(0.1)
        # criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
        # criteria2 = (cv2.TERM_CRITERIA_COUNT, 100, 0.001)
        print('Training MLP ...')
        # num_iter = model.train(train, train_labels, None, params = params)
        num_iter = model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))

        #设置time
        e2 = cv2.getTickCount()
        time = (e2 - e1) / cv2.getTickFrequency()
        print('Training duration:', time)

        #训练数据
        ret_0, resp_0 = model.predict(train)
        prediction_0 = resp_0.argmax(-1)
        true_labels_0 = train_labels.argmax(-1)

        train_rate = np.mean(prediction_0 == true_labels_0)
        print('Train accuracy: ', "{0:.2f}%".format(train_rate * 100))

        #测试数据
        ret_1, resp_1 = model.predict(test)
        prediction_1 = resp_1.argmax(-1)
        true_labels_1 = test_labels.argmax(-1)

        test_rate = np.mean(prediction_1 == true_labels_1)
        print('Test accuracy: ', "{0:.2f}%".format(test_rate * 100))

        if not os.path.exists('mlp_xml'):
            os.makedirs('mlp_xml')

        # 保存模型
        model.save('mlp_xml/unloading_mlp.xml')
        self.statuslabel.setText('状态：' + 'Success')


    #充电导航训练
    def Charge(self):
        QMessageBox.information(self, 'Tips', 'Loading training data...')
        self.statuslabel.setText('状态：' + 'Loading training data...')
        print('Loading training data...')
        e0 = cv2.getTickCount()

        # 读取训练数据
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 3), 'float')
        training_data = glob.glob('./training_data/train_charging*.npz')  # 在本工程目录中找到training_data目录并读取里面的所有npz文件

        # 无数据退出
        if not training_data:
            print("No training data in directory, exit")
            sys.exit()

        for single_npz in training_data:
            with np.load(single_npz) as data:
                train_temp = data['train']
                train_labels_temp = data['train_labels']
            image_array = np.vstack((image_array, train_temp))
            label_array = np.vstack((label_array, train_labels_temp))

        X = image_array[1:, :]
        y = label_array[1:, :]
        print('Image array shape: ', X.shape)
        print('Label array shape: ', y.shape)

        e00 = cv2.getTickCount()
        time0 = (e00 - e0) / cv2.getTickFrequency()
        print('Loading image duration:', time0)

        # 训练测试 split, 8:2
        train, test, train_labels, test_labels = train_test_split(X, y, test_size=0.2)

        # 设置开始
        e1 = cv2.getTickCount()

        # 创建MLP（神经网络）

        model = cv2.ml.ANN_MLP_create()
        # 创建人工网络神经层
        model.setLayerSizes(np.int32([38400, 64, 3]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.001))
        # BP方法
        model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        # 速度
        model.setBackpropWeightScale(0.01)
        # 最低部分不要
        model.setBackpropMomentumScale(0.1)
        # criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
        # criteria2 = (cv2.TERM_CRITERIA_COUNT, 100, 0.001)
        print('Training MLP ...')
        # num_iter = model.train(train, train_labels, None, params = params)
        num_iter = model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))

        # 设置time
        e2 = cv2.getTickCount()
        time = (e2 - e1) / cv2.getTickFrequency()
        print('Training duration:', time)

        # 训练数据
        ret_0, resp_0 = model.predict(train)
        prediction_0 = resp_0.argmax(-1)
        true_labels_0 = train_labels.argmax(-1)

        train_rate = np.mean(prediction_0 == true_labels_0)
        print('Train accuracy: ', "{0:.2f}%".format(train_rate * 100))

        # 测试数据
        ret_1, resp_1 = model.predict(test)
        prediction_1 = resp_1.argmax(-1)
        true_labels_1 = test_labels.argmax(-1)

        test_rate = np.mean(prediction_1 == true_labels_1)
        print('Test accuracy: ', "{0:.2f}%".format(test_rate * 100))

        if not os.path.exists('mlp_xml'):
            os.makedirs('mlp_xml')

        # 保存模型
        model.save('mlp_xml/charge_mlp.xml')
        self.statuslabel.setText('状态：' + 'Success')



    #采摘训练导航即小车视觉导航
    def onPicking(self):
        QMessageBox.information(self, 'Tips', 'Loading training data...')
        self.statuslabel.setText('状态：' + 'Loading training data...')
        print('Loading training data...')
        e0 = cv2.getTickCount()

        # 读取训练数据
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 3), 'float')
        training_data = glob.glob('./training_data/train_onPicking*.npz')  # 在本工程目录中找到training_data目录并读取里面的所有npz文件

        # 无数据退出
        if not training_data:
            print("No training data in directory, exit")
            sys.exit()

        for single_npz in training_data:
            with np.load(single_npz) as data:
                train_temp = data['train']
                train_labels_temp = data['train_labels']
            image_array = np.vstack((image_array, train_temp))
            label_array = np.vstack((label_array, train_labels_temp))

        X = image_array[1:, :]
        y = label_array[1:, :]
        print('Image array shape: ', X.shape)
        print('Label array shape: ', y.shape)

        e00 = cv2.getTickCount()
        time0 = (e00 - e0) / cv2.getTickFrequency()
        print('Loading image duration:', time0)

        # 训练测试 split, 8:2
        train, test, train_labels, test_labels = train_test_split(X, y, test_size=0.2)

        # 设置开始
        e1 = cv2.getTickCount()

        # 创建MLP（神经网络）

        model = cv2.ml.ANN_MLP_create()
        # 创建人工网络神经层
        model.setLayerSizes(np.int32([38400, 64, 3]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.001))
        # BP方法
        model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        # 速度
        model.setBackpropWeightScale(0.01)
        # 最低部分不要
        model.setBackpropMomentumScale(0.1)
        # criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
        # criteria2 = (cv2.TERM_CRITERIA_COUNT, 100, 0.001)
        print('Training MLP ...')
        # num_iter = model.train(train, train_labels, None, params = params)
        num_iter = model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))

        # 设置time
        e2 = cv2.getTickCount()
        time = (e2 - e1) / cv2.getTickFrequency()
        print('Training duration:', time)

        # 训练数据
        ret_0, resp_0 = model.predict(train)
        prediction_0 = resp_0.argmax(-1)
        true_labels_0 = train_labels.argmax(-1)

        train_rate = np.mean(prediction_0 == true_labels_0)
        print('Train accuracy: ', "{0:.2f}%".format(train_rate * 100))

        # 测试数据
        ret_1, resp_1 = model.predict(test)
        prediction_1 = resp_1.argmax(-1)
        true_labels_1 = test_labels.argmax(-1)

        test_rate = np.mean(prediction_1 == true_labels_1)
        print('Test accuracy: ', "{0:.2f}%".format(test_rate * 100))

        if not os.path.exists('mlp_xml'):
            os.makedirs('mlp_xml')

        # 保存模型
        model.save('mlp_xml/onPicking_mlp.xml')
        self.statuslabel.setText('状态：' + 'Success')

        """
        #与范式公司对接程序的#接口测试代码
        #POST无法进行网页测试，需要curl指令或者POSTMAN发送json数据测试即下面的parameter
        self.statuslabel.setText('状态：' + 'Error')
        #os.system("ls")
        #需要修改相应的parameter参数；如parameter = {"type": "1", "direction": "0"}
        parameter = {"username": "mycai", "password": "123456"}
        # json串数据使用
        parameter = json.dumps(parameter).encode(encoding='utf-8')

        header_info = {"Content-Type": "application/json"}
        #需要修改相应的url参数,地址也需要修改；如url="http://127.0.0.1:5000/pick"
        url = "http://127.0.0.1:5000/login"
        req = request.Request(url=url, data=parameter, headers=header_info)
        res = request.urlopen(req)
        res = res.read()

        print('返回参数：' + str(res))
        print('返回参数，转码utf-8后：' + str(res.decode(encoding='utf-8')))
        """

    #状态栏显示时间
    def showtime(self):
        self.timelable.setText(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
