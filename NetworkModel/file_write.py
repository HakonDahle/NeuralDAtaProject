import os
import time
import multiprocessing as multi

def generate_pheno_file(trial_nr,generation_nr, trial_name,current_process_name):
    current_process = multi.current_process()
    file_path = 'NetworkModel\\data\\temporary data\\' + str(trial_name) + '\\' + str(trial_nr)+'\\Generation'+str(generation_nr)   #Path to file location
    file_name = 'Phenotype for '+str(current_process_name)+', Generation_'+str(generation_nr)+'.txt'  # Naming the file according to generation and fitnesscore
    
    
    full_path = os.path.join(file_path, file_name)
    

    #Making sure directory exists and file
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
    if not os.path.isfile(full_path):
        file = open(full_path, 'w')
        #fitness.writelines(["Time", "\t", "Electrode", "\n"])
        file.close()
    return full_path

def write_pheno_file(full_path,pheno_type):    
    #File management    
    file = open(full_path, 'a')
    #HRfile.writelines(HR)
    for element in pheno_type:
        file.writelines([str(element[0])," ", str(element[1]), "\n"])
        #f.write(str(element[0]) + " " + str(element[1]) + '\n')
    file.close()

    
    

def fitness_file(fitness_score,generation_nr,trial_name,trial_nr):
    filepath = 'data\\Results\\' + str(trial_name) + '\\' + str(trial_nr)   #Path to file location
    filename = 'Fitnesscores.txt'

    fullpath = os.path.join(filepath, filename)

    #Making sure directory exists and file
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    if not os.path.isfile(fullpath):
        fitnessfile = open(fullpath, 'w')
        #fitness.writelines(["Time", "\t", "Electrode", "\n"])
        fitnessfile.close()

    file = open(fullpath,"a")
    file.writelines("Generation: ",generation_nr,str(fitness_score),"\n")
    file.close()

    return fullpath