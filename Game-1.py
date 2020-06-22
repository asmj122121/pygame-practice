import numpy as np
import os
import sys
import pygame                   # import the pygame module
import random                   # import random for random numbers!
import time
from pygame.locals import *     # import pygame.locals for easier access to key coordinates

# def ShowScore(score):
#    font=pygame.font.Font(None,30)
#    scoretext=font.render("bossHP:"+str(score), 1,(255,255,255))
#    screen.blit(scoretext, (500, 457))

if getattr(sys, 'frozen', False):  #如果是exe文件
    root = os.path.dirname(sys.executable)
elif __file__:
    root = os.path.dirname(__file__)

def ShowBossHP(HP):
    HP = HP*600/100
    pygame.draw.rect(screen,[255,0,0],[100,100,HP,20],0)

def ShowPlayerlife(playerlife):
   font=pygame.font.Font(None,30)
   playerlifetext=font.render("PlayerLife:"+str(playerlife), 1,(255,255,255))
   screen.blit(playerlifetext, (500, 300))

def prtectmode():
   font=pygame.font.Font(None,30)
   prtectmodetext=font.render("protectmode", 1,(255,255,255))
   screen.blit(prtectmodetext, (500, 350))

def name():
   font=pygame.font.Font("C:\Windows\Fonts\msjh.ttc",30)
   nametext=font.render("北科大-107810029-蔡易展", 1,(5,5,5))
   screen.blit(nametext, (50, 457))

class attach(pygame.sprite.Sprite):
    def __init__(self):
        super(attach, self).__init__()
        self.image = pygame.image.load(os.path.join(root,'attach.png')).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(player.place_l() + 3,player.place_t()))

    def update(self):
        self.rect.move_ip(0,-10)
        if self.rect.top <= 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((6,6))
        # self.surf.fill((254,254,254))
        # self.surf.blit(self.image,[100,150])
        # self.rect = self.surf.get_rect(center=(400, 500))
        self.image = pygame.image.load(os.path.join(root,'123.png')).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(400,500)) 

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:        # Keep player on the screen
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
    def place_l(self) :
        return self.rect.left
    def place_r(self) :
        return self.rect.right
    def place_t(self) :
        return self.rect.top
    def place_b(self) :
        return self.rect.bottom

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.image = pygame.image.load(os.path.join(root,'rumia.png')).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(player.place_l() + 3,player.place_t()))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < -10:        # Keep player on the screen
            self.rect.left = -10
        elif self.rect.right > 810:
            self.rect.right = 810
        if self.rect.top <= -13:
            self.rect.top = -13
        elif self.rect.bottom >= 610:
            self.rect.bottom = 610

class Enemy(pygame.sprite.Sprite):              #直線等速子彈
    def __init__(self,direct):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(os.path.join(root,'missile.png')).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.directx = np.sin(direct*np.pi/180.0)
        self.directy = np.cos(direct*np.pi/180.0)
        self.rect = self.image.get_rect(center=(boss.place_x(),boss.place_y()))
        self.speed = 7.0
        self.placex = boss.place_x()
        self.placey = boss.place_y()
        self.lastx = boss.place_x()
        self.lasty = boss.place_y()

    def update(self):
        self.placex += self.speed*self.directx
        self.placey += self.speed*self.directy
        self.movex = self.placex - self.lastx
        self.movey = self.placey - self.lasty
        self.rect.move_ip(self.movex,self.movey)
        if (self.rect.top <= 0)or(self.rect.bottom >= 600)or(self.rect.left <= 0)or(self.rect.right >= 800):
            self.kill()
        self.lastx = (self.rect.left + self.rect.right)/2
        self.lasty = (self.rect.top + self.rect.bottom)/2

class Enemy2(pygame.sprite.Sprite):              #直線變速子彈
    def __init__(self,f,direct,x,y):
        super(Enemy2, self).__init__()
        self.image = pygame.image.load(os.path.join(root,'missile2.png')).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.directx = np.sin(direct*np.pi/180.0)
        self.directy = np.cos(direct*np.pi/180.0)
        self.rect = self.image.get_rect(center=(x,y))
        self.f = f
        self.speed = 4.0
        self.placex = x
        self.placey = y
        self.lastx = x
        self.lasty = y

    def update(self,frame):
        if (frame - self.f) >= 42 :
            self.speed = -7.0
        elif (frame - self.f) >= 84 :
            self.speed = 4.0
        self.placex += self.speed*self.directx
        self.placey += self.speed*self.directy
        self.movex = self.placex - self.lastx
        self.movey = self.placey - self.lasty
        self.rect.move_ip(self.movex,self.movey)
        if (self.rect.top <= 0)or(self.rect.bottom >= 600)or(self.rect.left <= 0)or(self.rect.right >= 800):
            self.kill()
        self.lastx = (self.rect.left + self.rect.right)/2
        self.lasty = (self.rect.top + self.rect.bottom)/2

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load(os.path.join(root,'furandoru.png')).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(100,100))           #random.randint(820, 900), random.randint(0, 600)
        self.speed = 0
        self.speed2 = 3.0
        self.speedx = 0
        self.speedy = 0
        self.a = 1     # 1左 -1右    # a指加速度
        self.placex = 300
        self.placey = 100
        self.lastx = 300
        self.lasty = 100

    def firstmove(self,f):
        if f > 119 :
            if f % 120 == 0:
                self.speed = 10
                self.a = -1
            if f % 120 == 60:
                self.speed = -10
                self.a = 1
            if(abs(self.speed) > 5):
                if(f % 10 == 0):
                    self.speed += self.a
            self.rect.move_ip(self.speed, 0)
    def secondmove(self,frame):
        self.directx = np.sin((-frame*np.pi/210.0)+90)
        self.directy = np.cos((-frame*np.pi/210.0)+90)
        self.placex += self.speed2*self.directx
        self.placey += self.speed2*self.directy
        self.movex = self.placex - self.lastx
        self.movey = self.placey - self.lasty
        self.rect.move_ip(self.movex,self.movey)
        self.lastx = (self.rect.left + self.rect.right)/2
        self.lasty = (self.rect.top + self.rect.bottom)/2


    def update(self):
        # self.rect.move_ip(self.speed, 0)
        # if self.rect.left < 0:
        #     self.speed = random.randint(2, 5)
        # elif self.rect.right > 800:
        #     self.speed = random.randint(-5, -2)

        if self.rect.left+55 > 403:
            self.speedx = -3
        elif self.rect.left+59 < 400:
            self.speedx = 3
        elif self.rect.top+59 > 103:
            self.speedy = -3
        elif self.rect.top+59 < 100:
            self.speedy = 3
        else :
            self.speedx = 0
            self.speedy = 0
        self.rect.move_ip(self.speedx , self.speedy)
    def place_x(self) :
        return self.rect.left+55
    def place_y(self) :
        return self.rect.top+59

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))    # create the screen object    # here we pass it a size of 800x600
frame = 1
f = 0
y = 0
st = 0
sh = 0
blf = 0
bl2 = False
gamelevel = 0
bosslife = 3
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(root,'bgm.mp3'))
pygame.mixer.music.play(-1,0)

# ADDENEMY = pygame.USEREVENT + 1                 # Create a custom event for adding a new enemy.
# pygame.time.set_timer(ADDENEMY, 2000)

background = pygame.Surface(screen.get_size())
background = pygame.image.load(os.path.join(root,'background3.png'))

boss = Boss()
player = Player()                               # create our 'player', right now he's just a rectangle
player2 = Player2()   
playerlife = 3
protect = False
win = False
lose = False
shoot = False

attachs = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player2)
all_sprites.add(player)
all_sprites.add(boss)

clock = pygame.time.Clock()
running = True
nTotalEnemy = 0
bossHP = 100
timeBeginPlay = time.time()

while running:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        # elif event.type == ADDENEMY:
        #     timeCurrentNow = time.time()

    if win == False :

        #第一階段攻擊
        if bosslife == 3 :
            if (frame % 60 == 0 and frame > 119):
                shoot = True
            if (shoot == True):
                if (frame % 6 == 0):
                    for x in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180] :
                        new_enemy = Enemy(x)
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        new_enemy = Enemy(-x)
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                    sh += 1
                if (sh == 3):
                    shoot = False
                    sh = 0
            
        #第二階段攻擊
        if bosslife == 2:
            if ((frame) % 2 == 0):
                for x in [0,120,240] :
                    new_enemy2 = Enemy2(frame,x-y,boss.place_x(),boss.place_y())
                    enemies2.add(new_enemy2)
                    all_sprites.add(new_enemy2)
                y += 12

        #第三階段攻擊
        if bosslife == 1:
            if ((frame) % 20 == 0):
                rx = random.randint(100,700)
                ry = random.randint(100,400)
                for x in [0,60,120,180,240,300] :
                    new_enemy2 = Enemy2(frame,x-y,rx,ry)
                    enemies2.add(new_enemy2)
                    all_sprites.add(new_enemy2)
                y += 10

    enemies.update()
    enemies2.update(frame)
    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()

    if lose == False :
        if st <= 5 :
            if frame - f >= 5 :
                if pressed_keys[K_SPACE]:
                    new_attach = attach()
                    attachs.add(new_attach)
                    all_sprites.add(new_attach)
                    st += 1
        elif st > 5 :
            f = frame
            st = 0
        player.update(pressed_keys)
        player2.update(pressed_keys)
        attachs.update()

    if bosslife == 3 :
        boss.firstmove(frame)
    elif bosslife == 2 :
        if bl2 == False :
            blf = frame
            bl2 = True
        elif bl2 == True :
            boss.secondmove(frame - blf)
    elif bosslife == 1 :
        boss.update()
    # if(frame > 637 and frame <= 837):
    #     boss.secondmove(frame)
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    if win == False :
        if playerlife == 0:
            player.kill()
            player2.kill()
            lose = True
            background = pygame.image.load(os.path.join(root,'you lose.png'))
    if protect == False :
        if playerlife > 0 and pygame.sprite.spritecollideany(player, enemies or enemies2):
            playerlife -= 1
            pstrtime = frame
            protect = True
    elif protect == True :
        prtectmode()
        if frame >= (90 + pstrtime) :
            protect = False


    if lose == False :
        if bosslife <= 0 :
            boss.kill()
            win = True
            background = pygame.image.load(os.path.join(root,'you win.png'))

    if lose == False and win == False :
        # ShowScore(bossHP)
        ShowBossHP(bossHP)
        ShowPlayerlife(playerlife)
        if pygame.sprite.spritecollideany(boss, attachs):
            bossHP -= 1
        if bossHP <= 0 :
            bosslife -= 1
            bossHP = 100
    name()
    pygame.display.flip()
    frame += 1