import pygame
import pygame_gui
import os
import random
import time


bias=[1,1,1,1,1,1,1,3,3,3,3,3,3,8,8,8,8,8,8,5,5,5,5,0,0,0,0,0,2,2,2,2,4,4,4,4,8,8,8,6,6,1,2,3,4,5,6,7,8,0,0,1,3,8,1,3,1]
payoutLIST=[[2,2.5,11],[1.25,1.75,3],[2.5,3,13],[1.4,1.9,5],[3,6,16],[11,25,51],[1.8,2.2,9],[3.5,11,26],[1.5,2,6]]

def grid_maker(slotGRID,slot):
    for x in range(6):
        for y in range(5):
            place= random.choice(bias)

            slotGRID[x][y]= slot[place]
    return slotGRID



def seven_check(slotGRID,slot,bet):
    icon_remover =[]
    payout=0

    for a in range(len(slot)):
        count=0
        for x in range(len(slotGRID)):
            for y in range(len(slotGRID[x])):
                if slotGRID[x][y] == slot[a]:
                    count +=1
                    
        if count >6:
            icon_remover.append(slot[a])
            #check if 7/8 mathcing icons
            if count < 9:
                payout += bet*float(payoutLIST[a][0])
                payout = round(payout)
            #checks if 8-11 mathcing icons
            elif count >8 and count <12:
                payout += bet*float(payoutLIST[a][1])
                payout = round(payout)
            #check if more than 11 mathcing icons
            else:
                payout += bet*float(payoutLIST[a][2])
                payout = round(payout)

    if len(icon_remover) > 0:    
        for x in range(len(slotGRID)):
            for y in range(len(slotGRID[x])):
                for z in range(len(icon_remover)):
                    if slotGRID[x][y] == icon_remover[z]:
                        slotGRID[x][y] = 'replace'
    print(slotGRID)
    print('\n\n\n')
    for x in range(len(slotGRID)):
        for y in range(len(slotGRID[x])):
            if slotGRID[x][y] == 'replace':
                place = random.randint(0,5)
                slotGRID[x][y]= slot[place]
        time.sleep(0.5)

    print(slotGRID)
    counter = len(icon_remover)          
    return slotGRID, counter, payout

