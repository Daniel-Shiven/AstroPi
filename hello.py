#-----Packets-----#
from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
from gpiozero import CPUTemperature
import matplotlib.pyplot as plt
import csv
from pathlib import Path
from logzero import logger, logfile

#-----Variables-----#
startTime = datetime.now() #Establishing the start time as the current datatime.now()
nowTime = datetime.now() #Defining the variable that will store the current datatime.now()


#Setting up Packets
sense = SenseHat() #Binding the sense data to SenseHat()
sense.clear() #Clears all previous data
cpu = CPUTemperature()

def create_csv_file(dataFile):
    with open(dataFile, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Temperature", "Humidity", "Pressure")
        writer.writerow(header)

def add_csv_data(dataFile, data):
    with open(dataFile, 'a') as f:
       writer = csv.writer(f)
       writer.writerow(data)

baseFolder = Path(__file__).parent.resolve()

#Set up log file
logfile(baseFolder/"events.log")

#Initialise the CSV file
dataFile = baseFolder/"data.csv"
create_csv_file(dataFile)

counter = 1

while (nowTime < startTime + timedelta(minutes=1)): #Run for 60 seconds

    #Using the sensehat to record data and append it to its respective list
    pres = sense.get_pressure()
    temp = sense.get_temperature()
    hum = sense.get_humidity()
    
    #Save the data to the file
    data = (counter, datetime.now(), round(pres, 4), round(temp, 4), round(hum, 4))
    
    add_csv_data(dataFile, data)
    
#     st, ct = [], []
# 
#     st.append(sense.temperature)
#     ct.append(cpu.temperature)
#         
#     plt.plot(st)
#     plt.plot(ct)
#     plt.legend(['SenseHat Temp'], ['CPU Temp'], loc = 'upper left')
#     plt.show()
    
    #Log event
    logger.info(f"iteration {counter}")
    counter += 1
    
    #Recording data per 0.9999 seconds for accuracy
    sleep(0.9999)
    
    #Update current time to restart loop
    nowTime = datetime.now()



