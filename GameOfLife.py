import pycxsimulator
from pylab import *
import random as r
import Rule_table as rule

width = 8
height = 8
initProb = 0.2
rule_set = rule.create_rule_table(256)
'''for i in range(256):
    if r.random() < 0.5:
        rule_set.append(0)
    else:
        rule_set.append(1)
'''
def initialize():
    global time, config, nextConfig

    time = 0
    
    config = zeros([height, width])
    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = 1
            else:
                state = 0
            config[y, x] = state

    

    nextConfig = zeros([height, width])

def observe():
    cla()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    axis('image')
    title('t = ' + str(time))

def update():
    global time, config, nextConfig, rule_set

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            numberOfAlive = []
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    numberOfAlive.append(config[(y+dy)%height, (x+dx)%width])
            del numberOfAlive[5]

            num = 0
            for b in numberOfAlive:
                num = 2 * num + b
            num = int(num)
            #print(num) # 6

            #print(numberOfAlive) 

            state = int(rule_set[num])
            numberOfAlive.clear()

            nextConfig[y, x] = state
    rule_set = rule.mutate_rule_table(rule_set)
    config, nextConfig = nextConfig, config

pycxsimulator.GUI().start(func=[initialize, observe, update])