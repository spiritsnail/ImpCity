
import math
import random
import numpy

#number of players
players = 2
        
possibleValue = list(range(2,15))
possibleSuit = ['s','h','d','c']
deck = []
hand = []

deck = []
for deckValue in possibleValue:
    for deckSuit in possibleSuit:   
        
        deck.append([deckValue, deckSuit])        
        
#define a function to deal the top card of the deck

def deal(cards):
    
    cardout = []        
    for ccd in range(0,cards):
        cardout.append(deck[0])
        del deck[0]    
    return(cardout)
    
def poker():

    possibleValue = list(range(2,15))
    possibleSuit = ['s','h','d','c']

    hand = []
    deck = []
    
    for deckValue in possibleValue:
        for deckSuit in possibleSuit:   
            
            deck.append([deckValue, deckSuit])
    
    random.shuffle(deck)
    
    for cchands in range(0,players):
        hand.append( deal(2))
    
    board = deal(5)
    
    #values only
    valvec = [[]]
    suitvec = [[]]
    ehand = [[0]]
    
    for ccplay in range(1,players):
        valvec.append([]) 
        suitvec.append([])
        ehand.append([0])
        
    for ccval in range(0,players):   
        valvec[ccval].append(hand[ccval][0][0])
        suitvec[ccval].append(hand[ccval][0][1])
        valvec[ccval].append(hand[ccval][1][0])
        suitvec[ccval].append(hand[ccval][1][1])    
        
        for ccboard in range(0,5):
            valvec[ccval].append(board[ccboard][0])
            suitvec[ccval].append(board[ccboard][1])    
    
    #evaluate hands
    for ccval in range(0,players):
    
        countvec = [0]*13
        straight = 1    
        flush = 0
        cardsInSuit = []
        
        for ccnum in range(2, 15):
            countvec[ccnum-2] = valvec[ccval].count(ccnum)
    
        countvec.reverse()        
        
        for ccsuit in range(0,4):
            if suitvec[ccval].count(possibleSuit[ccsuit]) >= 5:
                flush = possibleSuit[ccsuit]
        #evaluate the hand
        #0highcard
        #if max(countvec) == 1:
        if max(countvec) == 1:
            ehand[ccval][0] = 0
            kicker = sorted(valvec[ccval],reverse=True)[0:5]
            ehand[ccval].extend(kicker)
        #1pair
        #2 two pair
        if max(countvec) == 2:
            if countvec.count(2) >= 2:
                ehand[ccval][0] = 2
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
            else:
                ehand[ccval][0] = 1
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                
    #    #3 three of a kind
        
        if max(countvec) == 3:
            if countvec.count(2) == 0 and countvec.count(3) == 1:
                ehand[ccval][0] = 3
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                ehand[ccval].append(14 - countvec.index(max(countvec)))
            else:
                #6 full house
                ehand[ccval][0] = 6
                ehand[ccval].append(14 - countvec.index(max(countvec)))
                countvec[countvec.index(max(countvec))] = 0
                for ccfh in range(0, len(countvec)):
                    if countvec[ccfh] == 3:
                        countvec[ccfh] == 2
                ehand[ccval].append(14 - countvec.index(max(countvec)))
       
       #4straight
            for ccstr in range(0, 9):
                if countvec[ccstr] > 0 and countvec[ccstr + 1] > 0 and \
                 countvec[ccstr + 2] > 0 and countvec[ccstr + 3] > 0 and \
                 countvec[ccstr + 4] > 0:
                     ehand[ccval][0] = 4
                     straight = 1
                     ehand[ccval][1] = countvec(14 - ccstr)
         #check for the wheel
                if countvec[0] > 0 and countvec[12] > 0 and countvec[11] > 0 and \
                 countvec[10] > 0 and countvec[9] > 0:
                     ehand[ccval][0] = 4
                     straight = 1
                     ehand[ccval][1] = 5
                     
    #    #5flush
        if flush != 0:
            ehand[ccval] = [5]
            for ccflush in range(0,5):
                if board[ccflush][1] == flush:
                    cardsInSuit.append(board[ccflush][0])
            if hand[ccval][0][1] == flush:
                cardsInSuit.append(hand[ccval][0][0])
            if hand[ccval][1][1] == flush:
                cardsInSuit.append(hand[ccval][1][0])
            
            ehand[ccval].extend(sorted(cardsInSuit,reverse=True)[0:5])
            
            #check for straight flush
            if straight == 1:
                for ccsf in range(0,len(cardsInSuit)-4):
                    if sorted(cardsInSuit)[ccsf+4] - sorted(cardsInSuit)[ccsf] == 4:
                        ehand[ccval] = [8,cardsInSuit[ccsf]]
                        
                #check for the wheel
                if 14 in cardsInSuit and 2 in cardsInSuit and 3 in cardsInSuit \
                 and 4 in cardsInSuit and 5 in cardsInSuit:
                     ehand[ccval] = [8,5]
    
    #    #7four of a kind
        if max(countvec) == 4:
            ehand[ccval] = [7]
            ehand[ccval].append( 14 - countvec.index(max(countvec)))
            countvec[countvec.index(max(countvec))] = 0
            ehand[ccval].append( 14 - countvec.index(max(countvec)))
    
    
    ccoverwin = 0
    couldwin = list(range(0,players))
    endpoint = 6
    losers = []
    
    #EVALUATE THE ULTIMATE WINNER
    
    while len(losers) < players - 1 and ccoverwin < endpoint:
    
        winvec = []     
        
        for ccwin in range(0,players):
            if ccwin not in losers:
                winvec.append(ehand[couldwin[ccwin]][ccoverwin])
            else:
                winvec.append(0)
    
        for ccwin2 in range(0,players):
            if winvec[ccwin2] == max(winvec):
                endpoint = len(ehand[ccwin2])
            elif ccwin2 not in losers:
                losers.append(ccwin2)
        
        ccoverwin += 1
        
        
    if len(couldwin) - len(losers) == 1:
        winner = [x for x in couldwin if x not in losers]
        #print("Player " + str(winner[0] + 1) + " wins!")
        return([winner[0],hand,ehand])
    else:
        winner = [x for x in couldwin if x not in losers]
        #print(str(winner) + " CHOP")
        return([players,hand,ehand])

aggression = 0.605
i_pairness = 0.177
i_lowcard =  0.674
i_highcard = 0.627
i_suited =   0.020
low_a =   0.332
low_b =   3.376
low_f =   0.392
high_a =  0.614
high_b =  7.319

terms = 10

bases= [aggression, i_pairness, i_lowcard, i_highcard, i_suited, \
    low_a, low_b, low_f, high_a, high_b]

perc = .05

def kingmake():
    #MAKE THE LIST OF POSSIBLE KINGS
    lowagg_base = bases[:]
    lowagg_base[0] -= perc * aggression
    hiagg_base = bases[:]
    hiagg_base[0] += perc * aggression
    crown = numpy.vstack((numpy.array([bases,]*163),\
        numpy.array([lowagg_base,]*163), \
        numpy.array([hiagg_base,]*163)))
    
    crown[0,:] = bases
    ccpr = 0
    
    for ccagg in range(0,3):   
        
        #+
        for ccplus in range(1,terms):
            ccpr += 1
            crown[ccpr, ccplus] += bases[ccplus] * perc
        
        #-
        for ccplus in range(1,terms):
            ccpr += 1
            crown[ccpr, ccplus] -= bases[ccplus] * perc
        
        #++
        for ccplus in range(1,terms):
            ccplus2 = ccplus + 1
            while ccplus2 < 9:
                ccpr += 1
                crown[ccpr, ccplus] += bases[ccplus] * perc
                crown[ccpr, ccplus2] += bases[ccplus2] * perc
                ccplus2 += 1
                
        #--
        for ccplus in range(1,terms):
            ccplus2 = ccplus + 1
            while ccplus2 < 9:
                ccpr += 1
                crown[ccpr, ccplus] -= bases[ccplus] * perc
                crown[ccpr, ccplus2] -= bases[ccplus2] * perc
                ccplus2 += 1
        
        #+-
        for ccplus in range(1,terms):
            for ccplus2 in range(1,terms):
                if ccplus != ccplus2:
                    ccpr += 1
                    crown[ccpr, ccplus] += bases[ccplus] * perc
                    crown[ccpr, ccplus2] -= bases[ccplus2] * perc
        
        ccpr += 1
    #   
    return(crown)

def castle_suited(suit_hand):
    if suit_hand[0][1] == suit_hand[1][1]:
        return(1)
    else:
        return(0)

def castle_high(high_hand,aa,bb):   
    xx = max(high_hand[0][0],high_hand[1][0])       
    outp = 1/(1 + math.exp(-aa * xx + bb))   
    return(outp)

def castle_low(low_hand,aa,bb,ff):
    bterm = 1/(1-ff)
    xx = min(low_hand[0][0],low_hand[1][0])       
    outp = 1/(bterm + math.exp(-aa * xx + bb)) + ff   
    return(outp)

def castle_gap(gap_hand):
    if gap_hand[0][0] == gap_hand[1][0]:
        return(1)
    else:
        return(0)

possibleValue = list(range(2,15))
possibleSuit = ['s','h','d','c']
deck = []
hand = []

cas_low  = [0, 0]
cas_high = [0, 0]
cas_pair = [0, 0]
cas_suit = [0, 0]

estvec1 = numpy.zeros([489,100])
estvec2 = numpy.zeros([489,100])
iters = 25000

for ccmega in range(0,50):
    
    king = kingmake()
    
    guess = numpy.zeros([numpy.size(king,0),1])
    for ccall in range(0,iters):
        
        deck = []
        for deckValue in possibleValue:
            for deckSuit in possibleSuit: 
                deck.append([deckValue, deckSuit])
        
        #shuffle the deck
        random.shuffle(deck)
        #play poker
        outcome = poker()
        
        for ccg in range(0,numpy.size(king, 0)):
            
            importance = sum(king[ccg,1:5])
            
            #evaluate hand 1            
            
            cas_low[0]  = castle_low(outcome[1][0],king[ccg,5],king[ccg,6],king[ccg,7])
            cas_high[0] = castle_high(outcome[1][0],king[ccg,8],king[ccg,9])
            cas_pair[0] = castle_gap(outcome[1][0])
            cas_suit[0] = castle_suited(outcome[1][0])        
            
            est1 = king[ccg, 0]*( \
            (king[ccg,1]/importance) * cas_low[0] + \
            (king[ccg,2]/importance) * cas_high[0] + \
            (king[ccg,3]/importance) * cas_pair[0] + \
            (king[ccg,4]/importance) * cas_suit[0] )
            
            #evaluate hand 2            
            
            cas_low[1]  = castle_low(outcome[1][1],king[ccg,5],king[ccg,6],king[ccg,7])
            cas_high[1] = castle_high(outcome[1][1],king[ccg,8],king[ccg,9])
            cas_pair[1] = castle_gap(outcome[1][1])
            cas_suit[1] = castle_suited(outcome[1][1])        
            
            est2 = king[ccg, 0]*( \
            (king[ccg,1]/importance) * cas_low[1] + \
            (king[ccg,2]/importance) * cas_high[1] + \
            (king[ccg,3]/importance) * cas_pair[1] + \
            (king[ccg,4]/importance) * cas_suit[1] )
            
            if ccall<100:
                estvec1[ccg,ccall] = est1
                estvec2[ccg,ccall] = est2
                
            if (est1 < est2 and outcome[0] == 1) or (est1 > est2 and outcome[0] == 0):
                guess[ccg] += 1
        
    oneking = random.choice(numpy.where(guess == max(guess))[0])
    aggression = float(king[oneking,0])
    i_pairness = float(king[oneking,1])
    i_lowcard =  float(king[oneking,2])
    i_highcard = float(king[oneking,3])
    i_suited   = float(king[oneking,4])
    low_a = float(king[oneking,5])
    low_b = float(king[oneking,6])
    low_f = float(king[oneking,7])
    high_a = float(king[oneking,8])
    high_b = float(king[oneking,9])
    
    bases= [aggression, i_pairness, i_lowcard, i_highcard, i_suited, \
    low_a, low_b, low_f, high_a, high_b]
    
    perc = float(.69 - max(guess)/iters)
    
    print(max(guess)/iters)
    print(bases)