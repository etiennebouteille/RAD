import xml.etree.ElementTree as ET
import subprocess
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
RUN_PIN = 17 #This is the run pin, connected to the non-inverter transistor
STOP_PIN = 27 #This is the stop pin, connected to the inverter transistor
READSTATE_PIN = 23 #This pin reads the state of the coil, via an opto-isolator
GPIO.setup(RUN_PIN, GPIO.OUT)
GPIO.setup(STOP_PIN, GPIO.OUT)
GPIO.setup(READSTATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(RUN_PIN, False)
GPIO.output(STOP_PIN, False)

import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 22

#the run function will send a 100ms pulse on the run pin
def run():
    GPIO.output(RUN_PIN, True)
    time.sleep(0.1)
    GPIO.output(RUN_PIN, False)
    return

#the stop function will send a 100ms pulse on the stop pin
def stop():
    GPIO.output(STOP_PIN, True)
    time.sleep(0.1)
    GPIO.output(STOP_PIN, False)
    return

#the readState function will check if the coil of the relay is powered
def readState():
    return GPIO.input(READSTATE_PIN)

def getTemperature():
    Humi = 0
    Temp = 0
    Humi, Temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return Temp, Humi;

oldmsgdate = ""

while True :
    output = subprocess.check_output("./hilink.sh get_sms", shell=True)
    tree = ET.fromstring(output)
    for message in tree.findall('Messages/Message'):
        sender = message.find('Phone').text
        msgcontent = message.find('Content').text
        msgdate = message.find('Date').text
        if (msgdate != oldmsgdate) : 
            print sender, msgcontent
            if(msgcontent == "Chauffe Marcel!"):
                run()
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Ca chauffe ma poule\'", shell=True) 
                print("Ca chauffe!!")
            elif(msgcontent == "Stop"):
                stop()
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Ok mais ca va cailler!!\'", shell=True) 
                print("Ca chauffe plus!!")
            elif(msgcontent == "Ca va?"): #returns the data to the sender
                temperature, humidity = getTemperature()
                temperature = round(temperature, 1)
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Il fait " + str(temperature) + " degres\'", shell=True)
                print("Il fait " + str(temperature))
            else:
                #renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Rien compris mon pote\'", shell=True) 
                print("Rien compris mon pote")

            print(readState())
            oldmsgdate = msgdate
    time.sleep(10)
