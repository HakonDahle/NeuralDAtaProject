# Program for organizing data in a list and add features
import matplotlib as plt
import numpy as np

# Data for reading the file and putting each line into a list
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

dense2310 = readFile('C:\Dense 2-3-10.spk.txt') # Loads the data
t = [i.split()[0] for i in dense2310][:]    # Copies the data list and stores the time into a separate list
data = [i.split()[1] for i in dense2310][:] # Copies the data list and stores the data into a separate list
width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y


def electrode_list(activeElectrodes,ti):
    temp_array = []
    temp_electrode = []
    for electrodenr in range(0,64):
        for element in range(len(activeElectrodes)):
            spike = int(activeElectrodes[element][:])  # The spiked electrode
            
            if electrodenr == spike:
                temp_electrode.append([element,ti[element]])
        temp_array.append(temp_electrode[:])
        temp_electrode.clear()
    
    return temp_array

electrodes = electrode_list(data,t)
print("electrodes[0]: ",electrodes[0][0][1])
