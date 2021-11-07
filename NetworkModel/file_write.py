import os
import time
import multiprocessing as multi

# Permanent storage of spike data into a file   
def phenotype_file(fitness_score,generation_nr,trial_name,trial_nr,best_match,pheno_type):    
    file_path = 'data\\Results\\' + str(trial_name) + '\\' + str(trial_nr)   #Path to file location
    file_name = 'Generation_'+str(generation_nr)+'_Fitnesscore_'+str(fitness_score)+'.txt'  # Naming the file according to generation and fitnesscore
    
    # Joining path and filename into a single string
    full_path = os.path.join(file_path, file_name)
    
    #Making sure directory and file exists 
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
    if not os.path.isfile(full_path):
        file = open(full_path, 'w')
        file.close()

    # Adding data to the file   
    file = open(full_path, 'a')
    for element in pheno_type[best_match]:
        file.writelines([str(element[0])," ", str(element[1]), "\n"])
    file.close()

# Permanent storage of fitness scores into a file 
def fitness_file(fitness_score,generation_nr,trial_name,trial_nr):
    filepath = 'data\\Results\\' + str(trial_name) + '\\' + str(trial_nr)   #Path to file location
    filename = 'Fitnesscores.txt'

    # Joining path and filename into a single string
    fullpath = os.path.join(filepath, filename)

    #Making sure directory exists and file
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    if not os.path.isfile(fullpath):
        fitnessfile = open(fullpath, 'w')
        fitnessfile.close()

    # Adding data to the file
    file = open(fullpath,"a")
    file.writelines([str(fitness_score),"\n"])
    file.close()