import os
import sys
import logging
import paho.mqtt.client as mqtt
import json
import random
import time
from create_data import get_messages
from datetime import datetime

PUBLIC_TLS_ADDRESS = "mqtt.synergitech.com.au"
PUBLIC_TLS_ADDRESS_PORT = 8883

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
# print(os.getcwd())

QOS = 1

logging.basicConfig(filename='paho.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def stop(client):
  client.disconnect()
  client.loop_stop()
  logging.info("Disconnecting")
  time.sleep(1)
  sys.exit(0)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
  if rc == 0:
    # print("\nConnected successfully to MQTT broker")
    logging.info("Connected successfully to MQTT broker")
    pass
  else:
    # print("\nFailed to connect, return code = " + str(rc))
    logging.info(f"Failed to connect, return code = {str(rc)}")
    pass


def on_subscribe(client, userdata, mid, granted_qos):
  # print("\nSubscribed with message id (mid) = " + str(mid) + " and QoS = " + str(granted_qos))
  logging.info(f"Subscribed with message id = {str(mid)} and QoS = {str(granted_qos)}")
  pass


def on_disconnect(client, userdata, disconnect_flags, rc, properties):
  # print("\nDisconnected with result code = " + str(rc))
  logging.info(f"Disconnected with result code = {str(rc)}")
  pass


def on_log(client, userdata, level, buf):
  # print("\nLog: " + buf)
  # logging_level = client.LOGGING_LEVEL[level]
  logging.debug(f"MQTT Log: {buf}")


def send_data(msg):
  if msg:
    topic = "upload_feed"
    # print("Publishing messages to topic " + topic + " with QoS = " + str(QOS))
    logging.info(f"Publishing messages to topic {topic} with QoS = {str(QOS)}")

    result = mqttc.publish(topic, msg, qos=1)

    # result: [0, 2]
    status = result[0]
    if status == 0:
      # print("Sent " + str(msg) + " to topic " + topic)
      logging.info(f"Sent {str(msg)} to topic {topic}")
      pass
    else:
      logging.error(f"Failed to send message to topic {topic}")
      # print("Failed to send message to topic " + topic)

  else:
    # print("Can not subscribe or publish to topic")
    stop(mqttc)

# Generate client ID with pub prefix randomly
client_id = f'pi-virtual-devices'

# print("Create new mqtt client instance")
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, protocol=mqtt.MQTTv5)

# print("Assign callback functions")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# print("Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT))
mqttc.tls_set(ca_certs="/home/nigel/virtual_iot_devices/certs/ca.crt", certfile="/home/nigel/virtual_iot_devices/certs/pi.crt", keyfile="/home/nigel/virtual_iot_devices/certs/pi.key")

mqttc.connect(PUBLIC_TLS_ADDRESS, PUBLIC_TLS_ADDRESS_PORT, 60) # Can return TimeoutError: timed out
mqttc.loop_start()

if __name__ == '__main__':
  try:
    msgs = get_messages()
    if msgs:
      for m in msgs:
        send_data(json.dumps(m))
        time.sleep(0.2)
  except Exception as e:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/nigel/virtual_iot_devices/error.log", "a") as log_file:
      log_file.write(f"[{now}] Error: {e.__class__.__name__}: {e}\n")

  # stop(mqttc)
