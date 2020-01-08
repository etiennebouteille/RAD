import pandas as pd

time = 0

homeinfo = pd.read_csv('rad-data.csv')
print(homeinfo)

#set variables to the first line of data in the file
temperature = homeinfo['temperature'].values[0]
thermostat = homeinfo['thermostat'].values[0]

def getTemperature():
    #TODO: use temperature sensor
    homeinfo.set_value(0, 'temperature', 10) #replace temperature in the first line of file with measured temp
    return 10

def setRadiatorPower():
    if temperature < thermostat :
        radiatorOn = True
    if temperature >= thermostat :
        radiatorOn = False

while True:
    getTemperature()
    setRadiatorPower()
    print('thermostat = %s, temperature = %s' % (thermostat, temperature))
    time += 1

