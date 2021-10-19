import random as r
import time
#import ListMethods as lm

class BinaryList:

    best_score = 0

    def __init__ (self, list,fit_score):
        self.list = list
        self.fit_score = fit_score

    def update_best_score(self,x):
        self.best_score = x


    def get_fit_score(self):
        return self.fit_score

    def show(self):
        print(f"list: {self.list}, fitness-score: {self.fit_score}")

def compare_list(holy_grail, list):
    fit_score = 0       

    for i in range(len(list)):
        if holy_grail[i] == list[i]:
            fit_score += 1
    return fit_score

def mutate_list(list):
    for i in range(len(list.list)):
        if r.random() <= 0.02:         
            if list[i].list == 1:
                list[i].list = 0
            else:
                list[i].list = 1
        list.fit_score = compare_list(holy_grail,list.list)
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
        
        BinaryList_object = BinaryList(bin_list[:],0) 
        BinaryList_object.fit_score = compare_list(holy_grail,BinaryList_object.list) 
        #BinaryList_object.show()
        evolution_list.append(BinaryList_object)
        #evolution_list[i].show()
        bin_list.clear()
        #evolution_list[i].show()
    return evolution_list

def pick_best_mutation(list):
    _score = 0
    best_mutation = 0
    for i in range(len(list)):
        if list[i].fit_score > _score:
            _score = list[i].fit_score
            best_mutation = list[i]
    return best_mutation     

size = 100

holy_grail = []
for i in range(size):
    holy_grail.append(1)

#print(holy_grail)

score = 0   
list = create_n_BinaryList_objects(size)
Best_object = pick_best_mutation(list)

while score < 75:
    
    print(score)
    mutated_list = mutate_list(Best_object)
    Best_object = pick_best_mutation(mutated_list)
    score = Best_object.fit_score





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