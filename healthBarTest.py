import pygame
from pygame.locals import *
import math
from math import *
import os

def getHealthBar(cellsLong,cellsHigh,value):
        #takes a length and height in cells and a floating point (0,1] fraction-of-health-left
        #returns a surface for blitting
        healthBarSurface=pygame.Surface((pixel*cellsLong,pixel*cellsHigh),0,32)
        barLength=(cellsLong-2*cellsHigh)*pixel+2*cellsHigh*pixel*11/15
        posBarLength=ceil(barLength*value) #length in (screen, not game) pixels that is full
        negBarLength=barLength-posBarLength
        if value>=0.5:
            color=(78,171,24)
        elif value>=0.1:
            color=(244,232,61)
        else:
            color=(227,85,14)
        white=(255,255,255)
        offsetX=4
        offsetY=4
        #draw the positive bar
        healthBarSurface.fill(color,Rect(offsetX*cellsHigh,offsetY*cellsHigh,posBarLength,6*cellsHigh))
        #draw the negative bar
        healthBarSurface.fill(white,Rect(offsetX*cellsHigh+posBarLength,offsetY*cellsHigh,negBarLength,6*cellsHigh))
        #draw the left end
        scaledBarLeft=pygame.transform.smoothscale(healthBarLeft,(pixel*cellsHigh,pixel*cellsHigh))
        healthBarSurface.blit(scaledBarLeft,(0,0))
        #draw the right end
        scaledBarRight=pygame.transform.smoothscale(healthBarRight,(pixel*cellsHigh,pixel*cellsHigh))
        healthBarSurface.blit(scaledBarRight,(pixel*(cellsLong-cellsHigh),0))
        #draw the middle
        scaledBarMiddle=pygame.transform.smoothscale(healthBarMiddle,(pixel*(cellsLong-2*cellsHigh),pixel*cellsHigh))
        healthBarSurface.blit(scaledBarMiddle,(pixel*cellsHigh,0))
        return healthBarSurface


pixel=15
pygame.init()
screenSize=(400,400)
healthBarLeft=pygame.image.load(os.path.join("sprites","barEndLeft.png"))
healthBarRight=pygame.image.load(os.path.join("sprites","barEndRight.png"))
healthBarMiddle=pygame.image.load(os.path.join("sprites","barMiddle.png"))
gameScreen=pygame.display.set_mode(screenSize,0,32)
gameScreen.fill((50,50,200))
gameScreen.blit(getHealthBar(12,1,0.0),(0,0))
gameScreen.blit(getHealthBar(12,2,0.09),(0,40))
gameScreen.blit(getHealthBar(12,2,0.4),(0,100))
gameScreen.blit(getHealthBar(12,3,0.4),(0,150))
gameScreen.blit(getHealthBar(12,4,0.8),(0,200))
gameScreen.blit(getHealthBar(12,5,1.0),(0,300))
pygame.display.flip()
