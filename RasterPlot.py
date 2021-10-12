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
t = [float(i.split()[0]) for i in dense2310][:]    # Copies the data list and stores the time into a separate list
data = [int(i.split()[1]) for i in dense2310][:] # Copies the data list and stores the data into a separate list
width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y


def electrode_list(activeElectrodes,time):    # Returns a list of timestamps organized for each electrode
    temp_array = []
    temp_electrode = []
    for electrodenr in range(0,64):
        for element in range(len(activeElectrodes)):
            spike = activeElectrodes[element]  # The spiked electrode
            
            if electrodenr == spike:
                temp_electrode.insert(len(temp_electrode),time[element])   # Inserts the timestamp into the column for the electrode
        temp_array.append(temp_electrode[:])    # Adds the electrode column at the end of the list
        temp_electrode.clear()  # Clears the temporary electrode to make it ready for the next
    
    return temp_array   

colors1 = ['C{}'.format(i) for i in range(64)]  # Creates 64 different colors, one for each electrode

electrodes = electrode_list(data,t) # Creates the list of electrodes

plt.eventplot(electrodes, colors=colors1)   # Creates the raster plot
plt.show()  # displays the rasterplot