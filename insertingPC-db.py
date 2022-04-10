import random
from datetime import * # this library is for the current time
import pymysql
import time
import socket
import qrcode

ip_address = socket.gethostbyname(socket.gethostname())

img = qrcode.make(ip_address)
img.save("ip_add.jpg")

print(ip_address + " Enter this ip address in mobile")



import pickle # This library is for saving or load the model into a file

with open(r"iForest_Model", "rb") as input_file: # defining a input_file variable as the filename of the current model with a read parameter
    model = pickle.load(input_file) # loading the model and define as model variable

#database connection
connection = pymysql.connect(host="localhost", user="admin", passwd="password", database="pd_database")
connection.autocommit = True
cursor = connection.cursor()

searchIp = "SELECT ip_address FROM raspberrypi WHERE ip_address = '{}';".format(ip_address)
cursor.execute(searchIp)
ipRow = cursor.fetchone()

if (len(ipRow) == None):
    password = input("Enter the password: ")

insertRPI = "INSERT INTO raspberrypi (ip_address, status, password) SELECT * FROM (SELECT '{}' as ip_address, '{}' as status, '{}' as password) as tmp WHERE NOT EXISTS (SELECT ip_address FROM raspberrypi WHERE ip_address = '{}') LIMIT 1;".format(ip_address, "not_connected", password, ip_address)
cursor.execute(insertRPI)
connection.commit()

records = None

while(True):
    if(records == None):
        connection = pymysql.connect(host="localhost", user="admin", passwd="password", database="pd_database")
        connection.autocommit = True
        cursor = connection.cursor()


        searcQuery = "SELECT * FROM raspberrypi WHERE ip_address LIKE '{}' and status LIKE '{}';".format(ip_address, "connected")
        cursor.execute(searcQuery)

        records = cursor.fetchone()
    else:
        break
    
print(records)


counter = 0
while(True):
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
    insertPC = "INSERT INTO pc_table(rpi_id, datetime, date, time, power_consumption, power_consumption_score, power_consumption_anomaly_score, status) VALUES({}, '{}', '{}', '{}', {}, {}, {}, '{}');".format(records[0], dateToday, dateNow, TimeNow, float(PC), float(Voltage_score[0]), int(Voltage_anomaly_score[0]), PC_status)

    #executing the quires
    cursor.execute(insertPC)
    connection.commit()

    time.sleep(1)
    counter+=1

#commiting the connection then closing it.

connection.close()

