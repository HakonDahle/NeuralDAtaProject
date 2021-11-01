# Program for organizing data in a list and add features


# Data for reading the file and putting each line into a list
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data

t = []
data = []

def datamanagement(datalist):
    time = [float(i.split()[0]) for i in datalist][:]    # Copies the data list and stores the time into a separate list
    spikes = [int(i.split()[1]) for i in datalist][:] # Copies the data list and stores the data into a separate list
    if time[-1] > 1800:
        del (time[next(x[0] for x in enumerate(time) if x[1] > 30*60):]) # clears all samples above 30 min
        del (spikes[len(time):]) # clears all samples above 30 min
    return time, spikes


def get_data():
    t, data = datamanagement(dense2310)
    return data

def get_time():
    t, data = datamanagement(dense2310)
    return t

