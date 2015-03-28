#################################PUNKEMON YO!!!!!###############################

import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *
import os
import string

fontLoaderCode=open("menu sprite code.py")
exec(fontLoaderCode.read())

################### Menu stuff ############################

#####startDict: for menus originating with the start menu
#startDict={"Start": start, "Wikidex": wikidex, "Team": team, "World": world,
#"Tokens": tokens, "Stats": stats, "Stuff": stuff, "Save": save,
#"Options": options}

#####fightDict: for menus originating with the battle menu
#fightDict={"Battle": battle, "Attack": attack, "Item": item, "Switch": switch, "Leg it": legIt}

class menu:
    def __init__(self,oplist,nextMenuMeta="previous",nextMenu=False,rollable=False):
        #rollable means being on the bottom option and hitting "down" gets you the top option
        self.oplist=oplist
        self.curPos=1 #current position of cursor, ONE-indexed
        self.rollable=rollable
        self.nextMenuMeta=nextMenuMeta
        #default of previous menu, can be set to "menu" for a specific nonprevious menu or False if it always goes back to world
        self.nextMenu=nextMenu
        
    def setNext(self,target): #sets menu to return to upon pressing B
        self.nextMenu=target

    def getNext(self): #returns nextMenu
        return self.nextMenu
    
    def getArray(self): #generates array with set of menu options for sprite generations
        #find length of longest menu item
        maxLength=2
        for op in self.oplist: #op needs to be a string
            if len(op)>maxLength:
                maxLength=len(op)
        #top border line
        opAr=[["*"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("=")
        opAr[0].append("*")
        #assemble menu line for a given entry
        for op in self.oplist: 
            tmp=["|"," "] #open line with pipe and space for cursor
            tmpStr=op.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("|")#close line with pipe
            opAr.append(tmp)
        opAr.append(opAr[0]) #bottom border is same as top
        #draw cursor
        opAr[self.curPos][1]=">"
        return(opAr)

    def setOptions(self,newList):
        self.oplist=newList
        
    def moveCursor(self,direction):
        if direction=="up":
            if self.curPos>1: #curPos=1 means cursor on top option
                self.curPos-=1
            elif self.rollable:
                self.curPos=len(self.oplist)
        elif direction=="down":
            if self.curPos<len(self.oplist):
                self.curPos+=1
            elif self.rollable:
                self.curPos=1
                
    def processInput(self, event, screen):
        if event.type==KEYDOWN:
            #print "----------------------"
            if event.key==K_UP:
                self.moveCursor("up")
            elif event.key==K_DOWN:
                self.moveCursor("down")
            elif event.key==K_a:
                oldMenu=self
                newMenu=menuDict[self.oplist[self.curPos-1]]
                screen.curMenu=newMenu
                if newMenu.nextMenuMeta=="previous":
                    newMenu.setnextMenu(oldMenu)
            elif event.key==K_s:
                screen.curMenu=self.getNext()
        #for i in screen.curMenu.getArray():
            #print i
    


class dialogMenu:
    def __init__(self,dialog,nextMenuMeta="menu",nextMenu=False,curSlide=1): #nextMenu can be world or menu, dialog is a list of strings
        self.dialog=dialog
        self.nextMenuMeta=nextMenuMeta
        #default of specific menu, can be set to "previous" for the previous menu (overwrites any initial set value) or False if it always goes back to world
        self.nextMenu=nextMenu
        self.curSlide=curSlide
        self.maxChars=20
        self.maxLines=3
        self.maxSlides=5
        #if len(dialog)>self.maxSlides:
            #print "STFU already! This is too many slides!"

    def setNext(self,target): #sets menu to which to return upon pressing B
        self.nextMenu=target

    def getNext(self): #returns nextMenu
        return self.nextMenu

    def processInput(self, event, screen):
        if event.type==KEYDOWN:
            #print "----------------------"
            if self.curSlide<len(self.dialog):
                self.curSlide+=1
            else:
                oldMenu=self
                newMenu=oldMenu.getNext()
                screen.curMenu=newMenu
                if newMenu.nextMenuMeta=="previous":
                    newMenu.setNext(oldMenu)
                self.curSlide=1
        #for i in screen.curMenu.getArray():
            #print i


    def getArray(self): #generates array with dialog characters in a box
        #get raw string of dialog and break it up into lines
        diastring=self.dialog[self.curSlide-1] #-1 bc curSlide is 1-indexed
        sentences=diastring.split("\n")
        finalLines=[] #will contain the final dialog, with each item being a line
        for sentence in sentences:
            if len(sentence)<=self.maxChars:
                finalLines.append(sentence)
            else:
                words=sentence.split()
                newLine=""
                for word in words:
                    #if you can fit one more word on the line,
                    if len(newLine)+len(word)<self.maxChars: 
                        newLine=newLine+word+" "
                    #if you can't, finalize the line and start a new one
                    else:
                        finalLines.append(newLine[0:-1])
                        newLine=word+" "
                finalLines.append(newLine[0:-1])
        #if len(finalLines)>self.maxLines:
            #print "Take a breath already! This is too many lines on one slide!"
        for i in range(0,len(finalLines)):
            #if len(finalLines[i])>self.maxChars:
                #print "You fucked up big time."
            finalLines[i]=finalLines[i].ljust(self.maxChars)
            
        ##Now to characterize and print the array
                
        #top border line
        diAr=[["*"]]
        #make the menu box the same size (just big enough to accomodate the longest allowable line) every time
        for i in range(0,self.maxChars):
            diAr[0].append("=")
        diAr[0].append("*")
        #assemble menu line for a given entry
        for line in finalLines:
            tmp=["|"]
            for char in line: #break line into individual characters
                tmp.append(char)
            tmp.append("|")
            diAr.append(tmp)        
        diAr.append(diAr[0]) #bottom border is same as top
        return(diAr)


class forcedChoiceMenu:
    def __init__(self,oplist,nextMenuMeta="previous",nextMenu=False,rollable=False):
        #rollable means being on the bottom option and hitting "down" gets you the top option
        self.oplist=oplist
        self.curPos=1 #current position of cursor, ONE-indexed
        self.rollable=rollable
        self.nextMenuMeta=nextMenuMeta
        #default of previous menu, can be set to "menu" for a specific nonprevious menu or False if it always goes back to world
        self.nextMenu=nextMenu
        
    def setNext(self,target): #sets menu to return to upon pressing B
        self.nextMenu=target

    def getNext(self): #returns nextMenu
        return self.nextMenu
    
    def getArray(self): #generates array with set of menu options for sprite generations
        #find length of longest menu item
        maxLength=2
        for op in self.oplist: #op needs to be a string
            if len(op)>maxLength:
                maxLength=len(op)
        #top border line
        opAr=[["*"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("=")
        opAr[0].append("*")
        #assemble menu line for a given entry
        for op in self.oplist: 
            tmp=["|"," "] #open line with pipe and space for cursor
            tmpStr=op.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("|")#close line with pipe
            opAr.append(tmp)
        opAr.append(opAr[0]) #bottom border is same as top
        #draw cursor
        opAr[self.curPos][1]=">"
        return(opAr)

    def setOptions(self,newList):
        self.oplist=newList
        
    def moveCursor(self,direction):
        if direction=="up":
            if self.curPos>1: #curPos=1 means cursor on top option
                self.curPos-=1
            elif self.rollable:
                self.curPos=len(self.oplist)
        elif direction=="down":
            if self.curPos<len(self.oplist):
                self.curPos+=1
            elif self.rollable:
                self.curPos=1
                
    def processInput(self, event, screen):
        if event.type==KEYDOWN:
            #print "----------------------"
            if event.key==K_UP:
                self.moveCursor("up")
            elif event.key==K_DOWN:
                self.moveCursor("down")
            elif event.key==K_a:
                oldMenu=self
                newMenu=menuDict[self.oplist[self.curPos-1]]
                screen.curMenu=newMenu
                if newMenu.nextMenuMeta=="previous":
                    newMenu.setnextMenu(oldMenu)
        #for i in screen.curMenu.getArray():
            #print i

        
########### Punkemon, because there need to be some mons in this mon-battling game ############

class punkemon:
    def __init__(self,species,nation,specNum,level,learnSpeed,baseStats,baseXPworth,allMoves=[]): #statVariables should be a list with base stats for the species plus anything else necessary to calculate attk, def, etc.
        self.species=species
        self.specNum=specNum
        self.nation=nation
        global IDnum
        self.ID=IDnum
        IDnum+=1
        self.level=level
        self.learnSpeed=learnSpeed #rate of leveling with respect to XP
        self.XP=self.getXP()
        self.baseStats=baseStats
        self.IVs=self.getIVs()
        self.EVs=[0,0,0,0,0] #accumulates with battles
        self.permStats=self.getPermStats()#stats right after healing
        self.tempStats=self.permStats#stats after effects of damage and stat-altering moves
        self.accuracy=100
        self.evasion=100
        self.status=False #poison/burn/freeze/sleep/paralysis/flinch/confused
        self.canMove=True
        self.allMoves=allMoves #learnable moves
        self.curMoves=self.getMoves(level)
        self.curPP=self.getPP()

    def getIVs(self):#generates stats for 0-15 biased towards mean)
        IVs=[];
        for i in range(0,5):
            IVs.append(randint(0,7)+randint(0,8))
            #d8 plus d9, zero-index
        return IVs

        
    #method for calculating attack, defense, etc.
    def getPermStats(self): #returns [Attack, Defense, HP, Speed, Special]
        #WARNING: never divide ints, it auto-floors! Always float() at least one argument
        Attack=floor(((self.IVs[0]+self.baseStats[0]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        Defense=floor(((self.IVs[1]+self.baseStats[1]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        HP=floor(((self.IVs[2]+self.baseStats[2]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+10)
        Speed=floor(((self.IVs[3]+self.baseStats[3]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        Special=floor(((self.IVs[4]+self.baseStats[4]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        return [Attack,Defense,HP,Speed,Special]

    def getXP(self):
        if self.learnSpeed=="slow":
            return 5*self.level**3/4
        elif self.learnSpeed=="medium":
            return self.level**3
        elif self.learnSpeed=="fast":
            return 4*self.level**3/5

    def getPP(self):
        curPP=[]
        for m in self.curMoves:
            curPP.append(m.maxPP)
        return curPP

    def getMoves(self,level):
        return self.allMoves[-4:]

    def setCanMove():
        pass
    ################WRITE THIS##############

    def levelUp(self,number=1):
        self.level+=number
        self.stats=self.getStats()


#################### Puttin' on the MOVES ###################

class move:
    def __init__(self,name,basePwr, baseAcc, maxPP, nation, sideEffect, fastMove=False):#sideEffect can be string or False
            self.name=name
            self.basePwr=basePwr
            self.baseAcc=baseAcc
            self.maxPP=maxPP
            self.nation=nation
            self.sideEffect=sideEffect
            self.fastMove=fastMove #pre-empts Speed duel (quick attack, swift)

    def getCurPP(self,attacker):
        for i in range(0,numMoves):
            if self.name==attacker.curMoves[i].name:
                return attacker.curPP[i]

    def getHit(self,attacker,defender):
        hitChance=float(self.baseAcc)*attacker.accuracy/defender.evasion
        if randint(0,99)<hitChance:
            return True
        return False
    
    def getDamage(self,attacker,defender):
        pass

    def getEffect(self,attacker,defender):
        if self.sideEffect:
            effectWords=self.sideEffect.split()
            #if effect is a stat move
            if effectWords[0]=="self":
                attacker.tempStats[statOrder[effectWords[1]]]+=int(effectWords[2])
            elif effectWords[0]=="enemy":
                defender.tempStats[statOrder[effectWords[1]]]+=int(effectWords[2])
            else:
                if randint(0,99)<int(effectWords[0]):
                    defender.status=effectWords[1]




############Screen and high-level "running the game" stuff##############
    
class screen:
    #runs at start of screen, conducts background setup before first loop
    def __init__(self):
        pygame.init()
        self.background=pygame.image.load("jedipunzel.jpg")
        self.screenSize=self.background.get_size()
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(255,255,255)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.processInput=self.menuInput
        self.drawScreen=self.drawMenu
        self.curMenu=Intro
        self.mainloop()
        self.mode="menu"

    

    def mainloop(self):
        if self.mode=="menu":
            while True:
                #find out what the user has done
                event=self.getInput()
                #deal with it, updating gamestate accordingly
                self.processInput(event)#this will be a different function depending on what's going on
                #update broader game state
                self.update() 
                #draw
                self.drawScreen()#this will be a different function depending on what's going on
                self.clock.tick(self.fps)
        if self.mode=="battle":
            firstMon=ownMon;secondMon=enemyMon
            firstMove=ownMove;secondMove=enemyMove#only change this if enemy goes first
            #if both or neither using fast moves
            if ownMon.fastMove==enemyMon.fastMove:
                #Speed duel
                if ownMon.Speed<enemyMon.Speed:
                    firstMon=enemyMon;secondMon=ownMon
                    firstMove=ownMove;secondMove=enemyMove
                    ##Note: as currently implemented, player wins ties.
            else: #if one fast move in play
                #if your fast move, run your move first
                if enemyMove.fastMove:
                    firstMon=enemyMon;secondMon=ownMon
                    firstMove=ownMove;secondMove=enemyMove
            if firstMon.canMove() and firstMon.getHit():
                firstMove.getDamage()
            if secondMon.canMove() and secondMon.getHit():
                secondMove.getDamage()
                    

    #find the first valid input and pass to input processor
    #if no valid input, pass Null
    def getInput(self):
        goodKeys=[K_a, K_s, K_SPACE, K_UP, K_DOWN, K_RIGHT, K_LEFT]
        #add > and < later for time warp and p for pause
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.display.quit()
                break
            elif event.type==KEYDOWN:
                if event.key in goodKeys:
                    return event
        return False           

    #process the input
    def menuInput(self,event):
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        else:
            self.curMenu.processInput(event, self)

    def update(self):
        pass

    def drawASCII(self):
        pass
        #print "----------------------"
        #print self.curMenu.getArray()
    def drawMenu(self):
        self.gameScreen.fill(self.backgroundColor)
        drawPos=[0,0]
        pixel=15 #side length of sprite grid unit in pixels
        drawArray=self.curMenu.getArray()
        for row in drawArray:
            drawPos[0]=0
            for cell in row:
                self.gameScreen.blit(menuSpriteDict[cell],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                drawPos[0]+=1
            drawPos[1]+=1
        pygame.display.flip()
            


#################Generating individual things
###### Global variables (semi-permanent)
IDnum=0 #increment this when a new punkemon is generated
numMoves=4
statOrder={"attack":0,"defense":1,"HP":2,"Speed":3,"special":4}
#your handy guide to the stats list: stat name-->index in stats list
  

###### Menu instances        
top=menu(["left","right"],True)
left=menu(["What's new?","botom","botom"],True)
left.setNext(top)
right=menu(["botom","botom"])
right.setNext(top)
botom=dialogMenu(["This is a test. \n This is a test with a very long line that needs to be broken up.","And it just keeps going! When will it end?!"])
falseChoice=forcedChoiceMenu(["Boy","Girl"])
nickChoice=forcedChoiceMenu(["ASSHAT","ASSFACE","BUTTHAT","BUTTFACE","FACEHAT","ASSBUTT",'"GARY"'])
noDice=dialogMenu(["Since it seems I can't talk either of you two out of it~","Your adventure in the world of PUNKEMON fighting starts NOW. Grab a mon and get going!"],"menu",top)
doItAnyway=forcedChoiceMenu(["You can't scare me.","I'm gonna be the best!"],"menu",noDice)
talkOut=dialogMenu(["I'll tell you what I told him:\nThe fighting circuit ain't no nursery school.","You've got a better chance of ending up in jail or a body bag than as a PUNKEMON CHAMPION."],"menu",doItAnyway)
Intro=dialogMenu(["Yo Brainbin!\nWelcome to the world of Punkemon~","My name is TYPHA.\nPeople in this hood, they call me the PUNKEMON PROFESSA.",
                  "There are creatures called PUNKEMON all up in dis world.","Some people think PUNKEMON are monsters.\nAin't totally wrong~","Some people keep 'em as pets.\nOthers use them in fights.",
                  "Me, I used to do that.\nNow I'm goin' straight.","I'm gonna study PUNKEMON as a profession.\nLab coat and everything.","When you're hiding behind that picture of Archie and Edith Bunker, it's hard to tell who you are.",
                  "Are you a boy, or a girl?"],"menu",falseChoice)
boy=dialogMenu(["You remember my little bro.\nYou've been at each other's throats ever since you were kids.","What was your charming nickname for him again?"],"menu",nickChoice)
asshat=dialogMenu(['Oh, yeah. "Asshat." Ha! You have such a way with words~'],"menu",talkOut)
assface=dialogMenu(['Oh, yeah. "Assface."Ha!  You have such a way with words~'],"menu",talkOut)
butthat=dialogMenu(['Oh, yeah. "Butthat." Ha! You have such a way with words~'],"menu",talkOut)
buttface=dialogMenu(['Oh, yeah. "Buttface." Ha! You have such a way with words~'],"menu",talkOut)
facehat=dialogMenu(['Oh, yeah. "Facehat." Ha! You have such a way with words~'],"menu",talkOut)
assbutt=dialogMenu(['Oh, yeah. "Assbutt." Ha! You have such a way with words~'],"menu",talkOut)
Gary=dialogMenu(['Oh, yeah. "Gary". Ha! You have such a way with words~'],"menu",talkOut)
menuDict={"top":top,"left":left,"right":right,"botom":botom, "Boy": boy,"FalseChoice":falseChoice,
          "nickChoice":nickChoice,"ASSHAT":asshat,"ASSFACE":assface,"BUTTHAT":butthat,"BUTTFACE":buttface,"FACEHAT":facehat,"ASSBUTT":assbutt,'"GARY"':Gary,
          "talkOut":talkOut,"doItAnyway":doItAnyway,"noDice":noDice, "You can't scare me.":noDice,"I'm gonna be the best!":noDice}

######Move instances
##Initialize moves with: name,basePwr, baseAcc, maxPP, nation, sideEffect, fastMove=False
tackle=move("Tackle",100,90,20,"normal",False)
thundershock=move("Thundershock",100,90,15,"electric","30 paralysis")
sandAttack=move("Sand Attack",100,90,20,"normal","enemy accuracy -5")##IMPLEMENT ACCURACY then pick a better number
splash=move("Splash",0,100,20,"water",False)

###Mon species creation
##Initialize all species with:
##species,nation,specNum,level,learnSpeed,baseStats,baseXPworth,allMoves=[]
    
class bulbasaur(punkemon):
    def __init__(self,name,level):
        punkemon.__init__(self,"Bulbasaur","grass",1,level,"medium",[49,49,45,45,65],64,[tackle])
        self.name=name
        
class charmander(punkemon):
    def __init__(self,name,level):
        punkemon.__init__(self,"Charmander","fire",4,level,"medium",[52,43,39,65,50],62,[tackle])
        self.name=name
        
class squirtle(punkemon):
    def __init__(self,name,level):
        punkemon.__init__(self,"Squirtle","water",7,level,"medium",[48,65,44,43,50],63,[tackle])
        self.name=name
     
class derp(punkemon):
    def __init__(self,name,level):
        punkemon.__init__(self,"Derp","fail",1,level,"slow",[0,0,0,0,0],64,[splash])
        self.name=name

 
######Pokemon instance creation
##Initialize all pokemon with: species, level
starterBulbasaur=bulbasaur("bulbasaur",5)
starterCharmander=charmander("charmander",5)
starterSquirtle=squirtle("squirtle",5)
derpy=derp("derpy",30)

######Hard sets of things that should be dynamically generated (Yeah testing!)
ownMon=starterBulbasaur
enemyMon=starterCharmander
ownMove=tackle
enemyMon=thundershock

         
