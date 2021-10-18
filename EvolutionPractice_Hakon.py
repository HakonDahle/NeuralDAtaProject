# 1. Make 10 random binary strings with 10 bits
# 2. compare them to the target (fitness funtion)
# 3. Take the most promising candidate and make a new population of 10 children.
# 4. Apply evelution to the children.
# 5. Send the children through the fitness function)
# 6. Repeat

import numpy as np
import random as rand
import time

target = [1]*10    #List version

# Creating the random start population
def init_population():
    pop = [0]*10  # Population
    for i in range (0,10):
        ind = [0]*10    # One individual of the population
        for n in range (0,10):
            if rand.random() <= 0.2:
                ind[n] = 1  # Assigning 10 random bits of 0/1
        pop[i] = ind
    return pop

# function finds the best match between the individuals of the population and the target by matching their bits.
def fitnessmodel(answer,candidate): 
    fitmax = 0  # initial fitness score
    fittest = [0]*10    # initial best match

    for i in range (0,10):  # Iterates through the individuals
        fitcount = 0    # resets fitnesscore for each iteration
        for n in range(0,10):   # Iterates through the bits of each individual
            if candidate[i][n] == answer[n]:    # Fitnesscore is accumulated if the bits are matching the target
                fitcount += 1
        if fitcount > fitmax:   # Updates if a better match and fitnesscore is found
            fitmax = fitcount
            fittest = candidate[i]
    return fittest, fitmax  # returns the best match and the fitnesscore

# Function that creates 10 children which might mutate
def evolution(ancestor):    
    children = []   # List that will contain the new generation
    for i in range(0,10):
        inherent = ancestor[0][:]   # copies the parent
        for n in range(0,10):
            prob = rand.random()    # Probability of a mutation
            if prob <= 0.05:    # mutation of the child
                if inherent[n] == 0:
                    inherent[n] = 1
                    continue
                elif inherent[n] == 1:
                    inherent[n] = 0
                    continue
        children.append(inherent)   # Adding the children to the new generation
    return children

# Initiate
population = init_population()  # Generating the first random population, Generation 0

# Observe and update
if target not in population:   # Checks if the population contains an individual equal to the target
    generationNr = 0    # Counts number of generations
    parent = fitnessmodel(target,population)   # Best match from the fitnessmodel
    child = evolution(parent)   # The child is a mutation of its parent
    
    while (parent[0] != child) and parent[1] < 10:  # Continously finding the closest match and evolving the children to the next generation
        parent = fitnessmodel(target,child)   
        child = evolution(parent)
        print("best match: ",parent[0], "fitnessore: ",parent[1])
        generationNr += 1
        #time.sleep(1)
print("Your evolutionary algorithm has completed, and it took",generationNr,"generations for it to complete.")
