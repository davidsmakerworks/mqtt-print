# MQTT Message Printer

# Copyright (c) 2019 David Rice

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from escpos import *
from textwrap import *

import ssl
import systemd.daemon
import configparser

import paho.mqtt.subscribe as subscribe

wrapper = TextWrapper(32)

config = configparser.ConfigParser()
config.read('mqtt-print.ini')

mqtt_server = config['MQTT'].get('Server')
mqtt_port = config['MQTT'].getint('Port')
mqtt_topic = config['MQTT'].get('Topic')
mqtt_use_auth = config['MQTT'].getboolean('Auth')
mqtt_use_tls = config['MQTT'].getboolean('TLS')

if mqtt_use_auth:
    mqtt_username = config['MQTT'].get('Username')
    mqtt_password = config['MQTT'].get('Password')

    mqtt_auth_info = {'username': mqtt_username, 
                      'password': mqtt_password}
else:
    mqtt_auth_info = None

if mqtt_use_tls:
    mqtt_tls_context = ssl.create_default_context()
else:
    mqtt_tls_context = None

printer_file = config['Printer'].get('PrinterFile')

systemd.daemon.notify('READY=1')

while True:
    msg = subscribe.simple(mqtt_topic, hostname=mqtt_server, port=mqtt_port, auth=mqtt_auth_info, tls=mqtt_tls_context)
    prt = printer.File(printer_file)

    msg_string = msg.payload.decode()
    msg_string = wrapper.fill(msg_string)

    prt.set(width=2, align='center')
    prt.text('****************\n')
    prt.text('INCOMING MESSAGE\n')
    prt.text('****************\n\n')
    prt.set(text_type='normal')
    prt.text('{0}'.format(msg_string))
    prt.text('\n\n--------------------------------\n\n\n\n')
    prt = None
