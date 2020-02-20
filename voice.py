from Adafruit_IO import MQTTClient
import requests

ADAFRUIT_IO_KEY = 'aio_WMYl98LkSGH6B3hsDiixEjsKTALr'
ADAFRUIT_IO_USERNAME = 'kodelan'


def connected(client):
    print("hello")
    client.subscribe("bulb")

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    if(feed_id == "bulb"):
        if(payload == '1'):
            print("bulb on")
        else:
            print("bulb off")



client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message
client.connect()
client.loop_background()
