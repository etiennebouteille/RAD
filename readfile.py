import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

import pandas as pd
import time

oldtime = time.time() 

homeinfo = pd.read_csv('rad-data.csv')
print(homeinfo)

#set variables to the first line of data in the file
temperature = homeinfo['temperature'].values[0]
thermostat = homeinfo['thermostat'].values[0]

radiatorOn = False

def getTemperature():
    #TODO: use temperature sensor
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
    homeinfo.at[0, 'temperature'] = temperature #replace temperature in the first line of file with measured temp
    return temperature 

def setRadiatorPower():
    if temperature < thermostat :
        return True
    if temperature >= thermostat :
        return False

def changeTemp(temp):
    if radiatorOn:
        temp += 1
        return temp
    else:
        return temp

while True:
    temperature = getTemperature()
    print("temperature = " + str(temperature))
    radiatorOn = setRadiatorPower()
    print(radiatorOn)
    #if time.time() - oldtime > 3 :
    #    temperature = changeTemp(temperature)
    #    oldtime = time.time()
    #    print(homeinfo)

