import random as r
import time

class BinaryList:

    best_score = 0

    def __init__ (self, list,fit_score):
        self.list = list
        self.fit_score = fit_score

    def update_best_score(x):
        best_score = x

    def get_fit_score(self):
        return self.fit_score

    def show(self):
        print(f"list: {self.list}, fitness-score: {self.fit_score}")

def compare_list(holy_grail, list):
    fit_score = 0
    for i in range(10):
        if holy_grail[i] == list[i]:
            fit_score += 1
    return fit_score

def mutate_list(list):
    for i in range(len(list)):
        if r.random() <= 0.2:         
            if list[i] == 1:
                list[i] = 0
            else:
                list[i] = 1
    return list

def create_n_BinaryList_objects(n):
    bin_list = []
    evolution_list = []
    for i in range (n):
        for j in range (n):
            if r.random() < 0.5:
                bin_list.append(0)
            else:
                bin_list.append(1)
        BinaryList_object = BinaryList(bin_list,0) 
        BinaryList_object.fit_score = compare_list(holy_grail,BinaryList_object.list) 
        #BinaryList_object.show()
        evolution_list.append(BinaryList_object)
        bin_list.clear()
        print(evolution_list[i])
        
holy_grail = [1,1,1,1,1,1,1,1,1,1]
create_n_BinaryList_objects(10)


'''Number_of_lists = 10
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


'''