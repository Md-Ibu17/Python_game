import os
import math 
import pygame
import random

from pygame.sprite import Group
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
##block function##
def get_block(size):
    path = join("assets","Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect = pygame.Rect(96,0,size,size)
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale2x(surface)
###END####
#GENERATING GAME PLAYER:
class Player(pygame.sprite.Sprite):
    COLOR = (0,250,0)
    GRAVITY = 1
    SPRITES = Load_sprite_sheets("MainCharacters","NinjaFrog",32,32,True)
    ANIMATION_DELAY = 2

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
        self.y_vel += min(1,(self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.update_sprite()
        self.fall_count +=1 

    #### collision functions ####
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    def hit_head(self):
        self.count=0
        self.y_vel *= -1
    ####END####
   #ANIMATING THE PLAYER:
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count//self.ANIMATION_DELAY)%len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count+=1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self,win):
        win.blit(self.sprite,(self.rect.x,self.rect.y))
##### END#######

### Another class ###
class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    def draw(self,win):
        win.blit(self.image,(self.rect.x,self.rect.y))
####END#########

####ADDING TERRAIN AND BLOCK####
class Block(Object):
    def __init__(self, x, y,size):
        super().__init__(x, y,size,size)
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)
#####END########

###PIXEL PERFECT COLLISION(VERTICAL)####
def handle_vertical_collision(player,objects,dy):
    colllided_objects =[]
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            if dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        colllided_objects.append(obj)
    return colllided_objects


#####END######
#MOVING THE PLAYER##
def handle_move(player,objects):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VELOCITY)
    handle_vertical_collision(player,objects,player.y_vel)

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
def draw(window,background,bg_image,player,objects):
    for tile in background:
        window.blit(bg_image,tile)
    
    for obj in objects:
        obj.draw(window)
    
    player.draw(window)
    
    pygame.display.update()            



#main window function
def main(window):
    clock = pygame.time.Clock()
    background,bg_image = get_background("Blue.png")
    
    block_size = 96

    player = Player(100,100,50,50)
    floor = [Block(i*block_size,HEIGHT-block_size,block_size) for i in range(-WIDTH//block_size,(WIDTH*2)//block_size)]
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player,floor)
        draw(window,background,bg_image,player,floor)
    pygame.quit()
    quit()
if __name__== "__main__":
    main(window)
