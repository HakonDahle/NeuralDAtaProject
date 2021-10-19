import random as r

class ListMethods:


    def mutate_list(list):
        for i in range(len(list)):
            if r.random() <= 0.2:         
                if list[i] == 1:
                    list[i] = 0
                else:
                    list[i] = 1
        return list

    '''def create_n_BinaryList_objects(n):
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
            print(evolution_list[i])'''