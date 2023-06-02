import paho.mqtt.publish as publish
import mysql.connector
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while 1:
    mydb = mysql.connector.connect(host="localhost", user="vernon",
                                   password="applepie", database="smart_lock_v2_db")
    
    print(mydb)
    
    while arduino.in_waiting == 0:
        pass
    
    oldLine = arduino.readline()
    line = oldLine.decode()
    
    if str(line[0]) == 'S':
        value = str(line[8:])
        print(value)
    elif str(line[0]) == 'E':
        value = int(line[11:])
        print(value)
    
    # Insert value into the database
    with mydb:
        mycursor = mydb.cursor()
                    
        if str(line[0]) == 'S':
            mycursor.execute("INSERT INTO statusLog (status) VALUES ('%s')" %(value))
        elif str(line[0]) == 'E':
            mycursor.execute("INSERT INTO entityLog (no_of_ent) VALUES (%s)" %(value))
            
        mydb.commit()
        mycursor.close()

    # Send value to ThingsBoard
    if str(line[0]) == 'E':
        publish.single(topic = "tb/team-yd/sensors/smart-lock/people", payload = '{"value":' +
                       str(value) +'}', hostname = "broker.hivemq.com")
    elif str(line[0]) == 'S':
        publish.single(topic = "v1/devices/me/telemetry", payload = '{"status":' +
                       str(value) +'}', hostname = "thingsboard.cloud",
                       auth = {'username': "22cf3y1zb6LvkGAzSkoA", 'password': ""})
