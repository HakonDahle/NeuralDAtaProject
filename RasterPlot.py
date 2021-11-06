# Program for organizing data in a list and add features
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import itertools as iter
import numpy as np
import ListsAndFeatures as LaF
import networkx as nx

"""
DATA MANAGEMENT AND LOADING
"""

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
Gen13_fit9 = readFile('data\Phenotype\Generation_13_Fitnesscore_9.txt') # CA_11ind_Len_Weight05_031121__1216
Gen8_fit6 = readFile('data\Phenotype\Generation_8_Fitnesscore_6.txt')   # CA_11ind_Len_Weight05_011121_2012
Gen25_fit6362 = readFile('data\Phenotype\Generation_24_Fitnesscore_6362.txt') # CA_11ind_Len_Noweight_021121_0939
Gen25_fit22 = readFile('data\Phenotype\Generation_24_Fitnesscore_22.txt')   # CA_11ind_Len_Genweight_041121_2006
Gen23_fit291 = readFile('data\Phenotype\Generation_23_Fitnesscore_291.txt')   # CA_11ind_Len_Genweight_041121_0107

fitnesscore_Gen8_fit6 = readFile('data\Fitnesscores\FitnesscoresCA_11ind_Len_011121_2012.txt')
fitnesscore_Gen13_fit9 = readFile('data\Fitnesscores\FitnesscoresCA_11ind_Len_031121__1216.txt')
fitnesscore_Gen25_fit6362 =readFile('data\Fitnesscores\FitnesscoresCA_11ind_Len_Noweight_021121_0939.txt')
fitnesscore_Gen14_fit14371 = readFile('data\Fitnesscores\FitnesscoresCA_7ind_Len_noweights_021121_0940.txt')
fitnesscore_Gen23_fit291 = readFile('data\Fitnesscores\FitnesscoresCA_11ind_Len_Genweight_041121_0107.txt')
fitnesscore_Gen25_fit22 = readFile('data\Fitnesscores\FitnesscoresCA_11ind_Len_GenWeight_041121_2006.txt')


t_fasit, data_fasit = datamanagement(dense2310)
t_Gen13_fit9, data_Gen13_fit9 = datamanagement(Gen13_fit9)
t_Gen8_fit6, data_Gen8_fit6 = datamanagement(Gen8_fit6)
t_Gen25_fit6362, data_Gen25_fit6362 = datamanagement(Gen25_fit6362)
t_Gen23_fit291, data_Gen23_fit291 = datamanagement(Gen23_fit291)
t_Gen25_fit22, data_Gen25_fit22 = datamanagement(Gen25_fit22)

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

"""
Scatter plot
"""

def show_rasterplot1(time_from_fasit,data_from_fasit,t1,data1):
    fig = plt.figure(1)
    ax = plt.subplot(211)#(nrows = 2, ncols = 1, sharex=True, sharey = True)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.scatter(time_from_fasit,data_from_fasit,s=0.8,alpha=0.5,c='green')
    plt.title('Reference data: Dense 2-3-31',size=32, fontweight="bold")
    plt.ylabel('Electrode',size=30)
    ax = plt.subplot(212)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.scatter(t1,data1,s=0.8,alpha=0.5,c='red')
    plt.title('Network model: Fitnesscore 9, Weight+=0.05',size=32, fontweight="bold")
    plt.ylabel('Node',size=30)
    plt.xlabel('Time [s]',size=30)
    plt.show()  # displays the rasterplot

def show_rasterplot2(time_from_fasit,data_from_fasit,t1,data1,t2,data2):
    fig = plt.figure(2)
    ax = plt.subplot(311)#(nrows = 2, ncols = 1, sharex=True, sharey = True)
    ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.scatter(time_from_fasit,data_from_fasit,s=0.8,alpha=0.5,c='red')
    plt.title('Network model: Fitnesscore 6362, Unweighted',size=30,fontweight="bold")
    plt.ylabel('Electrode',size=30)
    ax = plt.subplot(312)
    ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.scatter(t1,data1,s=0.8,alpha=0.5,c='red')
    plt.title('Network model, Fitnesscore 6, Weight+=0.05',size=30,fontweight="bold")
    plt.ylabel('Node',size=30)
    ax = plt.subplot(313)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.scatter(t2,data2,s=0.8,alpha=0.5,c='red')
    plt.title('Network model, Fitnesscore 22, Weight in genotype',size=30,fontweight="bold")
    plt.xlabel('Time [s]',size=30)
    plt.ylabel('Node',size=30)
    plt.show()  # displays the rasterplot

#show_rasterplot1(t_fasit,data_fasit,t_Gen13_fit9,data_Gen13_fit9,t_Gen8_fit6,data_Gen8_fit6)
#show_rasterplot2(t_Gen25_fit6362, data_Gen25_fit6362,t_Gen8_fit6, data_Gen8_fit6,t_Gen25_fit22, data_Gen25_fit22)

"""
Fitnesscores
"""

def show_fitnesscores(fitnesscores):
    #fitnesscores = locals()
    fig, ax = plt.subplots()
    maxx = 0
    maxy = 0


    for i in range(len(fitnesscores)):
        for j in range(len(fitnesscores[i])):
            fitnesscores[i][j] = int(fitnesscores[i][j])
    
    blue_line = mlines.Line2D([], [], color='blue', label='Spike triggered increment of 0.05)')
    green_line = mlines.Line2D([], [], color='green', label='Unweighted')
    green_dotted = mlines.Line2D([], [], color='green',ls='--', label='Unweighted (pop.size 7)')
    red_line = mlines.Line2D([], [], color='red', label='Genotype', )
    
    #ax.tick_params(axis='both', which='major', labelsize=20)
    plt.plot(fitnesscores[0],color='blue')  # CA_11ind_Len_weight+05
    plt.plot(fitnesscores[1],color='blue')  # CA_11ind_Len_weight+05
    plt.plot(fitnesscores[2],color='green') # CA_11ind_Len_noweight
    plt.plot(fitnesscores[3],label='Population size 7',color='green',ls='--') # CA_7ind_Len_noweight
    plt.plot(fitnesscores[4],color='red')   # CA_11ind_Len_Genweight
    plt.plot(fitnesscores[5],color='red')
    plt.legend(handles=[blue_line,green_line,green_dotted,red_line],loc='upper right') # ,prop={'size': 22}
    plt.ylabel('Fitnesscore')   # ,size=26
    plt.xlabel('Generation')    # , size=26
    plt.title('Weights\' impact on Fitnesscores',fontweight="bold") # , size=34
    #plt.ylim(0,maxy)
    #plt.xlim(0,maxx)
    plt.show()

maxlength = max(len(fitnesscore_Gen13_fit9),len(fitnesscore_Gen8_fit6),len(fitnesscore_Gen25_fit6362),len(fitnesscore_Gen14_fit14371),len(fitnesscore_Gen23_fit291),len(fitnesscore_Gen25_fit22))

if len(fitnesscore_Gen13_fit9) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen13_fit9)):
        fitnesscore_Gen13_fit9.append(fitnesscore_Gen13_fit9[-1])

if len(fitnesscore_Gen8_fit6) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen8_fit6)):
        fitnesscore_Gen8_fit6.append(fitnesscore_Gen8_fit6[-1])

if len(fitnesscore_Gen25_fit6362) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen25_fit6362)):
        fitnesscore_Gen25_fit6362.append(fitnesscore_Gen25_fit6362[-1])

if len(fitnesscore_Gen14_fit14371) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen14_fit14371)):
        fitnesscore_Gen14_fit14371.append(fitnesscore_Gen14_fit14371[-1])

if len(fitnesscore_Gen23_fit291) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen23_fit291)):
        fitnesscore_Gen23_fit291.append(fitnesscore_Gen23_fit291[-1])

if len(fitnesscore_Gen25_fit22) < maxlength:
    for _ in range(maxlength-len(fitnesscore_Gen25_fit22)):
        fitnesscore_Gen25_fit22.append(fitnesscore_Gen25_fit22[-1])

fitnesscores = []
fitnesscores.append(fitnesscore_Gen8_fit6)
fitnesscores.append(fitnesscore_Gen13_fit9)
fitnesscores.append(fitnesscore_Gen25_fit6362)
fitnesscores.append(fitnesscore_Gen14_fit14371)
fitnesscores.append(fitnesscore_Gen23_fit291)
fitnesscores.append(fitnesscore_Gen25_fit22)

fitnesscores.sort(key=len)

show_fitnesscores(fitnesscores)

"""
ASDR
"""

# Calculates fire rate for the whole electrode array (spikes/t)
def ArrayWideSpikeDetectionRate(time):
    t0 = 0 
    t1 = time[:]
    f = []
    interval = 1
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
    

def show_ASDR_result(ASDR_Gen,ASDR_Comp1):    
    fig = plt.figure(4)
    ax = plt.subplot(211)
    #ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.plot(ASDR_Gen)
    plt.ylabel('ASDR', size=30)
    plt.title('ASDR Reference data', size=40,fontweight="bold")

    ax = plt.subplot(212)
    #ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.plot(ASDR_Comp1)
    plt.ylabel('ASDR', size=30)
    plt.xlabel('Time[s]', size=30)
    plt.title('ASDR generated data', size=40,fontweight="bold")

    '''ax = plt.subplot(313)
    ax.tick_params(axis='both', which='major', labelsize=26)
    plt.plot(ASDR_Comp2)
    plt.ylabel('ASDR', size=30)
    plt.xlabel('Time[s]', size=30)
    plt.title('ASDR Weight in genotype', size=40,fontweight="bold")'''
    plt.show()

def show_ASDR_discussion(ASDR_Gen,ASDR_Comp1,ASDR_Comp2):
    pfig = plt.figure()
    ax = plt.subplot()
    ax.tick_params(axis='both', which='major', labelsize=26)

    plt.plot(ASDR_Gen)
    plt.plot(ASDR_Comp1)
    plt.plot(ASDR_Comp2)
    plt.title('ASDR Comparison', size=40)
    plt.ylabel('ASDR', size=30)
    plt.xlabel('Time [s]', size=30)
    plt.show()

ASDR_Gen13_fit9 = ArrayWideSpikeDetectionRate(t_Gen13_fit9)
ASDR_data = ArrayWideSpikeDetectionRate(t_fasit)
ASDR_Gen8_fit6 = ArrayWideSpikeDetectionRate(t_Gen8_fit6)
ASDR_Gen25_fit6362 = ArrayWideSpikeDetectionRate(t_Gen25_fit6362)
ASDR_Gen25_fit22 = ArrayWideSpikeDetectionRate(t_Gen25_fit22)

#show_ASDR_result(ASDR_data,ASDR_Gen8_fit6)    
#show_ASDR_discussion(ASDR_Gen8_fit6,ASDR_Gen25_fit6362,ASDR_Gen25_fit22)