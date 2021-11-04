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

def datamanagement(datalist):
    time = [float(i.split()[0]) for i in datalist][:]    # Copies the data list and stores the time into a separate list
    spikes = [int(i.split()[1]) for i in datalist][:] # Copies the data list and stores the data into a separate list
    if time[-1] > 1800:
        del (time[next(x[0] for x in enumerate(time) if x[1] > 30*60):]) # clears all samples above 30 min
        del (spikes[len(time):]) # clears all samples above 30 min
    return time, spikes

dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data
sparse7231 = readFile('data\Dense 2-3-10.spk.txt')
best_spikes = readFile('CA_Write_to_file/Test_Results/03_11_2021__12_46_18/Generation_11_FitScore_2501.txt')
fitness_score = readFile('CA_Write_to_file/Test_Results/03_11_2021__14_02_05/Fitness_score.txt')

width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y

t, data = datamanagement(best_spikes)

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

fitness_list = []
for i in range(len(fitness_score)):
    fitness_list.append([i,int(fitness_score[i])])
print(fitness_list)

colors1 = ['C{}'.format(i) for i in range(64)]  # Creates 64 different colors, one for each electrode

electrodes = electrode_list(data,t) # Creates the list of electrodes

plt.eventplot(electrodes, colors=colors1)   # Creates the raster plot
plt.show()  # displays the rasterplot
plt.plot(fitness_list)
plt.show()