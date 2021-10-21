import random as r

def create_rule_table(length):

    rule_table = []
    for i in range(length):
        if r.random() < 0.5:
            rule_table.append(0)
        else:
            rule_table.append(1)
    return rule_table




def mutate_rule_table(rule_table):
    for i in range(len(rule_table)):
        if r.random() <= 0.1:         
            if rule_table[i] == 1:
                rule_table[i] = 0
            else:
                rule_table[i] = 1
    return rule_table




