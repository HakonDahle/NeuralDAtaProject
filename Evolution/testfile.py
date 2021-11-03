import random as r
import time



#Oppretter en klasse som kan brukes til å opprette objekt med 
#to parametere, en liste, og en fitness-score
class binary_list:

    list = []
    fit_score = 0

    #Dette er konstruktøren i klassen, som man bruker senere til å opprette objektet
    def __init__ (self, list,fit_score):
        self.list = list
        self.fit_score = fit_score

    '''def get_fit_score():
        return self.fit_score'''

#Metode som sammenligner mål-listen med listen man har
def compare_list(holy_grail, list):
    fit_score = 0
    for i in range(10):
        if holy_grail[i] == list[i]:
            fit_score += 1
    return fit_score

#Metode som muterer listen man sender inn
def mutate_list(list):
    for i in range(len(list)):
        if r.random() <= 0.2:               #her er sannsynligheten for en mutasjon
            if list[i] == 1:
                list[i] = 0
            else:
                list[i] = 1
    return list

#Oppretter en tom startliste, en mål-liste, en mutert tom liste, og en variabel
#som sier hvilken evolusjon man er i, for å se hvor mange evolusjoner man trengte for å komme
#frem til målet
Number_of_lists = 10
bin_list = []
start_list = []
holy_grail = [1,1,1,1,1,1,1,1,1,1]
mutated_list = []
evolution_nr = 0
score = 0
index = 0

#Oppretter startlisten, som man tar utgangspunkt i
for i in range (Number_of_lists):
    for j in range (Number_of_lists):
        if r.random() < 0.5:
            bin_list.append(0)
        else:
            bin_list.append(1)
        #print(bin_list)
    s_list = binary_list(bin_list,0) #Lager et objekt med parametrene startlisten, og en fitnesscore på null(bare for å ha noe)
    s_list.fit_score = compare_list(holy_grail,s_list.list) #Definerer fitness-scoren til listen man startet med, og setter parameteret i objektet.
    start_list.append(s_list)
    print(start_list[i].__dict__)
    bin_list.clear()
    if s_list[i].fit_score > score:
            score = s_list[i].fit_score
            index = i

print("den beste listen er liste nummer",index+1)


