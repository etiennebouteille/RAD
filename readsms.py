import xml.etree.ElementTree as ET
import subprocess
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
RADIATOR_PIN = 16
GPIO.setup(RADIATOR_PIN, GPIO.OUT)
GPIO.output(RADIATOR_PIN, 0)



oldmessage = ""

while True :
    output = subprocess.check_output("./hilink.sh get_sms", shell=True)
    tree = ET.fromstring(output)
    for message in tree.findall('Messages/Message'):
        sender = message.find('Phone').text
        msgcontent = message.find('Content').text
        if (msgcontent != oldmessage) : 
            print sender, msgcontent
            if(msgcontent == "Chauffe Marcel !"):
                GPIO.output(RADIATOR_PIN, 1)
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Ca chauffe ma poule\'", shell=True) 
                print("Ca chauffe!!")
            elif(msgcontent == "Stop"):
                GPIO.output(RADIATOR_PIN, 0)
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Ok mais ca va cailler!!\'", shell=True) 
                print("Ca chauffe plus!!")
            else:
                renvoi = subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Rien compris mon pote\'", shell=True) 
                print("Rien compris mon pote")

            oldmessage = msgcontent
    time.sleep(2)
