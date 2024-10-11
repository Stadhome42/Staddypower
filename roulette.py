import pygame
import os
import pygame_gui
import time
import random
from assets.cards.creation import *

pygame.init()

WIDTH, HEIGHT = 1500, 750
pygame.display.set_caption("StaddyPower")
bet=1000000
ROULETTE = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255,255,255)
BLUE = (102, 212, 255)
RED = (220,20,60)
ORANGE =(255,128,0)
YELLOW =(255,255,0)
PINK = (255,131,250)
GREEN = (0,100,0)
GREY = (220,220,220)
BLACK=(0,0,0)
clock = pygame.time.Clock()
FPS = 30

WHEEL = pygame.transform.scale(pygame.image.load(os.path.join('Assets','wheel.png')),(576,474))
w,h = WHEEL.get_size()
new_rect = WHEEL.get_rect(center=WHEEL.get_rect(topleft=(100,150)).center)

def mouse_placement():
    MOUSE_POS = pygame.mouse.get_pos()
    return MOUSE_POS

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
    def __init__(self,colour, X, Y, width, height, text='',size='',):
        self.color = colour
        self.x = X
        self.y = Y
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.colour = colour

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
            text = font.render(self.text, 1, (255,255,255))
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


LOGINBUTTON = button(GREY, 150, 100, 100, 60, 'Log in', 'medium')
PLAYBUTTON= button((0,0,0),150,575+10,80,80)
PLAYCIRCLE= circle(GREEN,200,620+10,50,50,'PLAY','medium')



def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    return rotated_image, new_rect


def draw_roulette(clock,play):
    global WHEEL, new_rect
    PLAYBUTTON.draw(ROULETTE)
    ROULETTE.fill(BLUE)
    PLAYCIRCLE.draw(ROULETTE)
    if play == True:
        WHEEL, new_rect= blit_rotate_center(ROULETTE,WHEEL,new_rect.topleft,2)
    ROULETTE.blit(WHEEL,new_rect.topleft)
    x=700
    y=293
    for z in range(1,37):
        
        if z%2 == 0:
            colour= BLACK
        else:
            colour= RED
        SQUARE = rectangle(colour, x, y, 55, 55, str(z), 'medium')
        SQUARE.draw(ROULETTE)
        y+=55
        if z % 3 ==0:
            x+=55
            y=293

    pygame.display.update()




def roulette():
    start_time = None
    time_since_enter=0
    play= False
    run = True
    while run == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAYBUTTON.isOver(MOUSE_POS):
                    start_time = pygame.time.get_ticks()
                    play = True
                    print(start_time)
        if start_time != None:
            time_since_enter = pygame.time.get_ticks() - start_time  
        if play == True and time_since_enter >= 5000:
            play == False
            start_time = None

        MOUSE_POS=mouse_placement()
        draw_roulette(clock,play)
    pygame.quit()


roulette()