from multiprocessing.context import Process
import random as r
import copy
import multiprocessing
from functools import partial
import time


'''liste = [1,2,3]
var1 = 56
var2 = [[1,2,3],[10,11,12]]

var_list = []
var_list.append(liste)
var_list.append(var1)
var_list.append(var2)
for obj in var_list:

    print(obj)'''
'''liste = []
#Score
t0 = time.perf_counter()
for i in range(100):
    liste.append(r.randint(0,63))
t3 = time.perf_counter()
print(f'Finished in {t3-t0} seconds')
t1 = time.perf_counter()
liste.sort()
t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')
#print(liste)
score = 0
for i in range(64):
    try:
        index = liste.index(i)
        del liste[:index]
        print(index)
    except ValueError:
        print(f"inneholder ikke tallet {i}")
        score += 5000
print(score)
#print(liste)'''


'''def pluss(a,b,c):
    ans = a+b-c
    return ans

partial_pluss = partial(pluss,b=1, c=2)
ans = partial_pluss(10)
print(ans)'''


'''if __name__ == '__main__':

    for i in range(10):
        p = Process(target=pluss,args=(i,10))
        p.start()
        processlist = []
        processlist.append(p)
    

    for process in processlist:
        p.join()
        svarliste = []
        svarliste.append(p)
    print(svarliste)
'''

'''random_list = []
for i in range(1000):

    random_list.append(r.uniform(0,200))

random_list.sort()
num_n = []
liste = []
for i in range(200):
    for num in random_list:
        if num > i and i+1 > num:
            num_n.append(num)
    #print(num_n)
    nummer = copy.deepcopy(num_n)
    liste.append(nummer)
    num_n.clear()

for i in range (200):
    if len(liste[i]) == 0:
        print(f"det er ingen tall som begynner med {i}")
'''

'''time = 0
spikes = []
ny_liste = []

while time < 2:
    spikes_info = spikes[:]
    for i in range(3):
        spikes_info.append(r.randint(0,5))
    for i in range(len(spikes_info)):
        ny_liste.append([time,spikes_info[i]])
    time += 0.5
    spikes_info.clear()


print(spikes_info)



print(ny_liste)
'''




'''def arrayWideSpikeDetectionRate(time,interval):
    t0 = 0 
    t1 = time[:]
    f = []
    #interval = 0.1
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
'''
'''def ArrayWideSpikeDetectionRate(time):
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
    return f'''
'''
liste = [[1,2],[2,2],[3,2],[4,2],[10,2],[11,2],[12,2],[13,2],[14,2]]
for index in range(len(liste)):
    print(liste[index][0])
'''

def test_oppdeling(liste,interval):
    tid = []
    tid_regler = []
    #print(f"liste er {len(liste)} lang") 
    for i in range(len(liste)):
        for j in range(len(liste[i])):
            #print(f"halåå{liste[i][j][0]}")
            tid.append([liste[i][j][0]])
        tider = copy.deepcopy(tid)
        tid_regler.append(tider)
        tid.clear()
    return tid_regler


#print(f"liste er {len(liste)} lang")  

'''liste = test_oppdeling(liste,10)
for obj in liste:
    print(obj)
'''