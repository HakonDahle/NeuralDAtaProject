
import matplotlib as plt
import numpy as np
import pycxsimulator
from pylab import *


# Data for reading the file and putting each line into a list.
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

# Function for finding which step (sample number) the data or time is
def stepp(list,element):
    step = list.index(str(element))
    return step



dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data
t = [i.split()[0] for i in dense2310][:]    # Copies the data list and stores the time into a separate list
data = [i.split()[1] for i in dense2310][:] # Copies the data list and stores the data into a separate list
width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y


# Creates the electrode array with no spiked electrodes as initial state
def initialize():
    global time, config, nextConfig

    time = 0

    config = zeros([height, width])
    nextConfig = zeros([height, width])



def observe():
    cla()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    axis('image')
    title('t = ' + str(time))



def update():
    global time, config, nextConfig

    spike = int(data[time][:])  # The spiked electrode

    for y in range(width):
        for x in range(height):
            
            state = config[y, x]    # Acquires the state of the electrode

            if spike == x+(y*8):    # if the spike value and position of x and y correlates the state is set to 1
                state = 1
            else:   # in any other cases the value for the electrode is 0
                state = 0
            nextConfig[y,x] = state # updates the next status of the electrode array

    time += 1

    config, nextConfig = nextConfig, config

pycxsimulator.GUI().start(func=[initialize, observe, update])
