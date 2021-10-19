import random as r

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

def create_binary_object(length):
    bin_list = []
    for i in range (length):
        if r.random() < 0.5:
            bin_list.append(0)
        else:
            bin_list.append(1)
    BinaryList_object = BinaryList(bin_list[:],compare_list(holy_grail,bin_list[:]))
    return BinaryList_object

def get_fit_score(binary_object):
    fit_score = compare_list(holy_grail,binary_object.list)
    return fit_score

def create_list(list_size, object_size):
    list_of_objects = []
    for i in range(list_size):
        obj = create_binary_object(object_size)
        list_of_objects.append(obj) 
    return list_of_objects

def mutate_list(obj):
    for i in range(len(obj.list)):
        if r.random() <= 0.1:         
            if obj.list[i] == 1:
                obj.list[i] = 0
            else:
                obj.list[i] = 1
    return obj

'''def mutate_list(list):
    for i in range(len(list)):
        if r.random() <= 0.1:         
            if list[i] == 1:
                list[i] = 0
            else:
                list[i] = 1
    return list'''

def pick_best_mutation(list):
    _score = 0
    best_mutation = object
    for i in range(len(list)):
        if list[i].fit_score > _score:
            _score = list[i].fit_score
            best_mutation = list[i]
    #print(_score)
    return best_mutation 

def create_new_evolution(size, obj):
    evolution = []
    
    for i in range(size):
        obj = BinaryList(mutate_list(obj),0)
        obj.fit_score = get_fit_score(obj)
        evolution.append(obj)
        #obj.show()
        evolution[i].show()
    print("etter for loopen ser den sånn ut:")
    for j in range(size):
        evolution[j].show()
    return evolution
    


size = 10

holy_grail = []
for i in range(size):
    holy_grail.append(1)

liste = create_list(size,size)

#for i in range(size):
    #liste[i].show()

score = 0

best_mutation = pick_best_mutation(liste)
#print(f"den beste listen er : {best_mutation.list} med score {best_mutation.fit_score}")
liste = create_new_evolution(size,best_mutation)
'''for i in range(size):
    liste[i].show()
'''

best_mutation = pick_best_mutation(liste)
#print(f"den beste listen er : {best_mutation.list} med score {best_mutation.fit_score}")

