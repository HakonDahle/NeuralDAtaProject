import random as r

time = 0
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





def ArrayWideSpikeDetectionRate(time):
    t0 = 0 
    t1 = time[:]
    f = []
    interval = 0.1
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
