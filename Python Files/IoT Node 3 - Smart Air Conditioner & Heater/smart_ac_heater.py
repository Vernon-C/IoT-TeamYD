import serial
import paho.mqtt.client as mqtt
import json
import mysql.connector

serial_port = '/dev/ttyACM0'
baud_rate = 9600

thingsboard_host = 'thingsboard.cloud'
access_token = 'KAwFwgrzxfiNt5Qd42xl'

broker_address = "broker.hivemq.com"
broker_port = 1883

ser = serial.Serial(serial_port, baud_rate)

client = mqtt.Client()
subClient = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    
def on_message(client, userdata, msg):
    
    print("Success")
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    print("Topic: ", topic)
    print("Payload: ", payload)
    command = json.loads(payload)
    
    ser.write(str(command['value']).encode('utf-8'))
    
client.on_connect = on_connect
subClient.on_connect = on_connect
client.on_message = on_message
subClient.on_message=on_message

client.username_pw_set(access_token)
client.connect(thingsboard_host, 1883, 60)

subClient.connect(broker_address, broker_port)
topic = "tb/team-yd/sensors/smart-lock/people"
subClient.subscribe(topic)

client.loop_start()
subClient.loop_start()

try:
    while True:
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "kimmy",
        database = "assign3_db"
    )

        data = ser.readline().strip().decode()
        temp, degree_of_ac = map(int, data.split(','))
        
        with mydb:
            mycursor = mydb.cursor()
            sql = "INSERT INTO temp_ac_log (temp, degree_of_ac) VALUES (%s, %s)"
            val = (temp, degree_of_ac)
            mycursor.execute(sql, val)
            mydb.commit()
            
        telemetry_data = {
            'temperature': temp,
            'degree_of_ac': degree_of_ac
            }
        
        client.publish('v1/devices/me/telemetry', json.dumps(telemetry_data))
        print("Publish telemetry data to ThingsBoard", telemetry_data)
        
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    ser.close()
    print("Program terminated by user.")
