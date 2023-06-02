import serial
import time
import pymysql
from flask import Flask, render_template

app = Flask(__name__)

# Dictionary for the pins
pins = {
  2: {'name' : 'PIN2', 'state' : 0}
}

# Activated when the webpage is loaded
@app.route("/")
def index():
  # Read the pins' statuses from the dictionary and puts them into the html file
  templateData = {
    'pins' : pins
  }
  
  # Get the lock status
  connection = pymysql.connect(host="localhost", user="vernon", password="applepie", database="smart_lock_v2_db")
  cursor = connection.cursor()
  cursor.execute("SELECT status FROM statusLog ORDER BY statusId DESC LIMIT 1;")
  status = cursor.fetchall()
  
#  if (status == 0 or status == 1):
#      if status[0] == 0:
#          status = "Unlocked"
#      elif status[0] == 1:
#          status = "Locked"

  # Get the last unlocked duration
  cursor.execute("SELECT no_of_ent FROM entityLog ORDER BY entityId DESC LIMIT 1;")
  duration = cursor.fetchall()
  
  # Get the list of durations
  cursor.execute("SELECT * FROM entityLog;")
  durationList = cursor.fetchall()
  
  # Get the mean of all durations
  cursor.execute("SELECT AVG(no_of_ent) AS average from entityLog;")
  avgDuration = cursor.fetchall()
  
  # Get the MAX of all durations
  cursor.execute("SELECT MAX(no_of_ent) AS max from entityLog;")
  maxDuration = cursor.fetchall()
  
  # Get the MIN of all durations
  cursor.execute("SELECT MIN(no_of_ent) AS min from entityLog;")
  minDuration = cursor.fetchall()

  return render_template('index2.html', **templateData, status = status,
                         duration = duration, durationList = durationList,
                         avgDuration = avgDuration, maxDuration = maxDuration,
                         minDuration = minDuration)

# Activated when the URL "/action" is passed
@app.route("/<action>")
def action(action):
  # If the action matches, write a serial message to the Arduino
  if action == 'action1':
    ser.write(b"1")
    pins[2]['state'] = 1
  if action == 'action2':
    ser.write(b"2")
    pins[2]['state'] = 0
  if action == 'action3':
    ser.write(b"3")
    pins[6]['state'] = 1
  if action == 'action4':
    ser.write(b"4")
    pins[6]['state'] = 0

  # Read the dictionary and update the html file
  templateData = {
    'pins' : pins
  }
  
  # Get the lock status
  connection = pymysql.connect(host="localhost", user="vernon", password="applepie", database="smart_lock_v2_db")
  cursor = connection.cursor()
  cursor.execute("SELECT status FROM statusLog ORDER BY statusId DESC LIMIT 1;")
  status = cursor.fetchall()
  
#  if (status == 0 or status == 1):
#      if status[0] == 0:
#          status = "Unlocked"
#      elif status[0] == 1:
#          status = "Locked"
      
  # Get the last unlocked duration
  cursor.execute("SELECT no_of_ent FROM entityLog ORDER BY entityId DESC LIMIT 1;")
  duration = cursor.fetchall()

  # Get the list of durations
  cursor.execute("SELECT * FROM entityLog;")
  durationList = cursor.fetchall()

  # Get the mean of all durations
  cursor.execute("SELECT AVG(no_of_ent) AS average from entityLog;")
  avgDuration = cursor.fetchall()
  
  # Get the MAX of all durations
  cursor.execute("SELECT MAX(no_of_ent) AS maximum from entityLog;")
  maxDuration = cursor.fetchall()
  
  # Get the MIN of all durations
  cursor.execute("SELECT MIN(no_of_ent) AS minimum from entityLog;")
  minDuration = cursor.fetchall()

  return render_template('index2.html', **templateData, status = status,
                         duration = duration, durationList = durationList,
                         avgDuration = avgDuration, maxDuration = maxDuration,
                         minDuration = minDuration)

@app.route("/get_status")
def getStatus():
    status = get_status
    return render_template('index2.html', status = status)

# Start the Flask micro-web-framework server
if __name__ == "__main__":
  ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
  ser.flush()
  app.run(host='0.0.0.0', port = 8080, debug = False)

