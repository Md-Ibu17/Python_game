import os
import math 
import pygame
import random
'''
Below two lines is for,
instead of dynamilcally loading each file and images
'''
from os import listdir
from os.path import isfile,join
#pygame module initialization
pygame.init()
#window name or caption for the game
pygame.display.set_caption("platformer")

#Defining few global variables

WIDTH,HEIGHT= 1000,800
FPS=60
PLAYER_VELOCITY = 5

window = pygame.display.set_mode((WIDTH,HEIGHT))

#Flip sprites
def flip(sprites):
    return [pygame.transform.flip(sprite,True,False) for sprite in sprites]
#####END#####
#Load sprite sheets:
def Load_sprite_sheets(dir1,dir2,width,height,direction=False):
    path = join("assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites ={}
    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites=[]
        for i in range(sprite_sheet.get_width()//width):
            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png","")+"_right"] = sprites
            all_sprites[image.replace(".png","")+"_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites
     
#####END#####
#GENERATING GAME PLAYER:
class Player(pygame.sprite.Sprite):
    COLOR = (0,250,0)
    GRAVITY = 1
    SPRITES = Load_sprite_sheets("MainCharacters","NinjaFrog",32,32,True)
    def __init__(self,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count=0
        self.fall_count = 0
    
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,vel):  
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self,fps):
        #self.y_vel += min(1,(self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fall_count +=1 

    def draw(self,win):
        self.sprite = self.SPRITES["idle_"+ self.direction][0]
        win.blit(self.sprite,(self.rect.x,self.rect.y))
##### END#######

#MOVING THE PLAYER##
def handle_move(player):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VELOCITY)

##### END ###### 

#back_ground DRAWING:
def get_background(name):
    image = pygame.image.load(join("assets","Background",name))            #Loading the backgound images
    _,_,width,height = image.get_rect()                                    #width,height == tiles images width and height(the get_rect() will get the width and height ) 
    tiles=[]
    for i in range(WIDTH//width+1):
        for j in range(HEIGHT//height+1):
            pos=(i*width,j*height)
            tiles.append(pos)
    return tiles,image  


 #Creating a function to draw the background:
def draw(window,background,bg_image,player):
    for tile in background:
        window.blit(bg_image,tile)
    player.draw(window)
    pygame.display.update()            



#main window function
def main(window):
    clock = pygame.time.Clock()
    background,bg_image = get_background("Blue.png")

    player = Player(100,100,50,50)
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)
        draw(window,background,bg_image,player)
    pygame.quit()
    quit()
if __name__== "__main__":
    main(window)
