import serial
import MySQLdb
import datetime
import paho.mqtt.client as mqtt
import json

# Serial port configuration
serial_port = '/dev/ttyUSB0'  # Replace with the appropriate serial port
baud_rate = 9600

# ThingsBoard MQTT configuration
thingsboard_host = 'thingsboard.cloud'
access_token = 'ouz3RDPkNsKUe0fEVumy'  # Replace with your ThingsBoard device access token

broker_address = "broker.hivemq.com"
broker_port = 1883

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate)

# Create an MQTT client instance
client = mqtt.Client()
subClient = mqtt.Client()

# Define callback function for connection success
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))

# Define callback function for message reception
def on_message(client, userdata, msg):
    #print("Received MQTT message: " + str(msg.payload.decode()))
    #command = json.loads(msg.payload)
    
    print("Success")
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    print("Topic: ", topic)
    print("Payload: ", payload)
    command = json.loads(payload)
    
    print(command['value'])
    #ser.write(strValue)
    ser.write(str(command['value']).encode('utf-8'))

# Set the callback functions
client.on_connect = on_connect
subClient.on_connect = on_connect

#client.on_message = on_message

# Subscription
subClient.on_message=on_message

# Connect to the ThingsBoard MQTT broker
client.username_pw_set(access_token)
client.connect(thingsboard_host, 1883, 60)

subClient.username_pw_set("22cf3y1zb6LvkGAzSkoA")
subClient.connect(broker_address, broker_port)
topic = "tb/team-yd/sensors/smart-lock/people"
subClient.subscribe(topic)

# Start the MQTT client loop
client.loop_start()
subClient.loop_start()

# Main loop
try:
    while True:
        # Read serial data from Arduino
        data = ser.readline().strip().decode()

        # parse the data into separate values
        window, alarm = map(str, data.split(','))
        
        # connect to the database
        connection = MySQLdb.connect("localhost","pi","20020620","sensor_db")or dle("Could not connect to database")
        c = connection.cursor()

        # create a table for the data
        c.execute('''CREATE TABLE IF NOT EXISTS alarmSystem
            (timestamp TIMESTAMP, windowState real, alarmState real)''')
    
        # get the current timestamp
        time = datetime.datetime.now().isoformat()
    
        # insert the data into the database
        c.execute("INSERT INTO alarmSystem (timestamp, windowState, alarmState) VALUES (%s,%s,%s)", (time, window, alarm))
        connection.commit()

        # Create a telemetry payload
        telemetry_data = {
            "WindowState": window, 
            "AlarmState":alarm
        }

        # Publish the telemetry data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(telemetry_data))
        print("Published telemetry data to ThingsBoard:", telemetry_data)

except KeyboardInterrupt:
    # Stop the MQTT client loop and disconnect
    client.loop_stop()
    client.disconnect()
    ser.close()
    print("Program terminated by user.")
