import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import mainwindow


class MainCode(QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        mainwindow.Ui_MainWindow.__init__(self)


        self.setupUi(self)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()
    md.show()
    sys.exit(app.exec_())
