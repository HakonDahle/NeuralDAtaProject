# Program for organizing data in a list and add features
import matplotlib.pyplot as plt
import numpy as np

# Data for reading the file and putting each line into a list
def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

dense2310 = readFile('data\Dense 2-3-10.spk.txt') # Loads the data