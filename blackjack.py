import random
import time
from assets.cards.creation import *




hand=[]

deck=[]
LastCard=""
HITORSTICK="stick"
Total=0
Dealerhand=[]
DealerTotal=0
bet=0

def reset():
  global hand
  global Dealerhand
  global deck
  global LastCard
  global HITORSTICK
  global Total
  global DealerTotal
  global bet
  hand=[]
  Dealerhand=[]
  deck=[]
  LastCard=""
  HITORSTICK="stick"
  Total=0
  DealerTotal=0
  bet=0

def GetWallet(Username,database):
  Wallet = database.execute("SELECT Wallet FROM USERS WHERE Username = ?",[Username]).fetchone()
  Wallet= str(Wallet).strip("(,)")
  Wallet= int(Wallet)
  return Wallet

def MakeDeck():
  card = ["11", "2", "3", '4', '5', '6', '7', '8', '9', '10', '11', '11', '11']
  value = [
    "Ace", "2", "3", '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen',
    'King'
  ]
  suits = ["diamonds", "hearts", "spades", "clubs"]
  for x in range(len(value)):
    for y in range(len(suits)):
      deck.append([value[x], suits[y]])

  random.shuffle(deck)



def SelectCard(hand,Total):
  
  hand.append(deck[0])
  LastCard = hand[-1][0]
  
  if LastCard == 'King' or LastCard == 'Jack' or LastCard == 'Queen':
    Total +=10
  elif LastCard == 'Ace':
    if Total + 11 > 21:
      Total += 1
    else:
      Total +=11
  else:
    Total += int(deck[0][0])
  
  deck.pop(0)
  print('card',len(hand),hand[len(hand)-1],'\n')
  if len(hand)>2:
    print('Your hand - ', hand,'Total - ',Total,'\n' )
  return hand, Total

def DealerCard(Dealerhand,DealerTotal):
  global LastCard
  Dealerhand.append(deck[0])
  LastCard = Dealerhand[-1][0]
  
  if LastCard == 'King' or LastCard == 'Jack' or LastCard == 'Queen':
    DealerTotal +=10
  elif LastCard == 'Ace':
    if DealerTotal + 11 > 21:
      DealerTotal += 1
    else:
      DealerTotal +=11
  else:
    DealerTotal += int(deck[0][0])
  
  deck.pop(0)
  if len(Dealerhand) == 1:
    print("Dealer's card number",len(Dealerhand),Dealerhand[len(Dealerhand)-1],'\n')
  elif len(Dealerhand) == 2:
    print("Dealer has recieved their second card\n")
  return Dealerhand, DealerTotal


# def Hit():
#   global HITORSTICK


#   if Total <21:
#     HITORSTICK=input("do you want to hit or stick?\n")
#     if HITORSTICK.lower() == 'stick':
#       if Total<21:
#         DealerHit()
#     else:
#       SelectCard()
#       Hit()
 
# def DealerHit():
#   if DealerTotal < 18:
#     Dealerhand, DealerTotal = DealerCard()
#     DealerHit()
#   return Dealerhand, Dealerhand
  
def Deciding(DealerTotal, Total):
  print(DealerTotal,Total)
  if Total == 21:
    print('oh no')
    if DealerTotal == 21:
      print('blackjack push')
      return 'push'
    else:
      print('blackjack')
      return 'p'
  elif Total > 21:
    print('Dealer Won')
    return 'd'
  elif DealerTotal>21:
    print('Player Won')
    return 'p'
  elif Total < DealerTotal:
    print('Dealer Won\n')
    return 'd'
  elif Total == DealerTotal:
    print('Push\n')
    return 'push'
  else:
    print('Player Won\n')
    return 'p'

def Payout(pay,Username,database,Wallet,bet,hand,Total):
  if pay == 'p':
    Wallet = Wallet + (2*bet)
    if len(hand) == 2 and Total == '21':
      Wallet +=bet
  elif pay == 'push':
    Wallet += bet
  else:
    pass
  print('Balance: ', Wallet,'\n')
  database.execute("UPDATE USERS SET Wallet = ? WHERE Username =?",[Wallet,Username])
  database.commit()

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





# def Play(Username,database):
#   global Wallet
#   reset()
#   Wallet = GetWallet(Username,database)
#   MakeDeck()
#   PB=PlaceBet()
#   if PB == 'blank':
#     return
#   SelectCard()
#   DealerCard()
#   SelectCard()
#   DealerCard()
#   Hit()
#   print('player',hand,'\n')
#   print('dealer',Dealerhand,'\n')

#   pay=Deciding()
#   Payout(pay,Username,database)
  
  

# SelectCard()
# SelectCard()
# print('hand', hand)
# print('dealerhand' ,Dealerhand)
# Hit()




    