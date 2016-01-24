###Level builder feature list
#preview of current section of level
#background texture pallete
#foreground texture pallete
#save/load/new interface

#addition of item balls
#addition of npcs
#screenchangers: addition, connection, and
    #reciprocity checking (for indivdual and level)
    #is there another world at the other end
    #does it point to a screenchanger at those coordinates
    #does that screenchanger point back to correct screen
    #and to the correct coordinates.
#canvas size (for e.g. restricted vision in caves)
#padding character
#


#stuff that goes in a file:
#name, dimensions, padding character, Big Ole List

##TODO:
###save function
###Save-as
###load/save interface


import pygame
from pygame.locals import *
import os
from os import listdir
from os.path import isfile, join
worldCode=open("World.py")
exec(worldCode.read())

###Initializing stuff
pixel=15 #side length of sprite grid unit in pixels
screenWidth=29
screenHeight=21
paletteWidth=4 #number of pixels on right reserved for palette

def safeCopy(source):
    copy=[]
    for line in source:
        copy.append(list(line))
    return copy

class editorScreen:
    def __init__(self,xDim,yDim,paletteWidth):
        pygame.init()
        self.xDim=xDim #screen width in sprites, must be odd to keep player in center
        self.yDim=yDim #screen height in sprites must be odd to keep player in center
        self.paletteWidth=paletteWidth
        if xDim%2==0:
            print "xDim is even, make it odd."
        if yDim%2==0:
            print "yDim is even, make it odd."
        self.screenSize=(pixel*xDim,pixel*yDim)
        self.curWorld=False
        self.buttons=[]
        self.createButtons()
        self.editorScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(210,210,210)
        self.editorScreen.fill(self.backgroundColor)
        self.gameSlice=pygame.Surface(self.screenSize) #what was this for in the original file and are we going to use it here?
        self.terrainDebugMode=False
        self.curPaintingChar=False
        self.curGround=False #whether painting on background or foreground
        self.offset=[0,0] #how much the part of the map visible
            #is offset from having the top left corner
            #in the top left corner of the screen
        self.heldFirstCorner=False
        self.mainFont=pygame.font.SysFont("courier new",pixel)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.running=True
        self.loadWorldFile()

        #The following needs to be the last line in __init__!
        self.mainloop()


    def mainloop(self):
        while self.running:
            events=self.getInput()
            self.processInput(events)
            self.drawScreen()
            self.clock.tick(self.fps)
        pygame.display.quit()

    def createButtons(self):
        #create buttons for foreground x, T, " ", background "w", " ", "G", "-"
        #(self,screen,xPos,yPos,imageName="",char="",ground="background",name=False,height=1,width=1)

        #foregrounds start here

        FGeraser=button(self,screenWidth-paletteWidth,0,"eraser.png"," ","foreground","noFG")       
        rock=button(self,screenWidth-paletteWidth+1,0,"b.png","x","foreground","rock")
        tree=button(self,screenWidth-paletteWidth+2,0,"tree.png","T","foreground","tree")
        
        #backgrounds start here
        BGeraser=button(self,screenWidth-paletteWidth,8,"eraser.png"," ","background","noBG")
        water=button(self,screenWidth-paletteWidth+1,8,"water.png","w","background","water")
        tallGrass=button(self,screenWidth-paletteWidth+2,8,"t.png","G","background","tallgrass")
        dirt=button(self,screenWidth-paletteWidth+3,8,"p.png","-","background","dirt")

        #padding character change button
        paddingCharButton=button(self,screenWidth-paletteWidth,screenHeight-2,"bigblank.png"," ","tool","padding char",2,2)
        
            
        

    def getInput(self):
        goodKeys=[K_n,K_s,K_l,K_p,K_m,K_r,K_UP, K_DOWN, K_RIGHT, K_LEFT]
        events = pygame.event.get()
        keptEvents=[]
        for event in events:
            if event.type == QUIT:
                self.running=False
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                keptEvents.append(event)
            elif event.type == KEYDOWN and event.key in goodKeys:
                keptEvents.append(event)
        return keptEvents
        #if there are no quits or mouse clicks, the result of this function
        #will evaluate to False, because Python is nice like that.

    def processInput(self,events):
        for event in events:
            if event.type==KEYDOWN:
                if event.key==K_n:
                    self.createNewWorldFile() #write this function
                elif event.key==K_s:
                    self.saveWorldFile() #write this function
                elif event.key==K_l:
                    self.loadWorldFile()
                elif event.key==K_p:
                    self.setPaddingCharacter()  #do we still need to write this?
                elif event.key==K_r:
                    self.offset=[0,0]
                elif event.key==K_m:
                    self.terrainDebugMode=not self.terrainDebugMode
                elif (pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]):
                    #arrow key, scroll the world five squares in the specified direction
                    if event.key==K_UP:
                        self.offset[1]-=5
                    elif event.key==K_DOWN:
                        self.offset[1]+=5
                    elif event.key==K_LEFT:
                        self.offset[0]-=5
                    elif event.key==K_RIGHT:
                        self.offset[0]+=5
                else: #not holding ctrl, only scroll by one square
                    if event.key==K_UP:
                        self.offset[1]-=1
                    elif event.key==K_DOWN:
                        self.offset[1]+=1
                    elif event.key==K_LEFT:
                        self.offset[0]-=1
                    elif event.key==K_RIGHT:
                        self.offset[0]+=1
                        
            else: #mouse click
                pixelX=event.pos[0]/pixel
                pixelY=event.pos[1]/pixel
                #this auto-floors which is what we want
                #e.g. clicking on pixel 12 gets you box 0
                if pixelX>=(self.xDim-self.paletteWidth): #clicked on palette
                    for button in self.buttons:
                        if button.checkPosition([pixelX,pixelY]):
                            if button.ground=="tool":
                                button.useToolButton(button.name)
                            else:
                                self.curPaintingChar=button.char
                                self.curGround=button.ground
                else: #clicked on map
                    pixelX+=self.offset[0]
                    pixelY+=self.offset[1]
                    if 0<=pixelX<self.curWorld.dimx and 0<=pixelY<self.curWorld.dimy:
                        if (pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]):
                            if not self.heldFirstCorner:
                                self.heldFirstCorner=[pixelX,pixelY]
                            elif self.heldFirstCorner==[pixelX,pixelY]:
                                self.heldFirstCorner=False
                            else:
                                self.curWorld.setRegion(self.curGround,self.curPaintingChar,[pixelX,pixelY],self.heldFirstCorner)
                                self.heldFirstCorner=False
                        else:
                            self.curWorld.setSquare([pixelX,pixelY],self.curGround,self.curPaintingChar) #update the selection
                    else:
                        #extend the world map
                        if pixelY<0:
                            numTopPaddingRows=-1*pixelY
                            pad=[]
                            for i in range(0,numTopPaddingRows):
                                paddingRow=[]
                                for i in range(0,self.curWorld.dimx):
                                    paddingRow.append(self.curWorld.paddingChar)
                                pad.append(paddingRow)
                            self.curWorld.permSpriteMap=pad+self.curWorld.permSpriteMap
                            self.curWorld.dimy+=numTopPaddingRows
                            self.curWorld.permTerrainMap=self.curWorld.getPermTerrainMap(self.curWorld.permSpriteMap,self.curWorld.dimx,self.curWorld.dimy)
                            self.offset[1]-=pixelY
                            pixelY=0
                            
                        elif pixelY>=self.curWorld.dimy:
                            numBottomPaddingRows=pixelY-self.curWorld.dimy+1
                            pad=[]
                            for i in range(0,numBottomPaddingRows):
                                paddingRow=[]
                                for i in range(0,self.curWorld.dimx):
                                    paddingRow.append(self.curWorld.paddingChar)
                                pad.append(paddingRow)
                            self.curWorld.permSpriteMap=self.curWorld.permSpriteMap+pad
                            self.curWorld.dimy+=numBottomPaddingRows
                            self.curWorld.permTerrainMap=self.curWorld.getPermTerrainMap(self.curWorld.permSpriteMap,self.curWorld.dimx,self.curWorld.dimy)

                        if pixelX<0:
                            numLeftPaddingChars=-1*pixelX
                            pad=numLeftPaddingChars*[self.curWorld.paddingChar]
                            for i in range(0,len(self.curWorld.permSpriteMap)):
                                oldRow=self.curWorld.permSpriteMap[i]
                                self.curWorld.permSpriteMap[i]=pad+oldRow
                            self.curWorld.dimx+=numLeftPaddingChars
                            self.curWorld.permTerrainMap=self.curWorld.getPermTerrainMap(self.curWorld.permSpriteMap,self.curWorld.dimx,self.curWorld.dimy)
                            self.offset[0]-=pixelX
                            pixelX=0
                            
                        elif pixelX>=self.curWorld.dimx:
                            numRightPaddingChars=pixelX-self.curWorld.dimx+1
                            pad=numRightPaddingChars*[self.curWorld.paddingChar]
                            for i in range(0,len(self.curWorld.permSpriteMap)):
                                self.curWorld.permSpriteMap[i]+=pad
                            self.curWorld.dimx+=numRightPaddingChars
                            self.curWorld.permTerrainMap=self.curWorld.getPermTerrainMap(self.curWorld.permSpriteMap,self.curWorld.dimx,self.curWorld.dimy)
                            
                            
                #highlight selected square
                topLeft=(pixel*pixelX,pixel*pixelY)
                topRight=(pixel*(1+pixelX),pixel*pixelY)
                bottomLeft=(pixel*pixelX,pixel*(1+pixelY))
                bottomRight=(pixel*(1+pixelX),pixel*(1+pixelY))
                pygame.draw.line(self.editorScreen,(0,0,0),topLeft,topRight,3)
                pygame.draw.line(self.editorScreen,(0,0,0),topLeft,bottomLeft,3)
                pygame.draw.line(self.editorScreen,(0,0,0),topLeft,topRight,3)
                pygame.draw.line(self.editorScreen,(0,0,0),topLeft,topRight,3)
                

    def drawScreen(self):
        self.editorScreen.fill(self.backgroundColor)
        self.drawPalette()
        self.drawCurWorld()
        self.drawGrid()
        self.drawMisc() #offset and any other such small things
        pygame.display.flip()

    def drawPalette(self):
        blueRectangle=pygame.draw.rect(self.editorScreen,(0,0,255),(pixel*25,0,pixel*paletteWidth,pixel*21))

    def getWorldSlice(self,whichMap="draw"):#pads and crops the world map.
        #[This world map has been modified from its original version. It has been formatted to fit your screen.]
        #self.curWorld,self.xDim,self.yDim,self.playerPos
        xDim=self.xDim-paletteWidth #leave room for s/Jesus/the palette
        yDim=self.yDim
        paddingChar=self.curWorld.paddingChar
        if whichMap=="draw":
            startDrawMap=safeCopy(self.curWorld.permDrawMap)
        elif whichMap=="sprite":
            startDrawMap=safeCopy(self.curWorld.permSpriteMap)
        topRow=self.offset[1]
        
        paddingRow=[paddingChar]*len(startDrawMap[0])
        #pad the top
        startDrawMap=-topRow*[paddingRow]+startDrawMap
        #if we padded the top, adjust the topRow; otherwise leave it
        if topRow<0:
            topRow=0
        bottomRow=topRow+yDim #NO -1 HERE
        bottomPad=bottomRow-len(startDrawMap)
        #pad the bottom
        startDrawMap+=bottomPad*[paddingRow]

        leftCol=self.offset[0]
        for i in range(0,len(startDrawMap)):
            startDrawMap[i]=-leftCol*[paddingChar]+startDrawMap[i]
        #if we padded the left, adjust the leftCol; otherwise leave it
        if leftCol<0:
            leftCol=0
        rightCol=xDim+leftCol
        rightPad=rightCol-len(startDrawMap[0])
        for i in range(0,len(startDrawMap)):
            startDrawMap[i]+=rightPad*[paddingChar]
        choppedMap=[]
        for line in startDrawMap[topRow:bottomRow]:
            choppedMap.append(line[leftCol:rightCol])
        centerX=(xDim-1)/2
        centerY=(yDim-1)/2
        return choppedMap

    def drawCurWorld(self,surface=False):
        if not surface:
            surface=self.editorScreen
        surface.fill(self.backgroundColor)
        drawPos=[0,0]
        drawArray=self.getWorldSlice("sprite")
        secondList=[]
        for row in drawArray:
            drawPos[0]=0
            for cell in row:
                if isinstance(cell,tuple):
                    secondList.append(tuple(drawPos)) #handle its sprite later, but do blit the background
                    surface.blit(worldBGSpriteDict[cell[1]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                elif not self.terrainDebugMode:
                    surface.blit(worldBGSpriteDict[cell[1]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                    surface.blit(worldFGSpriteDict[cell[0]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                else:
                    surface.blit(self.getTerrainTile(self.curWorld.getTerrain(cell)),dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                drawPos[0]+=1
            drawPos[1]+=1
        for item in secondList:
            sprite = self.spriteSlice[item[1]][item[0]][0]
            drawPos=[item[0]*pixel, item[1]*pixel]
            if isinstance(sprite,(building,screenChanger,actionable)):
                sprite.addToSurface(surface,drawPos)
            else:
                print "not adding", sprite
        if surface==self.editorScreen:
            pass
            #pygame.display.flip() #otherwise we're drawing to a stored image
        else:
            return surface

    def getTerrainTile(self,terrNum):
        canvas=pygame.Surface((pixel,pixel),0,32)
        colorDict={0:(200,200,200),1:(0,0,0),2:(255,0,0),3:(0,255,0),4:(0,0,255)}
        canvas.fill(colorDict[terrNum])
        return canvas

    def drawGrid(self):
        for i in range(1,screenWidth):
            pygame.draw.line(self.editorScreen,(0,0,0),(pixel*i,0),(pixel*i,pixel*screenHeight))
        for i in range(1,screenHeight):
            pygame.draw.line(self.editorScreen,(0,0,0),(0,pixel*i),(pixel*screenWidth,pixel*i))

    def drawMisc(self):
        #offset and similar minor screen things
        offsetImg=self.mainFont.render("Offset: ("+str(self.offset[0])+","+str(self.offset[1])+")",True,(255,255,255),(0,0,0))
        self.editorScreen.blit(offsetImg,[0,pixel*(self.yDim-1)])
        for button in self.buttons:
            button.blitMe()

        #padding character indicator
        paddingCharImg=pygame.Surface((pixel,pixel),0,32)
        paddingCharImg.blit(worldBGSpriteDict[self.curWorld.paddingChar[1]],[0,0]) 
        paddingCharImg.blit(worldFGSpriteDict[self.curWorld.paddingChar[0]],[0,0])
        paddingCharImg=pygame.transform.scale2x(paddingCharImg)
        self.editorScreen.blit(paddingCharImg,[pixel*(self.xDim-self.paletteWidth),pixel*(self.yDim-2)])

        #painting character indicator
        if self.curPaintingChar:
            paintingCharImg=pygame.Surface((pixel,pixel),0,32)
            paintingCharImg.fill(pygame.Color(200,200,200))
            if self.curGround=="background":
                paintingCharImg.blit(worldBGSpriteDict[self.curPaintingChar],[0,0])
            elif self.curGround=="foreground":
                paintingCharImg.blit(worldFGSpriteDict[self.curPaintingChar],[0,0])
            else:
                print "ERROR: unknown third alternative to foreground/background",self.curGround
            paintingCharImg=pygame.transform.scale2x(paintingCharImg)
            self.editorScreen.blit(paintingCharImg,[pixel*(self.xDim-2),pixel*(self.yDim-2)])
        #outline of active world
        pygame.draw.rect(self.editorScreen,(255,0,0),(-1*pixel*self.offset[0],-1*pixel*self.offset[1],pixel*self.curWorld.dimx,pixel*self.curWorld.dimy),3)
        #outline of held first corner
        if self.heldFirstCorner:
            borderPosition=(pixel*(self.heldFirstCorner[0]-self.offset[0]),pixel*(self.heldFirstCorner[1]-self.offset[1]),pixel,pixel)
            pygame.draw.rect(self.editorScreen,(255,255,0),borderPosition,3)
        
                        
    def createNewWorldFile(self):
        pass
        

    def loadWorldFile(self):
        worldFiles=[]
        for f in listdir("World files"):
            if isfile(join("World files",f)):
                worldFiles.append(f)
        print worldFiles
        selectedFile=raw_input("Enter the name of the file you wish to open:")
        if selectedFile[-3:]!=".py":
            selectedFile+=".py"
        self.curWorldFileName=os.path.join("World files",selectedFile)
        self.curWorldFile=open(self.curWorldFileName,"r+")
        self.curWorldVersion=eval(self.curWorldFile.readline())
        if self.curWorldVersion==1:
            self.readWorldFile1()
        else:
            print "ERROR: Invalid version number"
        self.curWorldFile.close()

    def readWorldFile1(self):
        worldDims=eval(self.curWorldFile.readline())
        landMonSeed=eval(self.curWorldFile.readline())
        waterMonSeed=eval(self.curWorldFile.readline())
        paddingChar=eval(self.curWorldFile.readline())
        curWorldArray=[]
        for line in range(0,worldDims[1]):
            curWorldArray.append(eval(self.curWorldFile.readline()))
        self.curWorld=world(self,curWorldArray,worldDims[0],worldDims[1],landMonSeed,waterMonSeed,paddingChar)

    def saveWorldFile(self):
        self.curWorldFile=open(self.curWorldFileName[:-3]+"27.py","w")
        self.curWorldFile.write(str(self.curWorldVersion)+"\n")
        self.curWorldFile.write("["+str(self.curWorld.dimx)+","+str(self.curWorld.dimy)+"]\n")
        if self.curWorld.landMonSeed:
            line="monSeed("+str(self.curWorld.landMonSeed.ticketDict)+str(self.curWorld.landMonSeed.encounterRate)+")"
            self.curWorldFile.write(line+"\n")
        else:
            self.curWorldFile.write("False\n")
        if self.curWorld.waterMonSeed:
            line="monSeed("+str(self.curWorld.waterMonSeed.ticketDict)+str(self.curWorld.waterMonSeed.encounterRate)+")"
            self.curWorldFile.write(line+"\n")
        else:
            self.curWorldFile.write("False\n")
        self.curWorldFile.write('"'+self.curWorld.paddingChar+'"'+"\n")
        for line in self.curWorld.permSpriteMap:
            self.curWorldFile.write(str(line)+"\n")
        self.curWorldFile.close()
        
        
class button:
    def __init__(self,screen,xPos,yPos,imageName="",char="",ground="background",name=False,height=1,width=1):
        self.screen=screen
        self.xPos=xPos
        self.yPos=yPos
        self.name=name
        self.height=height
        self.width=width
        self.char=char
        self.ground=ground
        self.imageName=imageName
        self.image=pygame.image.load(os.path.join("sprites",imageName))
        self.screen.buttons.append(self)

    def checkPosition(self,pos): #returns True iff the position in (large) pixels is in the button
        inX,inY=pos
        if inX>=self.xPos and inX<=(self.xPos+self.width):
            if inY>=self.yPos and inY<=(self.yPos+self.height):
                return True
        return False
        #return (self.xPos<=pos[0]<(self.xPos+self.width) and self.yPos<=pos[1]<(self.yPos+self.height))

    def blitMe(self,surface="screen"):
        if surface=="screen":
            surface=self.screen
        surface.editorScreen.blit(self.image,[self.xPos*pixel,self.yPos*pixel])

    def useToolButton(self,name):
        if name=="padding char":
            if self.screen.curGround=="foreground":
                self.screen.curWorld.paddingChar=self.screen.curPaintingChar+self.screen.curWorld.paddingChar[1]
            elif self.screen.curGround=="background":
                self.screen.curWorld.paddingChar=self.screen.curWorld.paddingChar[0]+self.screen.curPaintingChar
            else:
                print "ERROR: invalid foreground/background option"
        else:
            print "ERROR: invalid tool button name"





editor=editorScreen(screenWidth,screenHeight,paletteWidth)
