# Imp City 1.2.1
# "Monkey See"

import numpy
import random
import math
import matplotlib.pyplot as pplot

##Input Parameters

#initial distribution of Imps
impLocations = []
xCoords = [[],[],[],[],[],[],[],[],[]]
yCoords = [[],[],[],[],[],[],[],[],[]]

#GENERATE THE INITIAL Locations OF PLANTS
for cc0 in range(0,10):
    for cc1 in range(0,10):
        impLocations.append(numpy.array([cc0, cc1]))
        
numberOfImps = len(impLocations)
foodlist = numpy.ones([1,len(impLocations)])[0]

#egalitarianism
#the maximum more than your share that a relationship can be
egalitarianism = 100

#base traits
baseT = numpy.array([10, 10, 10])

#variations and entropies
variation = 10/3  #10 being average
entropy = 1/3     #10 being average

proximityModifierVariation = 1/3
proximityModifierEntropy = 1/30

memoryModifierVariation = 1/3
memoryModifierEntropy = 1/30

#reproduction constants
floweringDistance = 1/2
floweringStddev = 1/8

#expanded prisoner's dilemma
consequenceMatrix = numpy.array([[-.25,0,.3],[-.05,0,.05],[-.4,0,.2]])

#CRUNCH
bases = [] #base behavior matrix (1,3)
proximityModifiers   = [] #proximity coefficient vectors (1,3)
memoryModifers   = [] #memory coefficient matricies  (3,3)
isdead = []
gens = 1
megakill = 0

## Function Definitions
 
def wre(param):
    neo = random.random() * sum(param)
    cc = 0
    bi = 1
    lenna = len(param)
    
    #biangulate the max number of possible times        
    while bi <= math.floor(math.log(lenna,2)):
        if sum(param[:cc + math.floor(lenna/math.pow(2,bi))]) < neo:
            cc += math.floor(lenna/math.pow(2,bi))
        bi += 1

    while cc < lenna:
        if neo <= sum(param[:cc+1]):
            return cc
        cc += 1

    return lenna

def makeMemoryList(popul):
    friendslist = []
    for cc in range(0,popul):
        friendslist.append(numpy.zeros([3,popul]))
    return friendslist

def makeBases():
    test = numpy.array([random.normalvariate(10,variation),
                        random.normalvariate(10,variation),
                        random.normalvariate(10,variation)])
    return test    

def reproduce(parent):
    loc = numpy.zeros([1,2])[0]
    direc = random.random()*2*math.pi
    loc[0] = impLocations[parent][0] + random.normalvariate(floweringDistance,floweringStddev) * math.cos(direc)
    loc[1] = impLocations[parent][1] + random.normalvariate(floweringDistance,floweringStddev) * math.sin(direc)
    mmMod = numpy.random.normal(0,memoryModifierEntropy,[3,3])
    mmNew = memoryModifers[parent] + mmMod
    pmMod = numpy.random.normal(0,proximityModifierEntropy,[1,3])
    pmNew = proximityModifiers[parent] + pmMod
    baseMod = numpy.random.normal(0,entropy,[1,3])[0]
    newBases = bases[parent] + baseMod
    return [loc, mmNew, pmNew, newBases]

#populate the characteristics of the initial set of Imps
for cc in range(0, numberOfImps):
    bases.append(makeBases())
    proximityModifiers.append(numpy.random.normal(0,proximityModifierVariation,[1,3]))
    memoryModifers.append(numpy.random.normal(0,proximityModifierVariation,[3,3]))
    
    if bases[cc][0] == max(bases[cc]):
        if proximityModifiers[cc][0][0] == max(proximityModifiers[cc][0]):      #hostile general, hostile close
            xCoords[0].append(impLocations[cc][0])
            yCoords[0].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][1] == max(proximityModifiers[cc][0]):    #hostile general, neutral close
            xCoords[1].append(impLocations[cc][0])
            yCoords[1].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][2] == max(proximityModifiers[cc][0]):    #hostile general, friendly close
            xCoords[2].append(impLocations[cc][0])
            yCoords[2].append(impLocations[cc][1])
    elif bases[cc][1] == max(bases[cc]):
        if proximityModifiers[cc][0][0] == max(proximityModifiers[cc][0]):      #neutral general, hostile close
            xCoords[3].append(impLocations[cc][0])
            yCoords[3].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][1] == max(proximityModifiers[cc][0]):    #neutral general, neutral close
            xCoords[4].append(impLocations[cc][0])
            yCoords[4].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][2] == max(proximityModifiers[cc][0]):    #neutral general, friendly close
            xCoords[5].append(impLocations[cc][0])
            yCoords[5].append(impLocations[cc][1])
    elif bases[cc][2] == max(bases[cc]):
        if proximityModifiers[cc][0][0] == max(proximityModifiers[cc][0]):      #friendly general, hostile close
            xCoords[6].append(impLocations[cc][0])
            yCoords[6].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][1] == max(proximityModifiers[cc][0]):    #friendly general, neutral close
            xCoords[7].append(impLocations[cc][0])
            yCoords[7].append(impLocations[cc][1])
        elif proximityModifiers[cc][0][2] == max(proximityModifiers[cc][0]):    #friendly general, friendly close
            xCoords[8].append(impLocations[cc][0])
            yCoords[8].append(impLocations[cc][1])
            
ml = makeMemoryList(numberOfImps)

#Generate a proximity list
#proximity is the inverse square of distance
proxlist = numpy.zeros([3, .5*len(impLocations)*(len(impLocations)-1)])
ccd1 = 0
tct = 0
while ccd1 < len(impLocations):
    for ccd2 in range(ccd1+1, len(impLocations)):
        proxlist[0][tct] = ccd1
        proxlist[1][tct] = ccd2
        dis = numpy.linalg.norm(impLocations[ccd1]-impLocations[ccd2])
        proxlist[2][tct] = 1/(dis*dis) #proximity
        tct += 1

    ccd1 += 1

while megakill == 0:
    
    pplot.plot(xCoords[0],yCoords[0], 'r*') #hostile all, hostile close
    pplot.plot(xCoords[1],yCoords[1], 'rv')    
    pplot.plot(xCoords[2],yCoords[2], 'ro')
    pplot.plot(xCoords[3],yCoords[3], 'y*')
    pplot.plot(xCoords[4],yCoords[4], 'yv')
    pplot.plot(xCoords[5],yCoords[5], 'yo')
    pplot.plot(xCoords[6],yCoords[6], 'g*')
    pplot.plot(xCoords[7],yCoords[7], 'gv')
    pplot.plot(xCoords[8],yCoords[8], 'go')
    pplot.axis([-8,18,-8,18])
    pplot.show()
    
    #RUN A GENERATION
    for ccp in range(0,2*numberOfImps):
        #CHOOSE A PAIR OF PLANTS
        chosepair = wre(proxlist[2])
        imp1 = int(proxlist[0][chosepair])
        imp2 = int(proxlist[1][chosepair])
        proximity = proxlist[2][chosepair]   
        
        #generate the final decision vector of plant 1
        finalDecisionVector1 = bases[imp1]
        finalDecisionVector1 = finalDecisionVector1 + (proximityModifiers[imp1][0] * proximity)
        finalDecisionVector1 = finalDecisionVector1 + sum(memoryModifers[imp1] * numpy.array([[ml[imp1][0][imp2]],
                                                    [ml[imp1][1][imp2]],
                                                    [ml[imp1][2][imp2]]]))
        #choose an action for plant 1
        if max(finalDecisionVector1) <= 0:
            finalDecisionVector1 = numpy.array([1,1,1])
        
        if min(finalDecisionVector1) < 0:
            for cc1 in range(0,3):
                if finalDecisionVector1[cc1] < 0:
                    finalDecisionVector1[cc1] = 0
                    
        choice1 = wre(finalDecisionVector1)
        
        #generate the final decision vector of plant 2
        finalDecisionVector2 = bases[imp2]
        finalDecisionVector2 = finalDecisionVector2 + (proximityModifiers[imp2][0] * proximity)
        finalDecisionVector2 = finalDecisionVector2 + sum(memoryModifers[imp2] * numpy.array([[ml[imp2][0][imp1]],
                                                    [ml[imp2][1][imp1]],
                                                    [ml[imp2][2][imp1]]]))
        #choose an action for plant 2
        if max(finalDecisionVector2) <= 0:
            finalDecisionVector2 = numpy.array([1,1,1])
        
        if min(finalDecisionVector2) < 0:
            for cc2 in range(0,3):
                if finalDecisionVector2[cc2] < 0:
                    finalDecisionVector2[cc2] = 0
        
        choice2 = wre(finalDecisionVector2)
        
        #modify the food and memories of the paticipants
        foodlist[imp1] += consequenceMatrix[choice1][choice2]
        foodlist[imp2] += consequenceMatrix[choice2][choice1]
        
        ml[imp1][choice2][imp2] += 1
        ml[imp2][choice1][imp1] += 1
        
        #print(" " + str(choice1) + "  " + str(choice2))    
        
        #kill any imps who have 0 or less food
        newprox = False
        noik = len(foodlist)
        if min(foodlist) <= 0:
            #delete its location
            for cck in range(0,noik):
                if foodlist[cck] <= 0 and not cck in isdead:
                    isdead.append(cck)
                    newprox = True
                        
            #generate a new proximity list without the killed imps
            if newprox:
                proxlist = numpy.zeros([3, .5*(numberOfImps - len(isdead))*(numberOfImps - len(isdead) - 1)])
                ccd1 = 0
                tct = 0
                while ccd1 < numberOfImps:
                    for ccd2 in range(ccd1+1, numberOfImps):
                        if ccd1 not in isdead and ccd2 not in isdead:
                            proxlist[0][tct] = ccd1
                            proxlist[1][tct] = ccd2
                            dis = numpy.linalg.norm(impLocations[ccd1]-impLocations[ccd2])
                            proxlist[2][tct] = 1/(dis*dis)
                            tct += 1
                    ccd1 += 1
                
                proxlist[2]= numpy.clip(proxlist[2::][0], 0, egalitarianism*numpy.average(proxlist[2::][0]))
    #We are done with a generation. Now reproduce.
    
    #return [loc, mmNew, pmNew, newBases]
    
    ngloc = []
    ngmemoryModifers = []
    ngproximityModifiers = []
    ngbases = []
    xCoords = [[],[],[],[],[],[],[],[],[]]
    yCoords = [[],[],[],[],[],[],[],[],[]]
    
    for ccf in range(0,len(foodlist)):
        if ccf not in isdead:
            for ccb in range(0, math.floor(foodlist[ccf])):
                baby = reproduce(ccf)
                ngloc.append(baby[0])
                ngmemoryModifers.append(baby[1])
                ngproximityModifiers.append(baby[2])
                ngbases.append(baby[3])
                
                #sort locations for the purpose of plotting them later                
                
                if baby[3][0] == max(baby[3]):
                    if baby[2][0][0] == max(baby[2][0]):      #hostile general, hostile close
                        xCoords[0].append(baby[0][0])
                        yCoords[0].append(baby[0][1])
                    elif baby[2][0][1] == max(baby[2][0]):    #hostile general, neutral close
                        xCoords[1].append(baby[0][0])
                        yCoords[1].append(baby[0][1])
                    elif baby[2][0][2] == max(baby[2][0]):    #hostile general, friendly close
                        xCoords[2].append(baby[0][0])
                        yCoords[2].append(baby[0][1])
                elif baby[3][1] == max(baby[3]):
                    if baby[2][0][0] == max(baby[2][0]):      #neutral general, hostile close
                        xCoords[3].append(baby[0][0])
                        yCoords[3].append(baby[0][1])
                    elif baby[2][0][1] == max(baby[2][0]):    #neutral general, neutral close
                        xCoords[4].append(baby[0][0])
                        yCoords[4].append(baby[0][1])
                    elif baby[2][0][2] == max(baby[2][0]):    #neutral general, friendly close
                        xCoords[5].append(baby[0][0])
                        yCoords[5].append(baby[0][1])
                elif baby[3][2] == max(baby[3]):
                    if baby[2][0][0] == max(baby[2][0]):      #friendly general, hostile close
                        xCoords[6].append(baby[0][0])
                        yCoords[6].append(baby[0][1])
                    elif baby[2][0][1] == max(baby[2][0]):    #friendly general, neutral close
                        xCoords[7].append(baby[0][0])
                        yCoords[7].append(baby[0][1])
                    elif baby[2][0][2] == max(baby[2][0]):    #friendly general, friendly close
                        xCoords[8].append(baby[0][0])
                        yCoords[8].append(baby[0][1])
                
            runt = random.random()
            if runt < foodlist[ccf]%1:
                baby = reproduce(ccf)
                ngloc.append(baby[0])
                ngmemoryModifers.append(baby[1])
                ngproximityModifiers.append(baby[2])
                ngbases.append(baby[3])
    
    print(len(impLocations))
    print("*****")
    
    if len(ngloc)>200:
        print("UTOPIA!")
        megakill = 1
    elif len(ngloc)<20:
        print("collapse!")
        megakill = 1
    else:
        gens += 1
        impLocations = ngloc
        memoryModifers = ngmemoryModifers
        proximityModifiers = ngproximityModifiers
        bases = ngbases
        isdead = []
        
        numberOfImps = len(impLocations)
        foodlist = numpy.ones([1,len(impLocations)])[0]
        ml = makeMemoryList(numberOfImps)
        
        test0 = proxlist
        
        #Generate a new proximity list
        proxlist = numpy.zeros([3, .5*len(impLocations)*(len(impLocations)-1)])
        ccd1 = 0
        tct = 0
        while ccd1 < len(impLocations):
            for ccd2 in range(ccd1+1, len(impLocations)):
                proxlist[0][tct] = ccd1
                proxlist[1][tct] = ccd2
                dis = numpy.linalg.norm(impLocations[ccd1]-impLocations[ccd2])
                proxlist[2][tct] = 1/(dis*dis)
                tct += 1
            ccd1 += 1
        
        proxlist[2]= numpy.clip(proxlist[2::][0], 0, egalitarianism*numpy.average(proxlist[2::][0]))
