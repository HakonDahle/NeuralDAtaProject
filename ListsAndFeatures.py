# Program for organizing data in a list and add features
import matplotlib as plt
import numpy as np

# Data for reading the file and putting each line into a list
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data
t = [float(i.split()[0]) for i in dense2310][:]    # Copies the data list and stores the time into a separate list
data = [int(i.split()[1]) for i in dense2310][:] # Copies the data list and stores the data into a separate list
width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y


# Makes a list of each spike sorted for each electrode which stores the step nr. and time stamp
def electrode_list(activeElectrodes,ti):
    temp_array = []
    temp_electrode = []
    for electrodenr in range(0,64):
        for element in range(len(activeElectrodes)):
            spike = activeElectrodes[element]  # The spiked electrode
            if electrodenr == spike:
                temp_electrode.append([element,float(ti[element])])
        temp_array.append(temp_electrode[:])
        temp_electrode.clear()
    
    return temp_array

electrodes = electrode_list(data,t)

# Calculates fire rate for the whole electrode array (spikes/t)
def ArrayWideSpikeDetectionRate(ti):
    n = 100 # number of spikes
    element = 0 # Used to keep control of which elements have been checked
    rate = n/(ti[element+(n-1)]-ti[element])
    print("ti[element+(n-1)] = ",ti[element+(n-1)], "ti[element]: ",ti[element],"ti[element+(n-1)]-ti[element]: ",ti[element+(n-1)]-ti[element])
    print("rate1: ",rate)
    element = n
    rate = n/(ti[element+(n-1)]-ti[element])
    print("ti[element+(n-1)] = ",ti[element+(n-1)], "ti[element]: ",ti[element],"ti[element+(n-1)]-ti[element]: ",ti[element+(n-1)]-ti[element])
    print("rate2: ",rate)
    element = 200
    rate = n/(ti[element+(n-1)]-ti[element])
    print("ti[element+(n-1)] = ",ti[element+(n-1)], "ti[element]: ",ti[element],"ti[element+(n-1)]-ti[element]: ",ti[element+(n-1)]-ti[element])
    print("rate3: ",rate)
    element = 300
    rate = n/(ti[element+(n-1)]-ti[element])
    print("ti[element+(n-1)] = ",ti[element+(n-1)], "ti[element]: ",ti[element],"ti[element+(n-1)]-ti[element]: ",ti[element+(n-1)]-ti[element])
    print("rate4: ",rate)
ASDR = ArrayWideSpikeDetectionRate(t)
