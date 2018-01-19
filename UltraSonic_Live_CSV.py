import matplotlib.pyplot as plt
import matplotlib.animation as anime
import matplotlib.style as style
import RPi.GPIO as GPIO
import time
import csv

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

with open("Distance Data", 'w') as clrFile: #Clear the existing data in the file and add headers
    clearFile = csv.writer(clrFile)
    clearFile.writerow(['Timestamp (in sec)', 'Data (in CM)'])

trigPin = 17
echoPin = 18

GPIO.setup(trigPin, GPIO.OUT)
GPIO.output(trigPin, GPIO.LOW)

GPIO.setup(echoPin, GPIO.IN)

style.use('fivethirtyeight')
fig = plt.figure()
sp = fig.add_subplot(1,1,1)

c = 340*100 #Speed of light in CM/s

x = []
y = []

t_start = time.time()

def get_data(data):

    '''the delay between each measurement must be at least 60 milliseconds, done in FuncAnimation interval'''

    GPIO.output(trigPin, GPIO.HIGH) #Start sending dignal to trigger
    time.sleep(10*(10**-6)) #Data sheet says signal must be 10 microseconds
    GPIO.output(trigPin, GPIO.LOW) #end signal

    while GPIO.input(echoPin) == GPIO.LOW:  #echo pin in low state
        pass    #do nothing. This will repeat until echo pin is in high state

    start = time.time() #get the time in which the pin start a high state

    while GPIO.input(echoPin) == GPIO.HIGH: #echo pin in high state
        pass    #do nothing. this will repeat until echo pin is in a low state

    stop = time.time()  #get the time when the pin stops its low state

    duration = stop - start

    data = (duration*c)/2   #equation given by datasheet. basically time *speed of sound. divided by two because the sound travels to and from the object.

    timeStamp = stop - t_start
    print data

    y.append(data)

    x.append(timeStamp)

    with open("Distance Data", 'a') as csvFile: #'a' is to append 
        fileWrite = csv.writer(csvFile) #now we can use the variable "exampleWrite" in place of this function
        fileWrite.writerow([timeStamp, data])

    csvFile.close()

    if len(x) > 100:    #to ensure the list does't get too big
        x.remove(x[0])
        y.remove(y[0])

    sp.scatter(x,y, label = 'Distance', s = 20, color = 'blue')

graph = anime.FuncAnimation(fig, get_data, interval = 60) #interval >= 60 milliseconds

plt.title('UltraSonic Sensor Data')
plt.xlabel('Time Since Start in Seconds')
plt.ylabel('Distance in CM')
plt.legend()
plt.show()

'''
    add an interrupt to stop code?
    
'''

