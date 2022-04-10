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

        # RPI Info
        searcQuery = "SELECT * FROM raspberrypi WHERE ip_address LIKE '{}' and status LIKE '{}';".format(ip_address, "connected")
        cursor.execute(searcQuery)

        self.RPIrecords = cursor.fetchone()

        # check ip address if exist
        if (len(ipRow) == None):
            #password = input("Enter the password: ")
            self.ipCheck() 
  
        # calling method
        self.UiComponents()
        self.Timer()

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
        #self.ipLabel.setStyleSheet("border : 5px solid black")

        self.passwordLabel = QLabel(self)
        self.passwordLabel.setText("Password: " + self.RPIrecords[2])
        self.passwordLabel.setAlignment(Qt.AlignCenter)
        self.passwordLabel.setGeometry(20, 20 + self.pixmap.height() + 40, self.pixmap.width(), 40)

        self.button = QPushButton("Stop", self)
        self.button.setGeometry(20+60, 20 + self.pixmap.height() + 40 + 40, 60, 40)
        self.button.clicked.connect(self.stopStartFuction)


    def ipCheck(self):
        self.passwordLE = QLineEdit(self)
        self.passwordLE.move(130, 22)

        text, ok = QInputDialog.getText(self, 'Password', 'Enter the password')
        if ok:
            self.passwordLE.setText(str(text))

    def Timer(self):
        self.start = True

        # creating a timer object
        self.timer = QTimer(self)

        # adding action to timer
        self.timer.timeout.connect(self.mainFunction)

        # update the timer every second
        self.timer.start(1000)

    def mainFunction(self):
        PC = random.random()*(200-0)+0 # declaring PC variable as power consumption value
        PC = float("{:.2f}".format(PC)) #convert into 2 decimal places
        #PC = 70 
        dateToday = datetime.now() # getting the current and declare as datetime variable
        dateNow = date.today() # today's date
        TimeNow = (datetime.time(datetime.now())) # current time

        # using now the model 
        Voltage_score = model.decision_function([[PC]]) # Computing the Average anomaly score of PC variable of the base classifiers

        Voltage_anomaly_score = model.predict([[PC]]) # Predict if a particular sample is an outlier or not (anomaly or normal)

        if Voltage_anomaly_score == -1: 
            PC_status = 'Anomaly' # if the Voltage_anomaly_score is equal to -1 then this is a Anamaly

        else:
            PC_status = 'Normal' # if the Voltage_anomaly_score is equal to 1 then this is a Normal Data

        # queries for inserting values
        insertPC = "INSERT INTO pc_table(rpi_id, datetime, date, time, power_consumption, power_consumption_score, power_consumption_anomaly_score, status) VALUES({}, '{}', '{}', '{}', {}, {}, {}, '{}');".format(self.RPIrecords[0], dateToday, dateNow, TimeNow, float(PC), float(Voltage_score[0]), int(Voltage_anomaly_score[0]), PC_status)

        #executing the quires
        cursor.execute(insertPC)
        connection.commit()

    def stopStartFuction(self):
        if (self.start == True):
            self.button.setText("Start")
            self.start = False # pause the timer
        else:
            self.button.setText("Start")
            self.start = True # start the timer
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(stylesheet)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
