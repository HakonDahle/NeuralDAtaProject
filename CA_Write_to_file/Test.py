import os
from multiprocessing import Pool
import random as r
import shutil
import time

liste = [0,1,2,3,4,5,6]
tid = 10
spikes = 22

def create_file(int):
    testliste = []
    for i in range(10):
        testliste = i*2

    process = os.getpid()
    filename = f"process_{process}_iteration_{int}.txt"
    f = open(filename, "w")
    f.write(f"{tid} {spikes}" + '\n')#f"{r.random()}" + '\n')
    f.close()
    return filename
if __name__ == '__main__':
    with Pool(os.cpu_count()-1) as p: #os.cpu_count()-1
            results = p.map(create_file,liste)
            p.close()


    print(results)
    src = results[0]
    dst = f'CA_Write_to_file/{results[0]}'
    new_name = 'CA_Write_to_file/test.txt'
    shutil.copyfile(src,dst)
    time.sleep(5)
    os.rename(src,new_name)
    