from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import os

import random
from datetime import * # this library is for the current time
import pymysql
import time
import socket
import qrcode

ip_address = socket.gethostbyname(socket.gethostname())

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2,
    )
qr.add_data(ip_address)
qr.make(fit=True)

image = qr.make_image(fill_color="black", back_color="white")

#img = qrcode.make(ip_address)
image.save("ip_add.png")

import pickle # This library is for saving or load the model into a file

with open(r"iForest_Model", "rb") as input_file: # defining a input_file variable as the filename of the current model with a read parameter
    model = pickle.load(input_file) # loading the model and define as model variable

#database connection
connection = pymysql.connect(host="localhost", user="admin", passwd="password", database="pd_database")
connection.autocommit = True
cursor = connection.cursor()

# check ip address if exist
searchIp = "SELECT ip_address FROM raspberrypi WHERE ip_address = '{}';".format(ip_address)
cursor.execute(searchIp)
ipRow = cursor.fetchone()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Group 20")
  
        # setting geometry
        self.resize(600, 400)

        # check ip address if exist
        if (len(ipRow) == None):
            #password = input("Enter the password: ")
            self.ipCheck() 
  
        # calling method
        self.UiComponents()
        #self.Timer()

        self.center()

        # opening window in maximized size
        self.showMaximized()
  
        # showing all the widgets
        self.show()

    #move window to center
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
  
    # method for widgets
    def UiComponents(self):
        # creating label
        self.img_QR = QLabel(self)

        self.pixmap = QPixmap(r"ip_add.png")
        self.img_QR.setPixmap(self.pixmap)
        print(self.pixmap.width(),self.pixmap.height())
        self.img_QR.setGeometry(20,20,self.pixmap.width(),self.pixmap.height())
        
        self.ipLabel = QLabel(self)
        self.ipLabel.setText("IP Address: " + ip_address)
        self.ipLabel.setAlignment(Qt.AlignCenter)
        self.ipLabel.setGeometry(20, 20 + self.pixmap.height(), self.pixmap.width(), 40)
        self.ipLabel.setStyleSheet("border : 5px solid black")

    def ipCheck(self):
        self.passwordLE = QLineEdit(self)
        self.passwordLE.move(130, 22)

        text, ok = QInputDialog.getText(self, 'Password', 'Enter the password')
        if ok:
            self.passwordLE.setText(str(text))
'''
    def Timer(self):
        self.start = True

        # creating a timer object
        self.timer = QTimer(self)

        # adding action to timer
        self.timer.timeout.connect(self.variables)

        # update the timer every second
        self.timer.start(1000)
'''  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(stylesheet)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
