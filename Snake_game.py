import pygame
import time
from pygame.locals import *
import sys
from random import randint

size=40

class Snake():
    def __init__(self,surface,length):
        self.length=length
        self.surface=surface
        self.face=pygame.image.load("./images/block.jpg").convert()
        self.x=[size]*length
        self.y=[size]*length
        self.width=1000
        self.height=500
        self.d=""
    
    def block(self):
        for i in range(self.length):
            self.surface.blit(self.face,(self.x[i],self.y[i]))
        pygame.display.flip()

    def new_block(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    
    def action(self):
        print(self.x,self.y)
        self.surface.fill((110,110,5))
        for i in range(self.length):
            self.surface.blit(self.face,(self.x[i],self.y[i]))
        pygame.display.flip()
    
    def up(self):
        self.d="U"

    def down(self):
        self.d="D"

    def left(self):
        self.d="L"
    
    def right(self):
        self.d="R"
        
        
    def move(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        if self.d=="U":
            self.y[0]-=size
            if self.y[0]<0:
                self.y[0]=self.height
            self.action()
        if self.d=="D":
            self.y[0]+=size
            if self.y[0]>self.height-size:
                self.y[0]=0
            self.action()
        if self.d=="R":
            self.x[0]+=size
            if self.x[0]>self.width-size:
                self.x[0]=0
            self.action()
        if self.d=="L":
            self.x[0]-=size
            if self.x[0]<0:
                self.x[0]=self.width
            self.action()

class food():
    def __init__(self,surface):
        self.surface=surface
        self.face=pygame.image.load("./images/apple.gif").convert()
        self.x=500
        self.y=40
        self.width=1000
        self.height=500

    def block(self):
        self.surface.blit(self.face,(self.x,self.y))
        pygame.display.flip()
    
    def newapple(self):
        self.x=randint(0,self.width//size)*(size-4)
        self.y=randint(0,self.height//size)*(size-4)
        print(self.x,self.y)


class First():
    def __init__(self,surface):
        self.surface=surface
        self.name_font = pygame.font.SysFont('Helvetica', 50)
        self.surface.fill((0,0,0))
        self.running=False
        
    def to_display(self):
        self.name = self.name_font.render("Game programming with Python", True, (255,255,55))
        self.space = self.name_font.render("Press SPACE to START",True,(255,255,55))
        self.surface.blit(self.name, (100,100))
        self.surface.blit(self.space,(100,400))
        pygame.display.flip()
    
    def action(self):
        for i in pygame.event.get():
            if i.type==KEYDOWN:
                if i.key==K_SPACE:
                    print("running")
                    self.running=True
                else:
                    pygame.quit()
                    sys.exit()
            elif i.type==QUIT:
                pygame.quit()
                sys.exit()
    

class Main_Game():
    def __init__(self):
        pygame.init()
        self.width=1000
        self.height=500
        self.surface=pygame.display.set_mode((self.width,self.height))
        self.name_font = pygame.font.SysFont('Helvetica', 20)

    def collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+size:
            if y1>=y2 and y1<y2+size:
                return True
        return False
    
    def gameover(self):
        self.surface.fill((110,110,5))
        self.end_font = pygame.font.SysFont('Helvetica', 50)
        self.a=str(self.snake.length-1)
        self.score_display = self.end_font.render("Game Over! Your Score:"+self.a, True, (0,0,55))
        self.surface.blit(self.score_display,(self.width//4,self.height//2))
        pygame.display.flip()
        self.running=False
    
    def score(self):
        self.a=str(self.snake.length-1)
        self.name = self.name_font.render("Score:"+self.a, True, (0,0,55))
        self.surface.blit(self.name,(self.width-200,self.height-(self.height-20)))
        pygame.display.flip()
    
    def play(self):
        first=First(self.surface)
        first.to_display()
        while not first.running:
            first.action()
        self.surface.fill((110,110,5))
        self.snake=Snake(self.surface,1)
        self.snake.block()
        self.apple=food(self.surface)
        self.apple.block()
        self.score()
        self.flag=0
        while True:
            for i in pygame.event.get():
                if i.type==KEYDOWN:
                    if i.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if i.key==K_UP or i.key==K_w:
                        self.snake.up()
                    if i.key==K_LEFT or i.key==K_a:
                        self.snake.left()
                    if i.key==K_DOWN or i.key==K_s:
                        self.snake.down()
                    if i.key==K_RIGHT or i.key==K_d:
                        self.snake.right()
                elif i.type==QUIT:
                    pygame.quit()
                    sys.exit()
            self.snake.move()
            self.apple.block()
            if self.collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
                self.apple.newapple()
                self.snake.new_block()
            for i in range(1,self.snake.length):
                if self.collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                   self.gameover()
                   self.flag+=1
                   while not self.running:
                    for i in pygame.event.get():
                        if i.type==KEYDOWN:
                            if i.key==K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                            if i.key==K_r:
                                self.flag=0
                                self.play()
                                print(self.snake.length)
                        elif i.type==QUIT:
                            pygame.quit()
                            sys.exit()
            if self.flag!=0:
                break                    
            self.score()
            time.sleep(0.5)

if __name__=="__main__":
    game=Main_Game()
    game.play()