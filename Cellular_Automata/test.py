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

