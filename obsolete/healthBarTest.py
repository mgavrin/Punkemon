import pygame
from pygame.locals import *
import math
from math import *
import os

def getHealthBar(cellsLong,value):
        #takes a length in cells and a floating point (0,1] fraction-of-health-left
        #returns a surface for blitting
        healthBarSurface=pygame.Surface((pixel*cellsLong,pixel),0,32)
        barLength=(cellsLong-2)*pixel+2*pixel*11/15
        posBarLength=ceil(barLength*value) #length in (screen, not game) pixels that is full
        negBarLength=barLength-posBarLength
        if value>=0.5:
            color=(78,171,24)
        elif value>=0.1:
            color=(244,232,61)
        else:
            color=(227,85,14)
        #draw the positive bar
        healthBarSurface.fill(color,Rect(4,4,posBarLength,6))
        #draw the negative bar
        healthBarSurface.fill((255,255,255),Rect(4+posBarLength,4,negBarLength,6))
        #draw the left end
        healthBarSurface.blit(healthBarLeft,(0,0))
        #draw the right end
        healthBarSurface.blit(healthBarRight,(pixel*(cellsLong-1),0))
        #draw the middle
        for i in range(1,cellsLong-1):
            healthBarSurface.blit(healthBarMiddle,(pixel*i,0))
        return healthBarSurface


pixel=15
pygame.init()
screenSize=(200,200)
healthBarLeft=pygame.image.load(os.path.join("sprites","barEndLeft.png"))
healthBarRight=pygame.image.load(os.path.join("sprites","barEndRight.png"))
healthBarMiddle=pygame.image.load(os.path.join("sprites","barMiddle.png"))
gameScreen=pygame.display.set_mode(screenSize,0,32)
gameScreen.blit(getHealthBar(7,0.0),(0,0))
gameScreen.blit(getHealthBar(7,0.09),(0,20))
gameScreen.blit(getHealthBar(7,0.4),(0,40))
gameScreen.blit(getHealthBar(7,0.6),(0,60))
gameScreen.blit(getHealthBar(7,0.8),(0,80))
gameScreen.blit(getHealthBar(7,1.0),(0,100))
pygame.display.flip()
