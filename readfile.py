import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
RADIATOR_PIN = 16
GPIO.setup(RADIATOR_PIN, GPIO.OUT)
GPIO.output(RADIATOR_PIN, 0)

import pandas as pd
import time

oldtime = time.time() 

homeinfo = pd.read_csv('rad-data.csv')
homelogs = pd.DataFrame(columns=['Time', 'Temperature', 'Humidity'])
print(homeinfo)

#set variables to the first line of data in the file
temperature = homeinfo['temperature'].values[0]
thermostat = homeinfo['thermostat'].values[0]

radiatorOn = False

def getTemperature():
    sensorHumidity, sensorTemp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if sensorHumidity is not None and sensorTemp is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(sensorTemp, sensorHumidity))
    else:
        print("Failed to retrieve data from humidity sensor")

    homeinfo.at[0, 'temperature'] = temperature #replace temperature in the first line of file with measured temp
    homeinfo.to_csv('rad-data.csv', index=False)

    return sensorTemp 

def setRadiatorPower():
    if temperature < thermostat :
        GPIO.output(RADIATOR_PIN, 1)
        return True
    if temperature >= thermostat :
        GPIO.output(RADIATOR_PIN, 0)
        return False

def writeLogs():
    homelogs.at[0, 'Time'] = time.time()
    homelogs.at[0, 'Temperature'] = temperature
    homelogs.at[0, 'Humidity'] = humidity

    with open('rad-logs.csv', 'a') as f:
        pd.to_csv(homelogs, header=False)

while True:
    temperature = getTemperature()
    print("temperature = " + str(temperature))
    radiatorOn = setRadiatorPower()
    print(radiatorOn)
    writeLogs()
