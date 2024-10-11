import pygame
import pygame_gui
import os
import random
import time

slot=['casino','diamond','lemon','watermelon','cherry','apple']
SLOTMACHINE= pygame.transform.scale(pygame.image.load(os.path.join('assets','slots','slotmachine' + '.png')),(475,395))

# 3 sevens = x8
# 3 diamonds = x6
# 3 lemons = x4
# 3 watermelons = x3
# 3 cherries =x2
# 3 apples = x1


def SLOT_RANDOM(window,width):
    for a in range(12):
        window.blit(SLOTMACHINE,(width//2 - 197,5))
        x= width//2-134
        y=191
        for z in range(3):
            slotVAL= random.randint(0,3)
            slotVAL+= random.randint(0,1)
            slotVAL+= random.randint(0,1)
            icon=pygame.transform.scale(pygame.image.load(os.path.join('assets','slots',slot[slotVAL] + '.png')),(52,52))
            window.blit(icon,(x,y))
            pygame.display.update()
            x+= 110
        time.sleep(0.1)
def SLOT_GEN(slotvalues,screen,width):
    slotvalues=[]
    x= width//2-134
    y=191
    for z in range(3):
        #random number generated that links to the icon
        slotVAL= random.randint(0,3)
        slotVAL+= random.randint(0,1)
        slotVAL+= random.randint(0,1)
        icon=pygame.transform.scale(pygame.image.load(os.path.join('assets','slots',slot[slotVAL] + '.png')),(52,52))
        screen.blit(icon,(x,y))
        pygame.display.update()
        x+= 110
        slotvalues.append(slotVAL)
    return slotvalues

def GetWallet(Username,database):
  Wallet = database.execute("SELECT Wallet FROM USERS WHERE Username = ?",[Username]).fetchone()
  Wallet= str(Wallet).strip("(,)")
  Wallet= int(Wallet)
  return Wallet

def PlaceBet(Username,database, bet):
  wallet = GetWallet(Username,database)
  
  temp = wallet - bet
  if temp < 0:
    return 'broke'
  else:
    wallet = temp
    database.execute("UPDATE USERS SET Wallet = ? WHERE Username =?",[wallet,Username])
    database.commit()
    bet =int(bet)
  return 


def winning (slotvalues,bet,username,database,wallet):
    if slotvalues[0]== slotvalues[1] and slotvalues[0]== slotvalues[2]:
        #determining how much should be awarded
        if slotvalues[0] == 0:
            wallet += 2*bet
        elif slotvalues[0] == 1:
            wallet += 3*bet
        elif slotvalues[0] == 2:
            wallet += 4*bet
        elif slotvalues[0] == 3:
            wallet += 5*bet
        elif slotvalues[0] == 4:
            wallet +=  6*bet
        else:
            wallet += 8*bet
        database.execute("UPDATE USERS SET Wallet = ? WHERE Username =?",[wallet,username])
        database.commit()
    elif slotvalues[0] == slotvalues[1] or slotvalues[0] == slotvalues[2] or slotvalues[1] == slotvalues[2]:
        if slotvalues[0] == 0:
            wallet += bet
        elif slotvalues[0] == 1:
            wallet += bet
        elif slotvalues[0] == 2:
            wallet += bet
        elif slotvalues[0] == 3:
            wallet += 2*bet
        elif slotvalues[0] == 4:
            wallet +=  4*bet
        else:
            wallet += 5*bet
        database.execute("UPDATE USERS SET Wallet = ? WHERE Username =?",[wallet,username])
        database.commit()
