# Program for organizing data in a list and add features
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Data for reading the file and putting each line into a list
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data
sparse7231 = readFile('data\Sparse 7-2-31.spk.txt')
t = []
data = []

def datamanagement(datalist):
    time = [float(i.split()[0]) for i in datalist][:]    # Copies the data list and stores the time into a separate list
    spikes = [int(i.split()[1]) for i in datalist][:] # Copies the data list and stores the data into a separate list
    if time[-1] > 1800:
        del (time[next(x[0] for x in enumerate(time) if x[1] > 30*60):]) # clears all samples above 30 min
        del (spikes[len(time):]) # clears all samples above 30 min
    return time, spikes
width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y

t, data = datamanagement(sparse7231)


# Makes a list of each spike sorted for each electrode which stores the step nr. and time stamp
def electrode_list(activeElectrodes,time):
    temp_array = []
    temp_electrode = []
    for electrodenr in range(0,64):
        for element in range(len(activeElectrodes)):
            spike = activeElectrodes[element]  # The spiked electrode
            if electrodenr == spike:
                temp_electrode.append([element,time[element]])
        temp_array.append(temp_electrode[:])
        temp_electrode.clear()
    
    return temp_array

electrodes = electrode_list(data,t)


# Calculates fire rate for the whole electrode array (spikes/t)
def ArrayWideSpikeDetectionRate(time):
    t0 = 0 
    t1 = time[:]
    f = []
    interval = 0.1
    spikes = 0   # number of spikes
    for element in range(len(time)):
        if t1[element] - t0 <= interval:
            spikes += 1
            #print("IF: element: ",element,"spikes: ",spikes)
        elif t1[element] - t0 > interval:
            f.append(spikes/(t1[element]-t0))
            t0 = t1[element]
            spikes = 0
    return f
    
ASDR = ArrayWideSpikeDetectionRate(t)


plt.plot(data[0:1000])
plt.show()
'''
plt.plot(ASDR[:len(ASDR)-1])
plt.show()
'''
