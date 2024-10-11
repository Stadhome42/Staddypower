import pygame
import os
import LandS
import pygame_gui
import time
import random
import blackjack, slots, sweet
import sqlite3
from assets.cards.creation import *
pygame.init()

# variables
WIDTH, HEIGHT = 900, 500
MAIN_MENU = pygame.display.set_mode((WIDTH, HEIGHT))
LOGGING = pygame.display.set_mode((WIDTH, HEIGHT))
SIGNUP = pygame.display.set_mode((WIDTH, HEIGHT))
GAMES = pygame.display.set_mode((WIDTH,HEIGHT))
BLACKJACK = pygame.display.set_mode((WIDTH,HEIGHT))
SLOTS = pygame.display.set_mode((WIDTH,HEIGHT))
SWEET = pygame.display.set_mode((WIDTH,HEIGHT))
WALLET = pygame.display.set_mode((WIDTH,HEIGHT))
database = sqlite3.connect('DATABASES.db')


pygame.display.set_caption("StaddyPower")
pygame.display.set_icon(pygame.image.load(os.path.join('assets','sweet','z_loly' + '.png')))
MANAGER_LI = pygame_gui.UIManager((WIDTH,HEIGHT))
MANAGER_SU = pygame_gui.UIManager((WIDTH,HEIGHT))
clock = pygame.time.Clock()
FPS = 100

#colours
global BLUE
BLUE = (102, 212, 255)
RED = (220,20,60)
ORANGE =(255,128,0)
YELLOW =(255,255,0)
PINK = (255,131,250)
GREEN = (0,100,0)
GREY = (220,220,220)
BLACK=(0,0,0)

#images
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('Assets','SPlogo.png')),(256,45))
BGAHELPLINE = pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','gambleaware-helpline-logo-black.png')),(305.4,216))
BGA = pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','begambleawareorg_black_png.png')),(192.5,25))
SWEETBACKGROUND =pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','sweet.jpg')),(900,500))
SWEETFRAME =pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','frame.png')),(470,370))
SWEETFRAME.set_alpha(220)
SWEETLOGO =pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','sweetbonanza.png')),(160,160))
SLOTLOGO =pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','slot.png')),(160,169))
BLACKJACKLOGO =pygame.transform.scale(pygame.image.load(os.path.join('assets','BGA','blackjack.png')),(160,160))

#font
ERRORFONT = pygame.font.SysFont('calibri', 16)
WALLETFONT = pygame.font.SysFont('calibri', 24)
WINFONT = pygame.font.SysFont('calibri', 26)


#colour picker class
class ColorPicker():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((220,220,220))
        self.rad = h//2
        self.pwidth = w-self.rad*2
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, color, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def get_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        if color.hsla == (0.0, 100.0, 50.0, 100.0):
            color = (102, 212, 255)
            return color
        return color

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 2)

#colour checking
def colourCheck():
    BLUE=COLOURPICKER.get_color()
    return BLUE
COLOURPICKER = ColorPicker(WIDTH//2-180, HEIGHT-150, 360, 20)


#button + rectangle + circle classes
class button():
    def __init__(self,colour, X, Y, width, height, text='',size=''):
        self.color = colour
        self.x = X
        self.y = Y
        self.width = width
        self.height = height
        self.text = text
        self.size = size

    def draw(self,MAIN_MENU,outline=None):
    #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(MAIN_MENU, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(MAIN_MENU, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            if self.size == 'medium':
                font = pygame.font.SysFont('comicsans', 28)
            elif self.size == 'small':
                font = pygame.font.SysFont('comicsans', 16)
            text = font.render(self.text, 1, (0,0,0))
            MAIN_MENU.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
    #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class rectangle():
    def __init__(self,colour, X, Y, width, height, text='',size=''):
        self.color = colour
        self.x = X
        self.y = Y
        self.width = width
        self.height = height
        self.text = text
        self.size = size

    def draw(self,MAIN_MENU,outline=None):
    #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(MAIN_MENU, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(MAIN_MENU, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            if self.size == 'medium':
                font = pygame.font.SysFont('comicsans', 28)
            elif self.size == 'small':
                font = pygame.font.SysFont('comicsans', 16)
            elif self.size == 'very small':
                font = pygame.font.SysFont('comicsans', 10)
            text = font.render(self.text, 1, (0,0,0))
            MAIN_MENU.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
    #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class circle():
    def __init__(self,colour, X, Y, radius, width, text='',size=''):
        self.color = colour
        self.x = X
        self.y = Y
        self.radius = radius
        self.width = width
        self.text = text
        self.size = size

    def draw(self,MAIN_MENU,outline=None):
    #Call this method to draw the button on the screen            
        pygame.draw.circle(MAIN_MENU, self.color, (self.x,self.y),self.radius,self.width)
        
        if self.text != '':
            if self.size == 'medium':
                font = pygame.font.SysFont('comicsans', 28)
            elif self.size == 'small':
                font = pygame.font.SysFont('comicsans', 16)
            elif self.size == 'very small':
                font = pygame.font.SysFont('comicsans', 10)
            text = font.render(self.text, 1, (0,0,0))
            MAIN_MENU.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def isOver(self, pos):
    #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.radius:
            if pos[1] > self.y and pos[1] < self.y + self.radius:
                return True
            
        return False

#circles

ONECIRCLE= circle(GREEN,225,420+10,25,25,'1','small')
FIVECIRCLE= circle(RED,300,420+10,25,25,'5','small')
TENCIRCLE= circle(ORANGE,375,420+10,25,25,'10','small')
TWENTYCIRCLE= circle(YELLOW,450,420+10,25,25,'20','small')
FIFTYCIRCLE= circle(PINK,525,420+10,25,25,'50','small')
HUNDREDCIRCLE= circle(GREEN,600,420+10,25,25,'100','small')
HITCIRCLE= circle(GREEN,100,420+10,50,50,'HIT','medium')
STANDCIRCLE= circle(RED,WIDTH - 100,420+10,50,50,'STAND','medium')
PLAYCIRCLE= circle(GREEN,100,420+10,50,50,'PLAY','medium')

#collision points for circles
ONEBUTTON= button((0,0,0),200,395+10,50,50)

FIVEBUTTON= button((0,0,0),275,395+10,50,50)
TENBUTTON= button((0,0,0),350,395+10,50,50)
TWENTYBUTTON= button((0,0,0),425,395+10,50,50)
FIFTYBUTTON= button((0,0,0),500,395+10,50,50)
HUNDEREDBUTTON= button((0,0,0),575,375+10,80,80)
HITBUTTON= button((0,0,0),50,375+10,80,80)
STANDBUTTON= button((0,0,0),WIDTH-150,375+10,80,80)
PLAYBUTTON= button((0,0,0),50,375+10,80,80)
SLOTPLAYBUTTON =button((0,0,0),WIDTH//2+228,62,50,50)


#rectangles
USERNAME_LOGINRECT= rectangle(GREY, 200, 100, 100, 30, 'Username:', 'small')
PASSWORD_LOGINRECT= rectangle(GREY, WIDTH - 300, 100, 100, 30, 'Password:', 'small')
USERNAME_SIGNUPRECT= rectangle(GREY, 100, 120, 100, 30, 'Username:', 'small')
PASSWORD_SIGNUPRECT= rectangle(GREY, WIDTH - 200, 120, 100, 30, 'Password:', 'small')
FIRSTNAME_SIGNUPRECT= rectangle(GREY, 100, 220, 100, 30, 'Firstname:', 'small')
SURNAME_SIGNUPRECT= rectangle(GREY, WIDTH - 200, 220, 100, 30, 'Surname:', 'small')
AGE_SIGNUPRECT= rectangle(GREY, 100, 320, 100, 30, 'Age:', 'small')
EMAIL_SIGNUPRECT= rectangle(GREY, WIDTH - 200, 320, 100, 30, 'Email:', 'small')
BALANCERECT= rectangle(GREY,0  ,0,125,40, 'Wallet/Settings', 'small')
TABLERECT= rectangle(GREY,0,0,WIDTH,HEIGHT-100)
SLOTSTABLERECT =rectangle(GREY,0,HEIGHT-100,WIDTH,100)
WINRECT= rectangle(GREY, WIDTH//2-93, HEIGHT//2 , 186, 30, 'Congratulations you won!!', 'small')
PUSHRECT= rectangle(GREY, WIDTH//2-93, HEIGHT//2 , 186, 30, 'Push', 'small')
LOSERECT= rectangle(GREY, WIDTH//2-93, HEIGHT//2 , 186, 30, 'Dealer won', 'small')
BACKGROUNDRECT= rectangle(GREY, WIDTH//2-90, HEIGHT-190 , 180, 20, 'Background colour', 'small')


#buttons
LOGINBUTTON= button(GREY, 150, 100, 100, 60, 'Log in', 'medium')
SUBMIT_LOGINBUTTON= button(GREY,WIDTH//2-25, 250, 50, 40, 'Submit', 'small')
BACKBUTTON= button(GREY,WIDTH - 60  ,0,60,40, 'Back', 'small')
SIGNUPBUTTON= button(GREY, WIDTH - 190, 100, 100, 60, 'Sign Up','medium')
SUBMIT_SIGNUPBUTTON= button(GREY,WIDTH//2-25, 400, 50, 40, 'Submit', 'small')
WALLETBUTTON =button(GREY,0  ,0,125,40, 'Wallet/Settings', 'small')

BLACKJACKBUTTON =button(GREY,WIDTH//6-80 ,100,160,300)
ROULETTEBUTTON =button(GREY,WIDTH//2-80  ,100,160,300)
SLOTSBUTTON =button(GREY,WIDTH - WIDTH//6 - 80  ,100,160,300)
SIGNOUTBUTTON =button(GREY,WIDTH-60 ,0,60,40, 'Sign out', 'small')



#textbox inputs
USERNAME_INPUT_LOGIN = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200,150),(100,50)), manager=MANAGER_LI, object_id="#username_login")
PASSWORD_INPUT_LOGIN = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH-300,150),(100,50)), manager=MANAGER_LI, object_id="#password_login")
USERNAME_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100,150),(100,50)), manager=MANAGER_SU, object_id="#username_signup")
PASSWORD_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH-200,150),(100,50)), manager=MANAGER_SU, object_id="#password_signup")
FIRSTNAME_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100,250),(100,50)), manager=MANAGER_SU, object_id="#firstname_signup")
SURNAME_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH-200,250),(100,50)), manager=MANAGER_SU, object_id="#surname_signup")
AGE_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100,350),(100,50)), manager=MANAGER_SU, object_id="#age_signup")
EMAIL_INPUT_SIGNUP = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH-200,350),(100,50)), manager=MANAGER_SU, object_id="#email_signup")


#drawings
def drawing_MAIN():
    MAIN_MENU.fill(BLUE)
    MAIN_MENU.blit(LOGO, (WIDTH//2 - LOGO.get_width()//2, 20))
    LOGINBUTTON.draw(MAIN_MENU)
    SIGNUPBUTTON.draw(MAIN_MENU)
    LOGGING.blit(BGA,(WIDTH-BGA.get_width(), 470))
    pygame.display.update()

def drawing_LI():
    LOGGING.fill(BLUE)
    LOGGING.blit(LOGO, (WIDTH//2 - LOGO.get_width()//2, 20))
    BACKBUTTON.draw(LOGGING)
    SUBMIT_LOGINBUTTON.draw(LOGGING)
    USERNAME_LOGINRECT.draw(LOGGING)
    PASSWORD_LOGINRECT.draw(LOGGING)
    LOGGING.blit(BGA,(WIDTH-BGA.get_width(), 470))

def drawing_SU():
    LOGGING.fill(BLUE)
    LOGGING.blit(LOGO, (WIDTH//2 - LOGO.get_width()//2, 20))
    BACKBUTTON.draw(SIGNUP)
    PASSWORD_SIGNUPRECT.draw(SIGNUP)
    USERNAME_SIGNUPRECT.draw(SIGNUP)
    FIRSTNAME_SIGNUPRECT.draw(SIGNUP)
    SURNAME_SIGNUPRECT.draw(SIGNUP)
    AGE_SIGNUPRECT.draw(SIGNUP)
    EMAIL_SIGNUPRECT.draw(SIGNUP)
    SUBMIT_SIGNUPBUTTON.draw(SIGNUP)
    LOGGING.blit(BGA,(WIDTH-BGA.get_width(), 470))

def drawing_GAMES():
    BLUE=colourCheck()
    GAMES.fill(BLUE)
    GAMES.blit(LOGO, (WIDTH//2 - LOGO.get_width()//2, 20))
    GAMES.blit(BGA,(WIDTH-BGA.get_width(), 470))
    WALLETBUTTON.draw(GAMES)
    BLACKJACKBUTTON.draw(GAMES)
    ROULETTEBUTTON.draw(GAMES)
    SLOTSBUTTON.draw(GAMES)
    SIGNOUTBUTTON.draw(GAMES)
    GAMES.blit(SWEETLOGO,(WIDTH//2-80,170))
    GAMES.blit(SLOTLOGO,(WIDTH - WIDTH//6 - 80,170))
    GAMES.blit(BLACKJACKLOGO,(WIDTH//6-80,170))

def drawing_BLACKJACK(play,bet,hand,Total,DealerHand, pay=''):
    BLUE=colourCheck()
    global wallet
    FIVEBUTTON.draw(BLACKJACK)
    TENBUTTON.draw(BLACKJACK)
    TWENTYBUTTON.draw(BLACKJACK)
    FIFTYBUTTON.draw(BLACKJACK)
    HUNDEREDBUTTON.draw(BLACKJACK)
    STANDBUTTON.draw(BLACKJACK)
    if play == 'stop':
        PLAYBUTTON.draw(BLACKJACK)
    if play == 'start':
        HITBUTTON.draw(BLACKJACK)

    BLACKJACK.fill(BLUE)
    TABLERECT.draw(BLACKJACK)
    wallet = str(blackjack.GetWallet(Username, database))
    BALANCERECT =rectangle(GREY,0  ,0,60,40, wallet, 'very small')
    BALANCERECT.draw(BLACKJACK)
    BACKBUTTON.draw(BLACKJACK)
    FIVECIRCLE.draw(BLACKJACK)
    TENCIRCLE.draw(BLACKJACK)
    TWENTYCIRCLE.draw(BLACKJACK)
    FIFTYCIRCLE.draw(BLACKJACK)
    HUNDREDCIRCLE.draw(BLACKJACK)
    STANDCIRCLE.draw(BLACKJACK)
    if play == 'stop':
        PLAYCIRCLE.draw(BLACKJACK)
    if play == 'start':
        HITCIRCLE.draw(BLACKJACK)
    BETVALRECT= WALLETFONT.render('Bet: '+ str(bet),True, BLACK)
    BLACKJACK.blit(BETVALRECT,(WIDTH//2- 50,HEIGHT - 30))
    draw_card(hand)
    draw_dealer_card(DealerHand,play)
    


    if Total > 21 and play != 'game over':
        EMPTY= ERRORFONT.render('You have gone bust',True,RED)
        BLACKJACK.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,130))
        play = 'pause'
    elif Total == 21 and play != 'game over':
        EMPTY= ERRORFONT.render('You hit 21',True,GREEN)
        BLACKJACK.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,130))
        play = 'pause'
    if play == 'game over':
        EMPTY = ERRORFONT.render('press on the below message to play again',True,RED)
        BLACKJACK.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,10))
    if pay == 'p':
        WINRECT.draw(BLACKJACK)
    elif pay == 'push':
        PUSHRECT.draw(BLACKJACK)
    elif pay == 'd':
        LOSERECT.draw(BLACKJACK)
    return play

def drawing_SLOTS(slot,icons,bet):
    BLUE=colourCheck()
    SLOTPLAYBUTTON.draw(SLOTS)
    FIVEBUTTON.draw(SLOTS)
    ONEBUTTON.draw(SLOTS)
    TENBUTTON.draw(SLOTS)
    TWENTYBUTTON.draw(SLOTS)
    FIFTYBUTTON.draw(SLOTS)
    HUNDEREDBUTTON.draw(SLOTS)
    SLOTS.fill(BLUE)
    SLOTSTABLERECT.draw(SLOTS)
    BETVALRECT= WALLETFONT.render('Bet: '+ str(bet),True, BLACK)
    SLOTS.blit(BETVALRECT,(WIDTH//2- 50,HEIGHT - 30))
    BACKBUTTON.draw(SLOTS)
    ONECIRCLE.draw(SLOTS)
    FIVECIRCLE.draw(SLOTS)
    TENCIRCLE.draw(SLOTS)
    TWENTYCIRCLE.draw(SLOTS)
    FIFTYCIRCLE.draw(SLOTS)
    HUNDREDCIRCLE.draw(SLOTS)
    wallet = str(blackjack.GetWallet(Username, database))
    BALANCERECT =  rectangle(GREY,0  ,0,60,40, wallet, 'very small')
    BALANCERECT.draw(SLOTS)
    SLOTS.blit(slots.SLOTMACHINE,(WIDTH//2 - 197,5))
    x= WIDTH//2-134
    y=191
    for z in range(len(icons)):
        icon=pygame.transform.scale(pygame.image.load(os.path.join('assets','slots',slot[int(icons[z])] + '.png')),(52,52))
        SLOTS.blit(icon,(x,y))
        x+= 110

def drawing_SWEET(slot,slotGRID,bet,winnings):
    PLAYBUTTON.draw(SWEET)   
    FIVEBUTTON.draw(SWEET)
    TENBUTTON.draw(SWEET)
    TWENTYBUTTON.draw(SWEET)
    FIFTYBUTTON.draw(SWEET)
    HUNDEREDBUTTON.draw(SWEET)
    SWEET.blit(SWEETBACKGROUND,(0,0))
    SWEET.blit(SWEETFRAME,(WIDTH//2-240,5))
    BETVALRECT= WALLETFONT.render('Bet: '+ str(bet),True, BLACK)
    SWEET.blit(BETVALRECT,(WIDTH//2- 50,HEIGHT - 30))    
    BACKBUTTON.draw(SWEET)
    FIVECIRCLE.draw(SWEET)
    TENCIRCLE.draw(SWEET)
    TWENTYCIRCLE.draw(SWEET)
    FIFTYCIRCLE.draw(SWEET)
    HUNDREDCIRCLE.draw(SWEET)
    PLAYCIRCLE.draw(SWEET)
    WIN= WINFONT.render('WIN $'+ str(winnings),True,BLACK)
    LOGGING.blit(WIN, (WIDTH//2 - WIN.get_width()//2,380))
    wallet = str(blackjack.GetWallet(Username, database))
    BALANCERECT =  rectangle(GREY,0  ,0,60,40, wallet, 'very small')
    BALANCERECT.draw(SWEET)


    x=WIDTH//2 - 240
    for m in range(len(slotGRID)):
        y=305
        for n in range(len(slotGRID[m])):
            icon = pygame.transform.scale(pygame.image.load(os.path.join('assets','sweet',slotGRID[m][n] + '.png')),(75,75))
            SWEET.blit(icon,(x,y))
            y -=75
        x+= 75
    pygame.display.update()
        
def draw_card(hand):
    y=200
    z=250
    if hand== []:
        pass
    else:
        for x in range(len(hand)):
            card= pygame.transform.scale(pygame.image.load(os.path.join('assets','cards',hand[x][1], hand[x][0]+ '_of_'+ hand[x][1]+'.png')),(100,145))
            BLACKJACK.blit(card,(y,z))
            y+=50
            z-=20

def draw_dealer_card(DealerHand,start):
    y=200
    z=25
    if DealerHand == []:
        pass
    elif len(DealerHand) < 3 and len(DealerHand) > 0:
        if start == 'game over':
            card= pygame.transform.scale(pygame.image.load(os.path.join('assets','cards',DealerHand[0][1], DealerHand[0][0] + '_of_'+ DealerHand[0][1]+'.png')),(100,145))
        else:
            card= pygame.transform.scale(pygame.image.load(os.path.join('assets','cards','reverse.png')),(100,145))
        BLACKJACK.blit(card,(y,z))
        y+=50
        if len(DealerHand) == 2:
            card= pygame.transform.scale(pygame.image.load(os.path.join('assets','cards',DealerHand[1][1], DealerHand[1][0] + '_of_'+ DealerHand[1][1]+'.png')),(100,145))
            BLACKJACK.blit(card,(y,z))
        
    else:
        for x in range(len(DealerHand)):
            y+=50
            card= pygame.transform.scale(pygame.image.load(os.path.join('assets','cards',DealerHand[x][1], DealerHand[x][0]+ '_of_'+ DealerHand[x][1]+'.png')),(100,145))
            BLACKJACK.blit(card,(y,z))

#functionality functions
def mouse_placement():
    MOUSE_POS = pygame.mouse.get_pos()
    return MOUSE_POS

def bet_checking_blackjack(bet):
    check= blackjack.PlaceBet(Username,database,bet)
    if check == 'broke':
        EMPTY= ERRORFONT.render('You cannot afford to place that bet',True,RED)
        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,220))
        pygame.display.update()
        time.sleep(2)
    else:
        return bet

def bet_checking_slots(bet):
    check= slots.PlaceBet(Username,database,bet)
    if check == 'broke':
        EMPTY= ERRORFONT.render('You cannot afford to place that bet',True,RED)
        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,63 - EMPTY.get_height()//2))
        pygame.display.update()
        time.sleep(2)
    else:
        return bet
        
def bet_checking_sweet(bet):
    check= slots.PlaceBet(Username,database,bet)
    if check == 'broke':
        EMPTY= ERRORFONT.render('You cannot afford to place that bet',True,RED)
        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,80 - EMPTY.get_height()//2))
        pygame.display.update()
        time.sleep(2)
    else:
        return bet

def sweet_checker(slotGRID,slot,bet,winnings):
    count = 1
    while count > 0:
        slotGRID, count, payout = sweet.seven_check(slotGRID,slot,bet)
        winnings += payout
        print(slotGRID)
        print(count)
        count = int(count)
        drawing_SWEET(slot,slotGRID,bet,winnings)
        time.sleep(0.5)
    wallet = int(blackjack.GetWallet(Username, database))
    wallet+=winnings
    database.execute("UPDATE USERS SET Wallet = ? WHERE Username =?",[wallet,Username])
    database.commit()


    return slotGRID, winnings
  
#windows
def window_SU():
    global username_input
    global password_input
    global Username
    runB = True
    MOUSE_POS = mouse_placement()
    username_input=''
    password_input=''
    firstname_input=''
    surname_input=''
    age_input=''
    email_input=''
    while runB:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runB = False
                pygame_gui.UI_TEXT_BOX_LINK_CLICKED
            #checks if the text boxes have a change in input
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#username_signup':
                username_input = event.text
                print('username')

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#password_signup':
                password_input = event.text
                print('password')
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#firstname_signup':
                firstname_input = event.text
                print('firstname')
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#surname_signup':
                surname_input = event.text
                print('surname')
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#age_signup':
                age_input = event.text
                print('age')
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#email_signup':
                email_input = event.text
                print('email')

            if event.type == pygame.MOUSEBUTTONDOWN:                
                if BACKBUTTON.isOver(MOUSE_POS):
                    window_MM()
                
                if SUBMIT_SIGNUPBUTTON.isOver(MOUSE_POS):
                    #checking the boxes are all filled in
                    if username_input=='' or password_input == '' or firstname_input =='' or surname_input == '' or age_input == '' or email_input == '':
                        EMPTY= ERRORFONT.render('Fill in all fields',True,RED)
                        SIGNUP.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,370))
                        pygame.display.update()
                        time.sleep(1.5)
                    else:
                        Username = LandS.SignUp(username_input,password_input,firstname_input,surname_input,age_input,email_input)
                        if Username == 'clashing':
                            CLASH= ERRORFONT.render('An account with that username already exists',True,RED)
                            SIGNUP.blit(CLASH, (WIDTH//2 - CLASH.get_width()//2,370))
                            pygame.display.update()
                            time.sleep(1.5)
                            #username already exists popup
                        elif Username == 'underage':
                            UNDERAGE= ERRORFONT.render('You must be 18+ to gamble',True,RED)
                            SIGNUP.blit(UNDERAGE, (WIDTH//2 - UNDERAGE.get_width()//2,370))
                            pygame.display.update()
                            time.sleep(1.5)
                            #must be 18+ to gamble
                        elif Username == 'number':
                            NUMBER= ERRORFONT.render('Enter digits for your age',True,RED)
                            SIGNUP.blit(NUMBER, (WIDTH//2 - NUMBER.get_width()//2,370))
                            pygame.display.update()
                            time.sleep(1.5)
                            #number must be entered in age box
                        elif Username == 'email':
                            EMAIL= ERRORFONT.render('enter a valid email',True,RED)
                            SIGNUP.blit(EMAIL, (WIDTH//2 - EMAIL.get_width()//2,370))
                            pygame.display.update()
                            time.sleep(1.5)
                            #email must be valid
                        else:
                            SUCCESS= ERRORFONT.render('Successfully signed up',True,GREEN)
                            SIGNUP.blit(SUCCESS, (WIDTH//2 - SUCCESS.get_width()//2,370))
                            SIGNUP.blit(BGAHELPLINE, (WIDTH//2 - BGAHELPLINE.get_width()//2,75))
                            pygame.display.update()
                            time.sleep(2)
                            window_GAMES()                        

            MANAGER_SU.process_events(event)
        
        MANAGER_SU.update(UI_REFRESH_RATE)
        MOUSE_POS = mouse_placement()
        drawing_SU()
        MANAGER_SU.draw_ui(SIGNUP)
        pygame.display.update()
    pygame.quit()

def window_LI():
    global username_input
    global password_input
    global Username
    runA = True
    MOUSE_POS = mouse_placement()
    username_input=''
    password_input=''
    while runA:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runA= False
                
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#username_login':
                username_input = event.text
                print(username_input)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#password_login':
                password_input = event.text
                print(password_input)

            if event.type == pygame.MOUSEBUTTONDOWN:                
                if BACKBUTTON.isOver(MOUSE_POS):
                    window_MM()
                if SUBMIT_LOGINBUTTON.isOver(MOUSE_POS):
                    print('lool')
                    print(username_input)
                    print('p',password_input)
                    if username_input == '' or password_input == '':
                        print('nope')
                        EMPTY= ERRORFONT.render('Fill in all fields',True,RED)
                        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,220))
                        pygame.display.update()
                        time.sleep(2)
                    else:
                        Username = LandS.LogIn(username_input, password_input)
                        print('yooo')
                        if Username == 'wrong':
                            print('try again')
                            INCORRECT =ERRORFONT.render('Username or password is incorrect',True,RED)
                            LOGGING.blit(INCORRECT, (WIDTH//2  - INCORRECT.get_width()//2,220))
                            pygame.display.update()
                            time.sleep(1.5)
                        else:
                            SUCCESS= ERRORFONT.render('Successfully logged in',True,GREEN)
                            SIGNUP.blit(SUCCESS, (WIDTH//2 - SUCCESS.get_width()//2,370))
                            LOGGING.blit(BGAHELPLINE, (WIDTH//2 - BGAHELPLINE.get_width()//2,75))
                            pygame.display.update()
                            time.sleep(2)
                            window_GAMES()         
            
            MANAGER_LI.process_events(event)
        
        MANAGER_LI.update(UI_REFRESH_RATE)
        MOUSE_POS = mouse_placement()
        drawing_LI()
        MANAGER_LI.draw_ui(LOGGING)
        pygame.display.update()
    pygame.quit()

def window_MM():
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:                
                if LOGINBUTTON.isOver(MOUSE_POS):
                    window_LI()
                    

                if SIGNUPBUTTON.isOver(MOUSE_POS):
                    window_SU()
                    
        MOUSE_POS = mouse_placement()
        drawing_MAIN()
        
    pygame.quit()

def window_WALLET():
    global username_input, password_input
    run = True
    
    while run:
        BLUE=colourCheck()
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:                
                if BACKBUTTON.isOver(MOUSE_POS):
                    window_GAMES()
        
        MOUSE_POS = mouse_placement()
        WALLET.fill(BLUE)
        WALLET.blit(LOGO, (WIDTH//2 - LOGO.get_width()//2, 20))
        BACKBUTTON.draw(WALLET)
        WALLET.blit(BGA,(WIDTH-BGA.get_width(), 470))
        #retrives the value in the user's wallet
        wallet = str(blackjack.GetWallet(Username, database))
        BALANCE = WALLETFONT.render('$' + str(wallet), True, BLACK)
        WALLET.blit(BALANCE,(WIDTH//2- BALANCE.get_width()//2,250))
        BACKGROUNDRECT.draw(WALLET)
        COLOURPICKER.draw(WALLET)
        pygame.display.update()
        COLOURPICKER.update()
        
    pygame.quit()

def window_GAMES():
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:                
                if WALLETBUTTON.isOver(MOUSE_POS):
                    window_WALLET()
                    print('wallet')
                if SIGNOUTBUTTON.isOver(MOUSE_POS):
                    window_MM()
                if BLACKJACKBUTTON.isOver(MOUSE_POS):
                    window_BLACKJACK()
                if SLOTSBUTTON.isOver(MOUSE_POS):
                    window_SLOT()
                if ROULETTEBUTTON.isOver(MOUSE_POS):
                    window_SWEET()
        
        MOUSE_POS = mouse_placement()
        drawing_GAMES()
        pygame.display.update()
    pygame.quit()

def window_BLACKJACK():
    global hand,DealerHand,Total,DealerHand,bet
    bet=0
    pay =''
    start = 'stop'
    hand, DealerHand =[],[]
    print(hand)
    print(DealerHand)
    Total, DealerTotal =0,0
    print(Total)
    blackjackrun = True
    while blackjackrun:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:                
                if WALLETBUTTON.isOver(MOUSE_POS):
                    window_WALLET()
                    print('wallet')
                if BACKBUTTON.isOver(MOUSE_POS):
                    blackjackrun = False
                    blackjack.reset()
                if start == 'stop':
                    #when button is pressed, checking the user can afford the bet
                    if FIVEBUTTON.isOver(MOUSE_POS):
                        bet+=bet_checking_blackjack(bet=5)
                    if TENBUTTON.isOver(MOUSE_POS):
                        bet+=bet_checking_blackjack(bet=10)
                    if TWENTYBUTTON.isOver(MOUSE_POS):
                        bet+=bet_checking_blackjack(bet=20)
                    if FIFTYBUTTON.isOver(MOUSE_POS):
                        bet+=bet_checking_blackjack(bet=50)
                    if HUNDEREDBUTTON.isOver(MOUSE_POS):
                        bet +=bet_checking_blackjack(bet=100)
                    if PLAYBUTTON.isOver(MOUSE_POS):
                        if bet == 0:
                            EMPTY= ERRORFONT.render('Place a bet to play',True,RED)
                            BLACKJACK.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,220))
                            pygame.display.update()
                            time.sleep(1)
                        else:
                            
                            blackjack.MakeDeck()
                            hand, Total = blackjack.SelectCard(hand,Total)
                            time.sleep(0.5)
                            drawing_BLACKJACK(start,bet,hand,Total,DealerHand)
                            pygame.display.update()
                            DealerHand, DealerTotal = blackjack.DealerCard(DealerHand,DealerTotal)
                            time.sleep(0.5)
                            start = drawing_BLACKJACK(start,bet,hand,Total,DealerHand)
                            pygame.display.update()
                            DealerHand, DealerTotal = blackjack.DealerCard(DealerHand,DealerTotal)
                            time.sleep(1)
                            start = 'start'
                if start == 'game over':
                    #determine which rectangle is which
                    if LOSERECT.isOver(MOUSE_POS):
                        print(hand)                      
                        window_BLACKJACK()                      
                    elif WINRECT.isOver(MOUSE_POS):
                        print(hand)
                        window_BLACKJACK()
                    elif PUSHRECT.isOver(MOUSE_POS):
                        print(hand)
                        window_BLACKJACK()
                if start == 'start':
                    if HITBUTTON.isOver(MOUSE_POS) and start == 'start':
                        hand, Total=blackjack.SelectCard(hand,Total)
                        print(Total)
                    if STANDBUTTON.isOver(MOUSE_POS) and start == 'start':
                        start = 'pause'

        MOUSE_POS = mouse_placement()
        if start == 'pause':
            if DealerTotal <18: 
                #checks if player has blackjack
                if Total == 21 and len(hand) == 2:
                    print('yo')
                    start = 'game over'
                    pay = blackjack.Deciding(DealerTotal,Total)
                    print(DealerTotal)
                    print(Total)
                    print(pay)
                    wallet = int(blackjack.GetWallet(Username, database))
                    blackjack.Payout(pay, Username, database,wallet,bet,hand,Total)
                elif Total > 21:
                    print('yo')
                    start = 'game over'
                    pay = blackjack.Deciding(DealerTotal,Total)
                    print(DealerTotal)
                    print(Total)
                    print(pay)
                    wallet = int(blackjack.GetWallet(Username, database))
                    blackjack.Payout(pay, Username, database,wallet,bet,hand,Total)
                else:
                    DealerHand,DealerTotal = blackjack.DealerCard(DealerHand,DealerTotal)
                    time.sleep(2)
            #checks if user or dealer has gone bust        
            elif Total >= 21 or DealerTotal >=   18:
                
                print('yo')
                start = 'game over'
                pay = blackjack.Deciding(DealerTotal,Total)
                print(DealerTotal)
                print(Total)
                print(pay)
                wallet = int(blackjack.GetWallet(Username, database))
                blackjack.Payout(pay, Username, database,wallet,bet,hand,Total)
                
        start = drawing_BLACKJACK(start,bet,hand, Total,DealerHand,pay)
        pygame.display.update()
        
    window_GAMES()

def window_SLOT():
    BLUE =colourCheck()
    slot=['casino','diamond','lemon','watermelon','cherry','apple']
    slotVAL=['0','0','0'] 
    run = True
    bet = 0
    SLOTS.fill(BLUE)
    SLOTSTABLERECT.draw(SLOTS)
    SLOTS.blit(slots.SLOTMACHINE,(WIDTH//2 - 197,5))
    EMPTY= ERRORFONT.render('Place a bet then on the red lever to play',True,RED)
    LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,63 - EMPTY.get_height()//2))
    pygame.display.update()
    time.sleep(1.2)
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if BACKBUTTON.isOver(MOUSE_POS):
                    window_GAMES()
                if WALLETBUTTON.isOver(MOUSE_POS):
                    window_WALLET()
                #checks if user can afford to place the bet         
                if ONEBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_slots(bet=1)
                if FIVEBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_slots(bet=5)
                if TENBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_slots(bet=10)
                if TWENTYBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_slots(bet=20)
                if FIFTYBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_slots(bet=50)
                if HUNDEREDBUTTON.isOver(MOUSE_POS):
                    bet +=bet_checking_slots(bet=100)
                if SLOTPLAYBUTTON.isOver(MOUSE_POS):
                    if bet > 0:
                        #Runs the slot machine if the user has placed a bet
                        slots.SLOT_RANDOM(SLOTS,WIDTH)   
                        slotVAL= slots.SLOT_GEN(slotVAL, SLOTS, WIDTH)
                        wallet = int(blackjack.GetWallet(Username, database))
                        slots.winning(slotVAL,bet,Username,database,wallet)
                        bet=0
                    else:
                        EMPTY= ERRORFONT.render('Place a bet to start playing',True,RED)
                        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,63 - EMPTY.get_height()//2))
                        pygame.display.update()
                        time.sleep(1.5)
                



        MOUSE_POS = mouse_placement()
        drawing_SLOTS(slot,slotVAL,bet)
        pygame.display.update()
    pygame.quit()

def window_SWEET():
    slot=['apple','banana','blue','grape','green','heart','plum','purple','watermelon']
    slotGRID=[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']] 
    run = True
    bet = 0
    slotGRID = sweet.grid_maker(slotGRID,slot)
    winnings=0

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: 
                #if button is pressed the specific function works
                if BACKBUTTON.isOver(MOUSE_POS):
                    window_GAMES()
                if WALLETBUTTON.isOver(MOUSE_POS):
                    window_WALLET()
                if FIVEBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_sweet(bet=5)
                if TENBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_sweet(bet=10)
                if TWENTYBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_sweet(bet=20)
                if FIFTYBUTTON.isOver(MOUSE_POS):
                    bet+=bet_checking_sweet(bet=50)
                if HUNDEREDBUTTON.isOver(MOUSE_POS):    
                    bet +=bet_checking_sweet(bet=100)
                if PLAYBUTTON.isOver(MOUSE_POS):
                    if bet > 0:
                        #runs the grid/game functions
                        winnings=0
                        slotGRID = sweet.grid_maker(slotGRID,slot)
                        drawing_SWEET(slot,slotGRID,bet, winnings)
                        time.sleep(2)
                        slotGRID, winnings = sweet_checker(slotGRID,slot,bet,winnings)
                        bet=0
                    else:
                        EMPTY= ERRORFONT.render('Place a bet to start playing',True,RED)
                        LOGGING.blit(EMPTY, (WIDTH//2 - EMPTY.get_width()//2,80 - EMPTY.get_height()//2))
                        pygame.display.update()
                        time.sleep(1.5)    
                        


                
        MOUSE_POS = mouse_placement()
        drawing_SWEET(slot,slotGRID,bet,winnings)
        pygame.display.update()
    pygame.quit()

window_MM()





