#-----Packets-----#
from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
import csv
from pathlib import Path
from logzero import logger, logfile
import random 

#-----Variables-----#
startTime = datetime.now() #Establishing the start time as the current datatime.now()
nowTime = datetime.now() #Defining the variable that will store the current datatime.now()

#Different colors for LED Matrix
r = (210, 48, 46) #red
blu = (1, 187, 212) #blue
w = (255, 255, 255) #white
bla = (0, 0, 0) #black
br = (120, 84, 72) #brown
o = (255, 151, 0) #orange
p = (244, 143, 177) #pink
g = (72, 68, 68) #grey
ly = (255, 245, 157) #light yellow
dy = (255, 220, 52) #dark yellow

dog = [
    blu, br, blu, blu, blu, blu, blu, br,
    br, br, br, w, w, w, br, br,
    br, br, w, w, w, w, w, br,
    br, br, o, w, w, w, w, br,
    blu, o, bla, o, w, w, bla, w,
    blu, o, bla, o, w, w, bla, w,
    blu, blu, o, w, bla, w, w, blu,
    blu, blu, blu, w, r, w, blu, blu]

cat = [
    blu, g, blu, blu, blu, blu, g, blu,
    g, p, g, blu, blu, g, p, g,
    g, p, w, g, g, w, p, g,
    g, w, w, w, w, w, w, g,
    g, w, bla, w, w, bla, w, g,
    g, w, w, p, p, w, w, g,
    blu, g, w, w, w, w, g, blu,
    blu, blu, g, g, g, g, blu, blu]

rabbit =  [
    ly, ly, blu, blu, blu, ly, ly, blu,
    blu, p, ly, blu, blu, p, blu, blu,
    blu, p, ly, ly, ly, p, blu, blu, 
    blu, ly, ly, ly, ly, ly, blu, blu,
    blu, ly, bla, ly, bla, ly, blu, blu,
    blu, ly, ly, p, ly, ly, blu, blu,
    blu, blu, ly, ly, ly, blu, blu, blu,
    blu, ly, ly, ly, ly, ly, blu, blu]

#Setting up Packets
sense = SenseHat() #Binding the sense data to SenseHat()
sense.clear() #Clears all previous data
sense.set_rotation(270) #LED Matrix rotation by 270 degrees
sense.low_light = True 

def create_csv_file(dataFile):
    with open(dataFile, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Temperature", "Humidity")
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
tempTotal = []
humTotal = []

sense.set_pixels(dog) #Puts dog image for first 10 seconds

#-----Algorithm Analysis-----#

# Establishing every animal's key variables (13 animals)
# First establishes animal name
# Second establishes the animals benefits with 0 or 1 (10 benefits)
# Third establishes temperature, humidity, and weight

animal_identity = [ ["golden", [1,1,1,1,1,1,0,0,0,0],[20,55,27.5]],
["pug", [0,0,0,1,0,0,1,0,0,0],[21,55,7.25]],
["labradoodle", [1,1,0,1,0,0,1,0,0,0],[21,55,22.5]],
["greyhound", [0,0,0,1,1,1,1,0,0,0],[19.5,55,27.5]],
["labradore", [1,1,1,1,1,1,1,0,0,0],[19.5,55,27.5]],
["poodle", [1,0,1,1,1,1,1,1,0,0],[19.5,55,22.5]],
["collie", [1, 1, 0, 1, 1, 1, 1, 1, 0, 0],[19.5,55,17]],
["terrier", [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],[19.5,55,7]],
["sphynx", [0,1,1,0,0,0,0,0,1,1],[25,55,4]],
["persian", [0, 1, 1, 0, 0, 0, 0, 0, 1, 1],[19.5,55,4]],
["rabbit", [1, 1, 0, 1, 0, 1, 1, 0, 0, 0],[18,55,3.9]],
["hamster", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[21,45,.095]],
["easternBox", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[25,60,4]],
["greekTortoise", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[26.5,60,10.5]]]


# This is the function that will produce our ideal combination of animals to send to the ISS,
# based on temp and humidity, then pyschological benefits, and finally lowest weight
def W_Rizz_Match(temp, humidity, animal_identity):
    # Initialize a list to store eligible animals
    eligible_animals = []
   
    # Loop through each animal and check if it's temperature and humidity are within the desired range
    for i in range(len(animal_identity)):
        if abs(temp - animal_identity[i][2][0]) <= 6 and abs(humidity - animal_identity[i][2][1]) <= 10 * humidity:
            eligible_animals.append(animal_identity[i])
   
    #Print a list of the eligible animals for bug fixing purposes (Remove in final draft)
    print("The eligible animals are:",)
    for i in range(len(eligible_animals)):
        print(eligible_animals[i][0])


    #This variable will store the weight and animals in the best list. Weight is set to 1k as the program
    #below needs a predefined weight for topchoice when it is first chosen
    topchoice = (1000,[])
    currentBest = 1
    isBest = False

    # Loop through each combination of eligible animals with a power set: all the possible subsets in a set
    # 2^ of the set length will yield the # of all possible sets.
    for i in range(1, 2**len(eligible_animals)):

        combination = [] #Initializes the list for a combination

        #This will run once for every eligible animal - checks to see if the eligible animal's index corresponds
        #With the number in the for i function. << is a bitwise shift operator
        for j in range(len(eligible_animals)):
            if i & (1 << j): # Compares binary i to binary 1 shifted to the left by j bits (10,100,1000 - only one 1 in the #)
                             # The & compares the corresponding bits of two binary numbers and sees if they are both 1
                             # for example i = 3 (110) and j=1 (10), the 2nd bits are both 1 so it evaluates to true
                combination.append(eligible_animals[j]) #then add it to the list

        total = [0, 0, 0, 0, 0, 0, 0, 0] #Each 0 represents a pro

        #Merging the lists - if animal's pros are not in total then add them
        for i in range(len(combination)):
            for j in range(len(total)):
                if combination[i][1][j] == 1 and total[j] == 0: #For each index
                    total[j] = 1

        print("Current Sum is", sum(total), "versus current best of", currentBest)
        isBest = False
        if sum(total) > currentBest:
            isBest = True

        if sum(total) >= currentBest:
            currentBest = sum(total)
            weight = 0
            final_list = []
            for i in range(len(combination)):
                weight += combination[i][2][2]
                final_list.append(combination[i][0])

            print(f"Another list is: {final_list}\nIt's weight is: {weight}")

            print(isBest)
            if weight < topchoice[0] or isBest:
                topchoice = []
                topchoice.append(weight)
                topchoice.append(final_list)


    return topchoice


while (nowTime < startTime + timedelta(minutes=180)): #Run for 180 minutes

    #Using the sensehat to record data and append it to its respective list
    temp = sense.get_temperature()
    hum = sense.get_humidity()
        
    tempTotal.append(temp)
    humTotal.append(hum)
    
    #Save the data to the file
    data = (counter, datetime.now(), round(temp, 4), round(hum, 4))
    
    add_csv_data(dataFile, data)
    
    #Log event
    logger.info(f"iteration {counter}")
    counter += 1
    
    if counter % 60 == 0: #collecting data every 60 seconds
            
        tempAverage = round(sum(tempTotal)/len(tempTotal), 2)
        humAverage = round(sum(humTotal)/len(humTotal), 2)
        
        if tempAverage > 30: #correcting margin of error in temperature recording
            tempAverage = tempAverage-10

    
        bestList = W_Rizz_Match(tempAverage,humAverage,animal_identity)
        print(f"1. The combined weight of the animals is {bestList[0]} and they are {bestList[1]}")
        
        if humAverage > 25 and humAverage < 45: #correcting margin of error in humidity recording
            humAverage = humAverage+20
        elif humAverage <= 25:
            humAverage = humAverage+40
        
        print(tempAverage)
        print(humAverage)
    
        bestList = W_Rizz_Match(tempAverage,humAverage,animal_identity)
        print(f"2. The combined weight of the animals is {bestList[0]} and they are {bestList[1]}")
        
        tempTotal = [] #Resets this variable after 30 secs
        humTotal = [] #Resets this variable after 30 secs
     
    if counter % 30 == 0: #shows new picture every 30 seconds

        sense.set_pixels(random.choice([dog, cat, rabbit]))

    
    #Recording data per 0.9999 seconds for accuracy
    sleep(0.9999)
    
    #Update current time to restart loop
    nowTime = datetime.now()
