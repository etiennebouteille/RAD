import xml.etree.ElementTree as ET
import subprocess
import time

print("received following message : " + content + " from number : " + phonenum)
while True :
    output = subprocess.check_output("./hilink.sh get_sms", shell=True)
    tree = ET.fromstring(output)
    for message in tree.findall('Messages/Message'):
        sender = message.find('Phone').text
        msgcontent = message.find('Content').text
        print sender, msgcontent
        if(msgcontent == "Chauffe Marcel"):
            print("Allumer le radiateur")
        else:
            print("Rien compris mon pote")
    time.sleep(2)
