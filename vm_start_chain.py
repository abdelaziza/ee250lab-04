"""EE 250L Lab 04 vm_start_chain code
Run vm_cont_chain.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
import socket

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
# this function also subscribes to the pong server when it connects as well prints the message from pong upon connecting
def on_connect(client, userdata, flags, rc):
    client.subscribe("abdelrhm/pong")
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("abdelrhm/pong", on_message_from_pong)
    
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

''' this function sets variable x as a payload and converts it to an int in order to add 1 to create the ping-pong effect, it publishes that number
to the server '''
def on_message_from_pong(client, userdata, message):
   x = message.payload.decode()
   x = int(x)
   x += 1
   client.publish("abdelrhm/ping", f"{x}")
   print("Recieved message from pong:",str(x))


if __name__ == '__main__':
    #get IP address of rpi
    ip_address="172.20.10.10" 

    #create a client object
    client = mqtt.Client()

    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message

    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect("eclipse.usc.edu", 1883, 60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    
    #this code sets the payload to 0 and starts the ping server after the client loop begins, publishes it to the ping server while adding 1 to it 
    time.sleep(1)
    x=0
    client.publish("abdelrhm/ping", f"{x+1}")
    print("Publishing ping")
    time.sleep(1)
