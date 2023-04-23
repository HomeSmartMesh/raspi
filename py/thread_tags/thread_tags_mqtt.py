#https://pypi.python.org/pypi/paho-mqtt/1.1
import paho.mqtt.client as mqtt
import socket 
import logging as log
import cfg
from mqtt import mqtt_start
import thread_tags_homeassistant

def replace_friendly_names(topic,friendlyNames):
    for long_name,short_name in friendlyNames.items():
        topic.replace(long_name,short_name)
    return topic

def run():
    config = cfg.configure_log(__file__)
    if(config["homeassistant"]):
        thread_tags_homeassistant.run()

    UDP_IP = "::" # = 0.0.0.0 u IPv4
    UDP_PORT = config["thread"]["port"]

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    #will start a separate thread for looping
    clientMQTT = mqtt_start(config,None,True)

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message = data.decode("utf-8")
        parts = message.split("{")
        topic = parts[0]
        payload = message[len(topic):]
        topic = replace_friendly_names(parts[0],config["friendlyNames"])
        log.info(f"'{topic}' => {payload}")
        clientMQTT.publish(topic,payload)
    return

run()
