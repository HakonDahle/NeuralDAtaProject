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
Gen13_fit9 = readFile('data\Generation_13_Fitnesscore_9.txt')
Gen8_fit6 = readFile('data\Generation_8_Fitnesscore_6.txt')
fitnesscore_Gen8_fit6 = readFile('data\FitnesscoresCA_11ind_Len_011121_2012.txt')

width = 8   # Number of electrodes in x direction
height = 8  # Number of electrodes in y

t_fasit, data_fasit = datamanagement(dense2310)
t_Gen13_fit9, data_Gen13_fit9 = datamanagement(Gen13_fit9)
t_Gen8_fit6, data_Gen8_fit6 = datamanagement(Gen8_fit6)
 

def electrode_list(activeElectrodes,time):    # Returns a list of timestamps organized for each electrode
    temp_array = []
    temp_electrode = []
    for electrodenr in range(0,60):
        for element in range(len(activeElectrodes)):
            spike = activeElectrodes[element]  # The spiked electrode
            
            if electrodenr == spike:
                temp_electrode.insert(len(temp_electrode),time[element])   # Inserts the timestamp into the column for the electrode
        temp_array.append(temp_electrode[:])    # Adds the electrode column at the end of the list
        temp_electrode.clear()  # Clears the temporary electrode to make it ready for the next
    
    return temp_array   

colors1 = ['C{}'.format(i) for i in range(60)]  # Creates 64 different colors, one for each electrode

electrodes = electrode_list(data_fasit,t_fasit) # Creates the list of electrodes

#plt.eventplot(electrodes, colors=colors1)   # Creates the raster plot



def show_rasterplot(time_from_fasit,data_from_fasit,t1,data1,t2,data2):
    fig = plt.figure(1)
    plt.subplot(311)#(nrows = 2, ncols = 1, sharex=True, sharey = True)
    plt.scatter(time_from_fasit,data_from_fasit,s=0.8,alpha=0.5,c='green')
    plt.title('Dense 2-3-31')
    plt.ylabel('Electrode')
    plt.subplot(312)
    plt.scatter(t1,data1,s=0.8,alpha=0.5,c='red')
    plt.title('Network model, Fitnesscore 9, Weight+=0.05')
    plt.ylabel('Node')
    plt.subplot(313)
    plt.scatter(t2,data2,s=0.8,alpha=0.5,c='red')
    plt.title('Network model, Fitnesscore 6, Weight+=0.05')
    plt.xlabel('Time [s]')
    plt.ylabel('Node')
    plt.show()  # displays the rasterplot

#show_rasterplot(t_fasit,data_fasit,t_Gen13_fit9,data_Gen13_fit9,t_Gen8_fit6,data_Gen8_fit6)

def show_fitnesscores(fitnesscore):
    fig = plt.figure(2)
    plt.plot()
    plt.ylabel('Fitnesscore')
    plt.xlabel('Generation')
    plt.show()

show_fitnesscores(fitnesscore_Gen8_fit6)