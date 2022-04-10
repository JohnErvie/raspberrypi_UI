from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

import random
from datetime import * # this library is for the current time
import pymysql
import time
import socket
import qrcode

ip_address = socket.gethostbyname(socket.gethostname())

img = qrcode.make(ip_address)
img.save("ip_add.jpg")

import pickle # This library is for saving or load the model into a file

with open(r"iForest_Model", "rb") as input_file: # defining a input_file variable as the filename of the current model with a read parameter
    model = pickle.load(input_file) # loading the model and define as model variable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
  
        # calling method
        self.UiComponents()

        # opening window in maximized size
        self.showMaximized()
  
        # showing all the widgets
        self.show()
  
    # method for widgets
    def UiComponents(self):
        # creating label
        self.img_QR = QLabel(self)

        self.pixmap = QPixmap('ip_add.jpg')
        self.img_QR.setPixmap(self.pixmap)
        self.img_QR.resize(self.pixmap.width(),self.pixmap.height())
        
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(stylesheet)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())