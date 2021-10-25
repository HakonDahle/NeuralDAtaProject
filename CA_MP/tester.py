import random as r
import copy

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




def arrayWideSpikeDetectionRate(time,interval):
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

#liste = [[[1,2],[2,2],[3,2],[4,2]],[[10,2],[11,2],[12,2],[13,2],[14,2]]]


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