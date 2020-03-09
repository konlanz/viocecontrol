from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from datetime import datetime

from Adafruit_IO import MQTTClient
ADAFRUIT_IO_KEY = 'aio_WMYl98LkSGH6B3hsDiixEjsKTALr'

ADAFRUIT_IO_USERNAME = 'kodelan'
FEED_ID = 'bulb'
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
button = Button(2)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/home')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    emit('after connect',  "hello connected")
     
def connected(client):
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    client.subscribe(FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(FEED_ID, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')



@socketio.on('hello')
def handle_message(message):
    global start, stop
    
    if(message == 1 ):
        GPIO.output(21, GPIO.LOW)
        print(34)
        start = datetime.now()
    else:
        GPIO.output(21, GPIO.HIGH)
        print(23)
        
    
    stop = datetime.now()
    timmerx = stop-start
    socketio.emit('timmer', str(timmerx))
  
light_on = False
def handle_abc():
    global start, stop 
    global light_on
    if(light_on):
        led.off()
        light_on = False
        socketio.emit('button', str(0))
            
    else:
        led.on()
        light_on = True
        socketio.emit('button', str(1))
        start = datetime.now()
        
    stop = datetime.now()
    timmerx = stop-start
    print(str(timmerx))
    socketio.emit('timmer', str(timmerx))
    
def message(client, feed_id, payload):
    global start, stop 
    global light_on
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if(light_on):
        GPIO.output(21, GPIO.LOW)
        light_on = False
        socketio.emit('timmerb', 0)
            
    else:
        GPIO.output(21, GPIO.HIGH)
        light_on = True
        socketio.emit('timmerb', 1)
        start = datetime.now()
	
	



@app.route('/')
def home():
    return render_template('xindex.html')
    
# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.on_subscribe  = subscribe
client.connect()
client.loop_background()
if __name__ == '__main__':
	socketio.run(app)
    

