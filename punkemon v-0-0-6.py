################################# PUNKEMON YO!!!!! ###############################
########## Imports from elsewhere
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
battlesCode=open("Battles.py")
exec(battlesCode)
monCode=open("Mons.py")
exec(monCode.read())
worldCode=open("World.py")
exec(worldCode.read())

######### this thing
fakeAPress=pygame.event.Event(KEYDOWN,{"key":K_a})
fakeBPress=pygame.event.Event(KEYDOWN,{"key":K_s})
fakeUpPress=pygame.event.Event(KEYDOWN,{"key":K_UP})
fakeDownPress=pygame.event.Event(KEYDOWN,{"key":K_DOWN})
fakeLeftPress=pygame.event.Event(KEYDOWN,{"key":K_LEFT})
fakeRightPress=pygame.event.Event(KEYDOWN,{"key":K_RIGHT})

###################### Action Items for future work sessions #############
###bugfixes
    #stop duplicate revive effect messages.
    #add null messages so you can take out HP notifications without a no-messages error
###feature expansions
    #numerical HP display
    #XP to next level display
    #menus in different places on the screen?
    #write the catch formula
    #expand on start menu, detail team screen and wikidex
        #make the team overview a special menu subclass
    #choice menu widths (what is this? I was too vague)
    #holding down buttons
###Ambitious stuff!
    #background music (less ambitious than frivolous but still)
    #make a level generator!
    #do the sprite work for battles (requires an Artist)
    #saving and loading games



############Story notes muthafuckas!
###The first pokemon pusher (local equivalent of pokemart) is named Marty. The others are named increasingly weird spellings of Marty.
###The Martys get their shit from 3d printers
###
###Pokedex and PC system belong to Typha's university; she sneaks you access and
###charges you to store mons above the party five.
###Dex is Typha's thesis project; you and rival are collecting data for her.
###Rival's and your seen-punkemon/caught-punkemon appear in the same dex with a mark for who caught them;
###contest between you and Rival to get the most--for <s>SCIENCE</s> bragging rights!
###"Oak: "Now's not the time for that!""-->"Typha: "What are you smoking? You can't use that now!""
###
###Gym type-->city name:normal=granite, fire=citrine, water=sapphire, grass=peridot, poison=amethyst,
###electric=topaz, psychic=alexandrite, dragon=opal, ice=diamond, flying=lapis,
###ground=axinite, rock=geode, bug=emerald, fighting=stibnite, ghost=obsidian
###some random other town: malachite
###town you start out in: pearl
###4 are mandatory and then pick 4 of the other 11
###
###one of the gyms is in the middle of nowhere by the side of the route,
###in a place too small to show up on your town map. The gym leader is a hermit.
###Maybe this is the ground gym or the fighting gym or something.
###
###Electric gym is locked with a sign saying "gone to grocery store, back in 15 minutes" (and pointer npc near gym)
###back of note has grocery list, which you automatically take on second reading
###go to grocery store, gym leader is trying to remember what he wanted
###give him list, he runs off and reappears at gym
###if you only read it once, or never read it, he comes back 20 minutes after you enter town
###if you helped him find his list, "thanks for helping me! I got the stuff to make my awesome barbeque!"
###if he came back on timer, "Aw man! I forgot the stuff I needed to make my awesome barbeque!"
###either way: but that won't stop me from FRYING YOU ALIVE!" -->Fight
###dex puzzle inside electric gym: visible live wires you have to navigate around in a maze,
###accidentally walk into one and you get knocked out and wake up at maze start
###
###Fire gym leader is Azula, Water gym leader is Akula, they have the same sprite
###
###Cities are named after birthstones, one of them is Alexandrite and it has a big library
###Typha is in the library at a conference and sends you to go get a book
###And then maybe she gives you the Master Ball her advisor's been developing
###
###The optional hometown (late-unlock) gym leader is your mom (credit to imzoruaok from tumblr)
###If your reputation stat is too low, you auto-lose and are Grounded Forever and have to reload your last save.
###five or six trainers along the way make "Your mom" jokes and one or two of them are shit like "you fight like your mom" that turn out to be true

################### Global functions
def safeCopy(source):
    copy=[]
    for line in source:
        copy.append(list(line))
    return copy

################### Menu stuff ############################
allMenus=[]
class menu:
    def __init__(self,oplist,mode,execOnA,execOnS,rollable=False,oplistConstructor=False,screen=False):
        #rollable means being on the bottom option and hitting "down" gets you the top option
        self.oplist=oplist
        self.mode=mode #"choice", "titledChoice", or "dialog", controls whether there's a moving cursor and if the first thing is a title or an option
        self.curPos=1 #current position of cursor, ONE-indexed
        if self.mode=="titledChoice":
            self.curPos=2
        self.rollable=rollable
        self.execOnA=execOnA
        self.execOnS=execOnS
        self.oplistConstructor=oplistConstructor
        if self.oplistConstructor:
            self.tempOplist=eval(self.oplistConstructor)
        else:
            self.tempOplist=self.oplist
        self.curSlide=1
        self.maxChars=screenWidth-2
        self.maxLines=4
        self.maxSlides=5
        self.screen=screen
        self.frame=self.getFrame()
        #Frame should be in terms of option numbers, NOT list index
        allMenus.append(self)

    def getFrame(self): #only call this in init or when curPos is set to 1
        if self.mode=="choice":
            return[1,screenHeight-2]
        elif self.mode=="titledChoice":
            return [1,screenHeight-2]
        elif self.mode=="dialog":
            return False

    def getArray(self,top):
        if self.mode=="choice":
            array=self.getArrayChoice(top)
        elif self.mode=="titledChoice":
            array=self.getArrayTitledChoice(top)
        elif self.mode=="dialog":
            array=self.getArrayDialog()
        else:
            print self.curMode+"? That's not even a menu type."
        return array
    
    def getArrayChoice(self,top): #generates array with set of menu options for sprite generations
        #find length of longest menu item
        maxLength=2
        for op in self.tempOplist: #op needs to be a string
            if len(op)>maxLength:
                maxLength=len(op)
        maxLength+=1 #allows space on the right for the scroll cues
        #find section of menu that can currently fit on the screen
        oplistInFrame=self.tempOplist[self.frame[0]-1:self.frame[1]]
        #top border line
        opAr=[["*TL"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("T=")
        opAr[0].append("*TR")
        #assemble menu line for a given entry
        for op in oplistInFrame: 
            tmp=["L|"," "] #open line with pipe and space for cursor
            tmpStr=op.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("R|")#close line with pipe
            opAr.append(tmp)
        lastLine=["*BL"]
        for i in range(0,maxLength+1): #+1 for cursor
            lastLine.append("B=")
        lastLine.append("*BR")
        opAr.append(lastLine)
        #draw cursor
        cursorIndex=self.curPos-self.frame[0]+1
        if top:
            opAr[cursorIndex][1]=">"
        else:
            opAr[cursorIndex][1]="cOp"
        #draw scroll-arrow if necessary
        if self.frame[0]!=1: #can scroll up
            opAr[1][-2]="cUp"
        if len(self.tempOplist)>screenHeight-2 and self.frame[1]!=len(self.tempOplist): #can scroll down
            opAr[-2][-2]="cDn"
        return(opAr)

    def getArrayTitledChoice(self,top): #generates array with set of menu options for sprite generations
        #find length of longest menu item
        maxLength=2
        for op in self.tempOplist: #op needs to be a string
            if len(op)>maxLength:
                maxLength=len(op)
        maxLength+=1
        #find section of menu that can currently fit on the screen
        oplistInFrame=self.tempOplist[1:][self.frame[0]-1:self.frame[1]-1]#heaven forgive me
        #top border line
        opAr=[["*TL"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("T=")
        opAr[0].append("*TR")
        #assemble first line (title)
        firstLine=["L|"]
        paddedTitle=self.tempOplist[0].ljust(maxLength+1)
        for char in paddedTitle:
            firstLine.append(char)
        firstLine.append("R|")
        opAr.append(firstLine)
        for op in oplistInFrame: 
            tmp=["L|"," "] #open line with pipe and space for cursor
            tmpStr=op.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("R|")#close line with pipe
            opAr.append(tmp)
        lastLine=["*BL"]
        for i in range(0,maxLength+1): #+1 for cursor
            lastLine.append("B=")
        lastLine.append("*BR")
        opAr.append(lastLine)
        #draw cursor
        cursorIndex=self.curPos-self.frame[0]+1
        if top:
            opAr[cursorIndex][1]=">"
        else:
            opAr[cursorIndex][1]="cOp"
        #draw scroll-arrow if necessary
        if self.frame[0]!=1: #can scroll up
            opAr[1][-2]="cUp"
        if len(self.tempOplist)>screenHeight-2 and self.frame[1]!=len(self.tempOplist): #can scroll down
            opAr[-2][-2]="cDn"
        return(opAr)

    def getArrayDialog(self): #generates array with dialog characters in a box
        #get raw string of dialog and break it up into lines
        diastring=self.tempOplist[self.curSlide-1] #-1 bc curSlide is 1-indexed
        sentences=diastring.split("\n")
        finalLines=[] #will contain the final dialog, with each item being a line
        for sentence in sentences:
            if len(sentence)<=self.maxChars:
                finalLines.append(sentence)
            else:
                words=sentence.split()
                newLine=""
                for word in words:
                    #if you can fit one more word on the line, add it
                    if len(newLine)+len(word)<self.maxChars: 
                        newLine=newLine+word+" "
                    #if you can't, finalize the line and start a new one
                    else:
                        finalLines.append(newLine[0:-1])
                        newLine=word+" "
                finalLines.append(newLine[0:-1])
        while len(finalLines)<4:
            finalLines.append("")
        for i in range(0,len(finalLines)):
            finalLines[i]=finalLines[i].ljust(self.maxChars)
        ##Characterize and print the array       
        #top border line
        diAr=[["*TL"]]
        #make the menu box the same size (just big enough to accomodate the longest allowable line) every time
        for i in range(0,self.maxChars):
            diAr[0].append("T=")
        diAr[0].append("*TR")
        #assemble menu line for a given entry
        for line in finalLines:
            tmp=["L|"]
            for char in line: #break line into individual characters
                tmp.append(char)
            tmp.append("R|")
            diAr.append(tmp)
        lastLine=["*BL"]
        #make the menu box the same size (just big enough to accomodate the longest allowable line) every time
        for i in range(0,self.maxChars):
            lastLine.append("B=")
        lastLine.append("*BR")
        diAr.append(lastLine)
        return(diAr)
        
    def moveCursor(self,direction):
        if self.mode=="choice":
            if direction=="up":
                if self.curPos>1: #curPos=1 means cursor on top option
                    self.curPos-=1
                    if self.curPos<self.frame[0]:
                        self.frame[0]-=1
                        self.frame[1]-=1
                elif self.rollable:
                    self.curPos=len(self.tempOplist)
                    newTop=max(len(self.tempOplist)-screenHeight+2,1)#ensure no 0 or negatives
                    self.frame=[newTop,len(self.tempOplist)]
            elif direction=="down":
                if self.curPos<len(self.tempOplist):
                    self.curPos+=1
                    if self.curPos>self.frame[1]:
                        self.frame[0]+=1
                        self.frame[1]+=1
                elif self.rollable:
                    self.curPos=1
                    self.frame=self.getFrame()
        elif self.mode=="titledChoice":
            if direction=="up":
                if self.curPos>2: #curPos=2 means cursor on top option
                    self.curPos-=1
                    if self.curPos<=self.frame[0]:
                        self.frame[0]-=1
                        self.frame[1]-=1
                elif self.rollable:
                    self.curPos=len(self.tempOplist)
                    newTop=max(len(self.tempOplist)-screenHeight+3,1)
                    self.frame=[newTop,len(self.tempOplist)]
            elif direction=="down":
                if self.curPos<len(self.tempOplist):
                    self.curPos+=1
                    if self.curPos>self.frame[1]:
                        self.frame[0]+=1
                        self.frame[1]+=1
                elif self.rollable:
                    self.curPos=2
                    self.frame=self.getFrame

    def processInput(self,event,screen):
        if self.mode=="choice" or self.mode=="titledChoice":
            self.processInputChoice(event,screen)
        elif self.mode=="dialog":
            self.processInputDialog(event,screen)
            
    def processInputChoice(self, event, screen):
        if event.type==KEYDOWN:
            if event.key==K_UP:
                self.moveCursor("up")
            elif event.key==K_DOWN:
                self.moveCursor("down")
            elif event.key==K_a:
                exec(self.execOnA)
            elif event.key==K_s:
                exec(self.execOnS)

    def processInputDialog(self, event, screen):
        if event.type==KEYDOWN:
            if self.curSlide<len(self.tempOplist):
                self.curSlide+=1
            elif event.key==K_a:
                exec(self.execOnA)
            elif event.key==K_s:
                exec(self.execOnS)


    def mutateToNewMenu(self,newOptions,newMode=False):#Deprecated.
        #mutates the mode and oplist while retaining the stack and the execOn code.
        #Deprecated.
        if newMode:
            self.curMode=newMode
        if isinstance(newOptions,str):
            self.oplist=eval(newOptions)
        else:
            self.oplist=newOptions
        self.length=len(self.tempOplist)
        self.curPos=1

    def replaceMenu(self,newMenuInstance):
        self.screen.activeMenus[-1]=newMenuInstance

    def backUpMenuStack(self):
        self.screen.activeMenus=self.screen.activeMenus[:-1]

    def addToMenuStack(self,newMenu=False):
        #Gets a new menu from the menudict and adds it to the screen, while keeping the old menu visible behind it.
        #Use when going to a menu that should revert to the previous menu on pressing "S".
        oldMenu=self
        if not newMenu:
            newMenu=menuDict[self.tempOplist[self.curPos-1]]
        newMenu=newMenu.evaluatedCopy()
        self.screen.activeMenus.append(newMenu)

    def evaluatedCopy(self):
        #Returns a menu that is the same as self, but with the oplist evaluated if necessary.
        #Use for menus where the oplist depends on the game state and you don't want to mutate.
        #will probably be deprecated after the oplist constructor is its own argument
        if isinstance(self.oplist,str):
            print "evaluatedCopy got used"
            newOplist=eval(self.oplist)
            return menu(newOplist,self.mode,self.execOnA,self.execOnS,self.rollable,self.screen)
            #If you have changed the init arguments for menu and now things are breaking, this is probably the problem
            #Heed this prophecy, for it came true the first time within a day of its writing!
        else:
            return self
                    
########## Incidental menu-class functions that get run during menus at some point in the game. The execOnAs and execOnSs of various menus.
########## These will probably proliferate. It's alright. Didn't Tom Lehrer tell you? Proliferation is the word of the day.
    def pickStarter(self,name):
        if name=="Bulbasaur":
            starterMon=Bulbasaur(15,"Bulbasaur")
            #secondMon=Diglett(20,"Diglett")
            garyMon=Charmander(5,"Charmander")
        elif name=="Charmander":
            starterMon=Charmander(50,"Charmander")
            garyMon=Squirtle(5,"Squirtle")
        elif name=="Squirtle":
            starterMon=Squirtle(5,"Squirtle")
            garyMon=Bulbasaur(5,"Bulbasaur")
        starterMon.trainer=self.screen.player
        #secondMon.trainer=self.screen.player
        #thirdMon.trainer=self.screen.player
        self.screen.player.team=[starterMon]#,secondMon]#,thirdMon]
        self.screen.player.monsSeen.append(starterMon.species)
        self.screen.player.monsCaught.append(starterMon.species)
        garyMon.trainer=Gary
        Gary.team=[garyMon]
        self.screen.switchTo('world')

    def displayItemsList(self):
        result=[]
        names=Red.inventory.keys()
        for name in names:
            dispStr=str(self.screen.player.inventory[name]).rjust(2,"0")+"x"+name
            result.append(dispStr)
        return result

    def selectItemOutsideBattle(self):
        #get the current oplist
        if self.oplistConstructor:
            self.tempOplist=eval(self.oplistConstructor)
        else:
            self.tempOplist=self.oplist
        self.screen.player.selectedItemName=self.tempOplist[self.curPos-1].split("x",1)[1] #take only the part of "itemName: numberAvailable" before the colon
        if itemDict[self.screen.player.selectedItemName].targetsMon:
            self.addToMenuStack(itemChooseMon)
        else:
            self.itemOutsideBattle(False)

    def itemOutsideBattle(self,targetMonTeamIndex):
        itemName=self.screen.player.selectedItemName
        chosenItem=itemDict[itemName]
        targetMon=self.screen.player.team[targetMonTeamIndex] #mon instance or False if none is needed
        legal=chosenItem.isLegal(chosenItem,targetMon,False)
        if legal:
            useResultMessage=chosenItem.use(chosenItem,self.screen.player,targetMon)
            self.addToMenuStack(menu([useResultMessage],"dialog","self.backUpMenuStack()","self.backUpMenuStack()",False,False,self.screen))
            self.screen.player.selectedItemName=False
        else:
            self.addToMenuStack(menu(["What are you smoking? Now's not the time for that!"],"dialog","self.backUpMenuStack()","self.backUpMenuStack()",False,False,self.screen))


########## Battle menus: simplified menus for use in battle.
########## Currently used to display most of the available battle information, because graphics aren't done yet.
class battleMenu:
    def __init__(self,curMode,oplist):
        self.curMode=curMode #either "choice" or "dialog"
        self.oplist=oplist #list of messages if dialog, list of choices if choice
        self.length=len(self.oplist)
        self.curPos=1 #choice # or place in the messages list
        self.drawArray=[] #list of sprite
        self.maxChars=screenWidth-2
        self.maxLines=3
        self.canGoBack=True

    def switchMenu(self,newOptions,newMode=False):#switches to a new menu, in a new mode if necessary
        if newMode:
            self.curMode=newMode
        self.oplist=newOptions
        self.length=len(self.oplist)
        self.curPos=1
        
    def getArray(self):
        if self.curMode=="choice":
            array=self.getArrayChoice() #modify this to deal with null messages?
        elif self.curMode=="dialog":
            array=self.getArrayDialog() #modify this to deal with null messages?
        else:
            print self.curMode+"? That's not even a battle menu type."
        return array

    def getArrayChoice(self): #generates array with set of menu options for sprite generations
        #find length of longest menu item
        maxLength=2
        for op in self.oplist: #op needs to be a string
            opString=str(op)
            if len(opString)>maxLength:
                maxLength=len(opString)
        #top border line
        opAr=[["*TL"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("T=")
        opAr[0].append("*TR")
        #assemble menu line for a given entry
        for op in self.oplist:
            opString=str(op)
            tmp=["L|"," "] #open line with left-edge pipe and space for cursor
            tmpStr=opString.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("R|")#close line with pipe
            opAr.append(tmp)
        lastLine=["*BL"]
        for i in range(0,maxLength+1): #+1 for cursor
            lastLine.append("B=")
        lastLine.append("*BR")
        opAr.append(lastLine) #bottom border is same as top
        #draw cursor
        opAr[self.curPos][1]=">"
        return(opAr)

    def getArrayDialog(self):#generates array with dialog characters in a box
        #get raw string of dialog and break it up into lines
        diastring=self.oplist[self.curPos-1] #-1 bc curPos is 1-indexed
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
        for i in range(0,len(finalLines)):
            finalLines[i]=finalLines[i].ljust(self.maxChars)
            
        ##Characterize and print the array       
        #top border line
        diAr=[["*TL"]]
        #make the menu box the same size (just big enough to accomodate the longest allowable line) every time
        for i in range(0,self.maxChars):
            diAr[0].append("T=")
        diAr[0].append("*TR")
        #assemble menu line for a given entry
        for line in finalLines:
            tmp=["L|"]
            for char in line: #break line into individual characters
                tmp.append(char)
            tmp.append("R|")
            diAr.append(tmp)        
        lastLine=["*BL"]
        #make the menu box the same size (just big enough to accomodate the longest allowable line) every time
        for i in range(0,self.maxChars):
            lastLine.append("B=")
        lastLine.append("*BR")
        diAr.append(lastLine)
        return(diAr)

    def getNext(self):
        if self.curMode=="dialog":
            self.curPos+=1
            if self.curPos>len(self.oplist):
                return False
            else:
                return True
        if self.curMode=="choice":
            #Figure out the next menu and return appropriate string to feed to switchTo().
            return self.oplist[self.curPos-1]
            
            
        

        


#################### Puttin' on the MOVES ###################

class move:
    def __init__(self,name,basePwr, baseAcc, maxPP, nation, special, sideEffect, message=False, fastMove=False, critRate=1):#sideEffect can be string or False
            self.name=name
            self.basePwr=basePwr
            self.baseAcc=baseAcc
            self.maxPP=maxPP
            self.nation=nation
            self.special=special
            self.sideEffect=sideEffect
            self.message=message
            self.fastMove=fastMove #pre-empts Speed duel (quick attack, swift)
            self.critRate=critRate
            
            

    def __repr__(self):
        return self.name #hahahaha!

    def __str__(self):
        return self.name 

    def getCurPP(self,attacker):
        for i in range(0,numMoves):
            if self.name==attacker.curMoves[i].name:
                return attacker.curPP[i]

    def getHit(self,attacker,defender):
        messages=[]
        if (defender.curMove!="item" and defender.curMove.sideEffect and "offscreen" in defender.curMove.sideEffect):
            if defender.status["charging"]:
                hit=False,[] #auto-miss on dig and fly
        if attacker.status["confused"] and randint(0,1)==0:
            messages.append(attacker.name+" hurt itself in its confusion!")
            attacker.tempStats["HP"]-=hitYourself.getDamage(attacker,defender)
            hit=False
        
            
        
        else:
            if attacker.status["confused"]:
                messages.append(attacker.name+" attacked despite confusion!")
            hitChance=float(self.baseAcc)*attacker.accuracy/defender.evasion
            if randint(0,99)<hitChance:
                hit=True
            else:
                messages.append("... but it missed!")
                hit=False
        return (hit,messages)

    def getModifier(self,attacker,defender):
        #put some messages in here later
        #STAB
        if self.nation in attacker.nation:
            stab=1.5
        else:
            stab=1
        #Type matchup multiplier
        typeMod=self.getTypeModifier(attacker,defender)
        #critical
        critChance=self.critRate*attacker.critRate
        if random() <critChance:
            #critical hit!
            crit=2
        else:
            crit=1
        #damage range
        randomFactor=uniform(.85,1)
        modifier=stab*typeMod*crit*randomFactor
        return modifier

    def getTypeModifier(self,attacker,defender):
        typeMod=1
        typeMod*=typeDict[self.nation,defender.nation[0]]
        if len(defender.nation)>1:
            typeMod*=typeDict[self.nation,defender.nation[1]]
        return typeMod
        
    def getDamage(self,attacker,defender):
        modifier=self.getModifier(attacker, defender)
        if attacker.curMove.special:
            attackerAttack=attacker.tempStats["Special"]
            defenderDefense=defender.tempStats["Special"]
        else:
            attackerAttack=attacker.tempStats["Attack"]
            defenderDefense=defender.tempStats["Defense"]
        damage=float(2*attacker.level+10)/250*attackerAttack/defenderDefense*self.basePwr*modifier
        return ceil(damage)

    def getEffect(self,attacker,defender):
        #The logic behind this is complicated.
        #Some moves' effects are 3-word phrases of the form "[pokemon][accuracy/evasion/critRate][degree of change]".
        #Others are 3-word phrases of the form "[pokemon][stat][degree of change].
        #Still others are 2-word phrases of the form "[percent chance][possible status effect]",
        #And a final group are 2-word phrases of the form "[charging or multiple][number of turns or whether enemy is trapped]".
        #These possibilities are handled in the above order, with the exception of charging and multiple,
        #which must be handled before the damage is calculated and, therefore, before getEffect.

        messages=[]
        
        #check if an effect can succeed with the current type matchup, add relevant message
        typeModifier=self.getTypeModifier(attacker, defender)
        if typeModifier==0:
            return ["It has no effect!"] #effect will fail if there is one, do nothing
        elif typeModifier==0.5:
            messages.append("It's not very effective~")
        elif typeModifier==2:
            messages.append("It's super effective!")

        if self.sideEffect:#if there is an effect
            #break effect down into words
            effectWords=self.sideEffect.split()
            #handle weirdass arbitrary shit
            if effectWords[0]=="exec":
                exec(effectWords[1])
            #handle accuracy/evasion effects
            elif effectWords[1]=="accuracy" or effectWords[1]=="evasion":
                if effectWords[0]=="self":
                    call="attacker"
                    messages.append(attacker.name+self.message)
                else:
                    call="defender"
                    messages.append(defender.name+self.message)
                call+="."+effectWords[1]
                call+="*=1.4**"+effectWords[2]
                exec(call)
            #handle critRate effects
            elif effectWords[1]=="critRate":
                if effectWords[0]=="self":
                    call="attacker"
                    messages.append(attacker.name+self.message)
                else:
                    call="defender"
                    messages.append(defender.name+self.message)
                call+=".critRate="+call+".permStats['Speed']/512.0*"+effectWords[2]
                exec(call)
            #handle all other stat effects
            elif len(effectWords)==3:
                #if effect is a stat move
                if effectWords[0]=="self":
                    attacker.tempStats[effectWords[1]]*=1.4**float(effectWords[2])
                    messages.append(attacker.name+self.message)
                elif effectWords[0]=="enemy":
                    defender.tempStats[effectWords[1]]*=1.4**float(effectWords[2])
                    messages.append(defender.name+self.message)
            
            #handle 2-word status effects
            elif effectWords[0] not in ["charging","multiple","chain"]: #e.g. sleep, burn, etc.
                if effectWords[1] in defender.tempStats: #moves that probabilistically change stats
                    if randint(0,99)<int(effectWords[0]):
                        defender.tempStats[effectWords[1]]*=1.4**(-1.0)
                        messages.append(defender.name+self.message)
                else:
                    fail=False
                    if self.basePwr==0 and not defender.getEffectSuccess(effectWords[1]):
                        fail=True
                    if randint(0,99)<int(effectWords[0]) and not fail:
                        defender.status[effectWords[1]]=True
                        messages.append(defender.name+self.message)
                    if fail:
                        messages.append("But it failed!")

            #handle multiple
            elif effectWords[0]=="multiple" and attacker.status["multiple"]: #multiple move
                 enemyCanMove=not(effectWords[1]=="False" or effectWords[1]=="false")
                 if not enemyCanMove: #enemy cannot move
                     defender.status["trapped"]=True
        return messages

moveCode=open("Moves.py")
exec(moveCode.read())

class typeMatchup:
    def __init__(self):
        self.order=["Normal","Fighting","Flying","Poison","Ground","Rock","Bug",
                    "Ghost","Fire","Water","Grass","Electric","Psychic","Ice","Dragon"]
        self.typeDict={"Normal":[1,1,1,1,1,.5,1,0,1,1,1,1,1,1,1,1],
                  "Fighting":[2,1,.5,.5,1,2,.5,0,1,1,1,1,.5,2,1,1],
                  "Flying":[1,2,1,1,1,.5,2,1,1,1,2,.5,1,1,1,1],
                  "Poison":[1,1,1,.5,.5,.5,2,.5,1,1,2,1,1,1,1,1],
                  "Ground":[1,1,0,2,1,2,.5,1,2,1,.5,2,1,1,1,1],
                  "Rock":[0,.5,2,1,.5,1,2,1,2,1,1,1,1,2,1,1],
                  "Bug":[1,.5,.5,2,1,1,1,.5,.5,1,2,1,2,1,1,1],
                  "Ghost":[0,1,1,1,1,1,1,2,1,1,1,1,0,1,1,1],
                  "Fire":[1,1,1,1,1,.5,2,1,.5,.5,2,1,1,2,.5,1],
                  "Water":[1,1,1,1,2,2,1,1,2,.5,.5,1,1,1,.5,1],
                  "Grass":[1,1,.5,.5,2,2,.5,1,.5,2,.5,1,1,1,.5,1],
                  "Electric":[1,1,2,1,0,1,1,1,1,2,.5,.5,1,1,.5,1],
                  "Psychic":[1,2,1,2,1,1,1,1,1,1,1,1,.5,1,1,1],
                  "Ice":[1,1,2,1,2,1,1,1,1,.5,2,1,1,.5,2,1],
                  "Dragon":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
                  "Fail":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]}
        #keys in dict are attacker move type,
        #entries in values are type modifiers for each defender type
                   

    def lookup(self,attType,defType):
        row=self.typeDict[attType]
        colIndex=self.order.index(defType)
        typeMod=row[colIndex]
        return typeMod

    def __getitem__(self,k):
        #This is an amusingly versatile function. It can take a list. It can take a tuple. It can even take a dict, if you want to be disgusting.
        attType=k[0]
        defType=k[1]
        return self.lookup(attType,defType)
#don't forget to INIT IT!
typeDict=typeMatchup()

############ People (player and other trainers and NPCs)
class character:
    def __init__(self,team,name,sprite,money,beforeDialog=False,afterDialog=False,AI="normal",rewardItem=False):
        self.team=team
        self.name=name
        self.sprite=sprite
        self.money=money #money you get for beating them, or your money if it's you
        self.beforeDialog=beforeDialog
        self.afterDialog=afterDialog
        self.AI=AI #whether character is player, opponent, bad-AI opponent or good-AI opponent
        self.curMon=team[0] #mon that goes out when battle starts
        self.nextMon=False #the mon you're in the middle of switching to due to vagaries of control structure and turn timing
        self.inventory={}#the inventory used for display. Maps names to # you have.
        self.facingDict={"North":"_U","South":"_D","East":"_R","West":"_L","none":""}

    def getNumUnfainted(self):
        num=0
        for mon in self.team:
            if mon.tempStats["HP"]>0:
                num+=1
        return num
            
    def getNextMon(self): #returns new mon when one faints
        messages=[]
        #this is intended only for normal and bad AIs.
        #Better (gym leader/rival) AI and players should overload this in their subclasses.
        for mon in self.team:
            if mon.tempStats["HP"]>0:
                return(mon,messages)
        return (False,messages)

    def getNextMove(self):
        if self.curMon.status["multiple"]:
            return self.curMon.curMove
        if self.curMon.status["charging"]:
            return self.curMon.curMove
        moveList=self.curMon.curMoves
        nextMove=False
        if all([PP == 0 for PP in self.curMon.curPP]):
            return struggle
        if self.AI=="normal":
            while not nextMove:
                randomIndex=randint(0,len(moveList)-1)
                if self.curMon.curPP[randomIndex]>0:
                    nextMove=moveList[randomIndex]
            return nextMove
        if self.AI=="lousy":
            stackedMoveList=list(moveList)
            for move in moveList:
                if move.basePwr==0:
                    stackedMoveList.append(move)
                    stackedMoveList.append(move) #add really shitty moves twice
                elif move.basePwr<40:
                    stackedMoveList.append(moveP) #add kinda shitty moves once
            while not nextMove:
                randomIndex=randint(0,len(stackedMoveList)-1)
                tryMove=stackedMoveList[randomIndex]
                moveIndex=moveList.index(tryMove)
                if self.curMon.curPP[moveIndex]>0:
                    nextMove=tryMove
            return nextMove
        if self.AI=="awesome":
            stackedMoveList=list(moveList)
            for move in moveList:
                if move.basePwr>=60:
                    stackedMoveList.append(move)
                    stackedMoveList.append(move)
            while not nextMove:
                randomIndex=randint(0,len(stackedMoveList)-1)
                tryMove=stackedMoveList[randomIndex]
                moveIndex=moveList.index(tryMove)
                if self.curMon.curPP[moveIndex]>0:
                    nextMove=tryMove
            return nextMove

class PC(character):
    def __init__(self,name,gender,starterTeam,money):
        self.gender=gender
        if gender=="female":
            self.sprite="PCfemale"
        else:
            self.sprite="PCmale"
        character.__init__(self,starterTeam,name,self.sprite,0,"player")
        self.money=money
        self.monsSeen=[]
        self.monsCaught=[]
        self.encounterModifier=0#positive=more encounters, negative=fewer encounters
        self.activeItem=False #last still-active long-duration item used
        self.lastItem=False #last instantaneous item used
        self.stepsToItemEnd=0
        self.totalSteps=0
        self.facingDirection="South"

    def takeStep(self):
        self.totalSteps+=1
        if self.activeItem:
            self.stepsToItemEnd-=1
            if self.stepsToItemEnd==0:
                self.activeItem=False
                self.encounterModifier=0
                #add other lines here to neutralize other possible active items as they appear

    def teamAsString(self):
        res=[]
        for i in self.team:
            res.append(str(i))
        return res

    def wikidexAsList(self):
        statsString='Punkemon seen: '+str(len(self.monsSeen))+'\n'+'Punkemon caught: '+str(len(self.monsCaught))
        return [statsString]

    def hasUnfaintedMons(self):
        for i in self.team:
            if i.tempStats["HP"]>0:
                return True
        return False

class wildPunkemon(character):
    def __init__(self,name,team):
        self.name=name
        self.team=team
        character.__init__(self,self.team,name,False,0,"normal")




##############Items ##############################
itemDict={}
class item:
    def __init__(self,name,useFunction,legalFunction,battleUseable,targetsMon=True): 
        #name as it appears in the inventory
        self.name=name
        #function that takes a player and performs the action of that player using that item
        #unique to each of potion, super potion, repel, water stone, etc.
        self.use=useFunction
        self.isLegal=legalFunction
        self.battleUseable=battleUseable
        #targetsMon is true if the item needs to be used on a specific punkemon (e.g. potions or stones), false otherwise (e.g. repel, escape rope)
        self.targetsMon=targetsMon
        itemDict[self.name]=self

        
    def healMon(self,player,target,numHP):
        if player.inventory[self.name]>0:
        #make sure this can only be called on an item that has been in the inventory at least once
        #otherwise it will throw a keyError
            player.inventory[self.name]-=1
            oldHP=target.tempStats["HP"]
            newHP=min(target.tempStats["HP"]+numHP,target.permStats["HP"])
            target.tempStats["HP"]=newHP
            return target.name+" recovered "+str(newHP-oldHP)+" HP."
        else:
            return "You don't have any!"
        
    def usePotion(self,player,target):
        return self.healMon(player,target,20)
    
    def useSuperPotion(self,player,target):
        return healMon(player,target,50)

    def potionLegal(self,target,inBattle):
        return target.permStats["HP"]>target.tempStats["HP"]>0

    def repel(self,player,modifier,duration):
        if player.inventory[self.name]>0:
            player.inventory[self.name]-=1
            player.encounterModifier=modifier
            player.activeItem=self
            player.stepsToItemEnd=duration
            return "Repel was used successfully."
        else:
            return "You don't have any!"

    def useRepel(self,player,target):
        return self.repel(player,-10,500) #sanity-check these numbers!

    def repelLegal(self,target,inBattle):
        return not inBattle

    def useRevive(self,player,target):
        if player.inventory[self.name]>0:
            player.inventory[self.name]-=1
            target.tempStats["HP"]=0.5*target.permStats["HP"]
            return target.name+" was revived!"
        else:
            return "You don't have any!"
            
    def reviveLegal(self,target,inBattle):
        return target.tempStats["HP"]<=0

    def useBall(self,player,target,ballLevel):
        if player.inventory[self.name]>0:
            player.inventory[self.name]-=1
            catchSuccess=True #replace this with some math using ballLevel and the target mon and the phase of the moon and stuff
            if catchSuccess:
                target.duplicate(player,"Steve")
            return catchSuccess
        else:
            return "You don't have any!"

    def ballLegal(self,target,inBattle):
        return isinstance(target.trainer,wildPunkemon)

    def usePunkeball(self,player,target):
        return self.useBall(player,target,1) #change 1 to the number associated with standard balls in the formula

    def useStone(self,player,target,stoneType):
        if player.inventory[self.name]>0:
            player.inventory[self.name]-=1
            if len(target.evolveStone)==1:
                nextEvolution=target.nextEvolution
                target.duplicate(False,nextEvolution,nextEvolution)
            else: #special case for eevee, because eevee is a special snowflake
                nextEvolution=target.evolveDict[stoneType]
                target.duplicate(False,nextEvolution,nextEvolution)
            return target.name+" evolved into "+nextEvolution+"!"
        else:
            return "You don't have any!"

    def stoneLegal(self,target,inBattle,stoneType):
        return (target.evolveStone and stoneType in target.evolveStone)

    def useWaterStone(self,player,target):
        return self.useStone(player,target,"water")

    def waterStoneLegal(self,target,inBattle):
        return self.stoneLegal(target,inBattle,"water")

    def useFireStone(self,player,target):
        return self.useStone(player,target,"fire")

    def fireStoneLegal(self,target,inBattle):
        return self.stoneLegal(target,inBattle,"fire")

    def useThunderStone(self,player,target):
        return self.useStone(player,target,"thunder")

    def thunderStoneLegal(self,target,inBattle):
        return self.stoneLegal(target,inBattle,"thunder")
    
    def useMoontone(self,player,target):
        return self.useStone(player,target,"moon")

    def moonStoneLegal(self,target,inBattle):
        return self.stoneLegal(target,inBattle,"moon")

    def useLeafStone(self,player,target):
        return self.useStone(player,target,"leaf")

    def leafStoneLegal(self,target,inBattle):
        return self.stoneLegal(target,inBattle,"leaf")
        

potion=item("Potion",item.usePotion,item.potionLegal,True,True)
superPotion=item("Super potion",item.useSuperPotion,item.potionLegal,True,True)
repel=item("Repel",item.useRepel,item.repelLegal,False,False)
revive=item("Revive",item.useRevive,item.reviveLegal,True,True)
punkeball=item("Punkeball",item.usePunkeball,item.ballLegal,True,False)
#more balls
waterStone=item("Water stone",item.useWaterStone,item.waterStoneLegal,True,True)
fireStone=item("Fire stone",item.useFireStone,item.fireStoneLegal,True,True)
thunderStone=item("Thunder stone",item.useThunderStone,item.thunderStoneLegal,True,True)
moonStone=item("Moon stone",item.useMoontone,item.moonStoneLegal,True,True)
leafStone=item("Leaf stone",item.useLeafStone,item.leafStoneLegal,True,True)

##############Sprites! ###########################
terrainDict={"T":1,"x":1,"-":0,"G":3,"w":4,"O":2," ":0,"B1":1}
#human-readable terrain dict: T=tree, x=rock, G=tall grass, w=water
    
##class sprite:
##    def __init__(self,longName,screenName,fileLocation,screen,pos,terrain=False,destination=False):
##        self.longName=longName #(e.g. "tree", "mart", "rock")
##        self.screenName=screenName#(e.g. T, X, @)
##        self.fileLoc=fileLocation #file name and any necessary path
##        self.screen=screen
##        self.pos=pos #A two-element list with the coordinates of the top left corner (from top left of screen, +y is down)
##        self.drawMap=self.screen.drawMap
##        self.drawMap[pos[0]][pos[1]]=self.screenName #put the square in the draw map
##        self.terrain=terrain
##        #0=passable, 1=impassable, 2=screen change, 3=encounter, 4=water
##        self.destination=destination
##        #if not False, this will be a 2-element list with new world instance and initial player coordinates upon entering that world
##        self.terrainMap=self.screen.terrainMap
##        self.terrainMap[pos[0]][pos[1]]=self.terrain #put the square in the terrain map



######################### Building and its subclasses

##We need to work out what we were doing here and make sure it isn't stupid or half-finished.
        
class building:
    def __init__(self,inputMap,shortName): #defaults are for houses you can't go in
        self.inputMap=inputMap
        self.shortName=shortName
        #Example:
        ##B1=[
        ##   [1,1,1]
        ##   [1,"O1",1]
        ##         ]

    def addToMap(self,terrainMap, spriteMap,xpos,ypos,backTerrain):
        #Starting at the provided x and y positions [upper left corner of building]...
        curX=xpos
        curY=ypos
        #iterate over the huilding's input map. 
        for row in self.inputMap:
            for char in row:
                #First, figure out if it's a door.
                if isinstance(char,screenChanger):
                    #set terrain there to be a screen change
                    terrainMap[curY][curX]=2
                    #add the door to the world's sprite map
                    spriteMap[curY][curX]=(char,backTerrain)
                else:
                    # just set terrain to the appropriate type:
                    terrainMap[curY][curX]=char 
                curX+=1 #increment the x position as we move across the row                    
            curY+=1   #increment row at end of each row...
            curX=xpos #...and reset the x to the position of the lefthand side of the building
        #Once done with that, add ourself to the appropriate spot in the spriteMap:
        spriteMap[ypos][xpos]=(self,backTerrain)
        #Now done with the map, end this function...

    def addToSurface(self,screen,pos):
        #Draws the building's sprite to the provided screen at the given pos (x,y)
        screen.blit(pygame.image.load(os.path.join("sprites",self.shortName+".png")),pos)


class testBuilding(building):
    def __init__(self,entrance):
        testBuildingMap=[[1,1,1],
                         [1,entrance,1]]
        building.__init__(self,testBuildingMap,"B1") #B1.jpg will be the sprite

    

############################# screenChanger
class screenChanger:
    def __init__(self,name,sprite,destination,startPos): #sprite will be the filename of the sprite, e.g. "stairUp"
        self.name=name #the unique name of an individual ladder or stair or cave or whatever
        self.sprite=sprite #sprite will be the filename of the sprite, e.g. "stairUp"
        self.destination=destination
        self.startPos=startPos

    def addToSurface(self,screen,pos):
        screen.blit(pygame.image.load(os.path.join("sprites",self.sprite+".png")),pos)
    
        


class monSeed:
    def __init__(self,ticketDict,encounterRate):
        self.ticketDict=ticketDict#maps mon instances to number of lottery tickets that mon gets
        self.encounterRate=encounterRate #between 0 and 100
        self.allMons=self.ticketDict.keys()

    def getFight(self,encounterModifier):
        tempEncounterRate=self.encounterRate+encounterModifier
        if randint(0,100)<tempEncounterRate:
            #if encounterRate=100, always picks a mon
            #if encounterRate=0, never picks a mon
            return self.pickMon()
        else:
            return False

    def pickMon(self): #returns each mon with probability proportional to its share of the tickets
        totalTickets=0
        for mon in self.allMons:
            totalTickets+=self.ticketDict[mon]
        winner=randint(1,totalTickets)
        curTicket=0
        for mon in self.allMons:
            curTicket+=self.ticketDict[mon]
            if curTicket>=winner:
                return mon

############# Actionables npcs, enemy trainers, cuttable trees, item balls, wandering punkemon, stuff you walk up to and press A basically
class actionable:
    def __init__(self,pos,sprite,sightLine):
        self.permPos=pos
        self.tempPos=list(self.permPos)
        self.sprite=sprite
        self.sightLine=sightLine#the distance they can see
        self.sightLineSquares=[] #this will get populated when the world inits
        self.facingDict={"North":"_U","South":"_D","East":"_R","West":"_L","none":""}

    def getSightLine(self,terrainMap): #returns a list of 2-item locations that are their sightline
        sightLineSquares=[]
        curPos=self.tempPos #[X,Y]
        blocked=False
        counter=0
        while not blocked and counter<=self.sightLine:
            counter+=1
            if self.facingDirection=="North":
                nextPos=[curPos[0],curPos[1]-1]
            elif self.facingDirection=="South":
                nextPos=[curPos[0],curPos[1]+1]
            elif self.facingDirection=="East":
                nextPos=[curPos[0]+1,curPos[1]]
            elif self.facingDirection=="West":
                nextPos=[curPos[0]-1,curPos[1]]
            elif self.facingDirection=="none":
                nextPos=[curPos[0],curPos[1]]
                blocked=True
            if nextPos[0]<0 or nextPos[1]<0 or nextPos[0]>len(terrainMap[0]) or nextPos[1]>len(terrainMap):
                blocked=True
            if not blocked:
                newTerr=terrainMap[nextPos[1]][nextPos[0]]
                if newTerr in (0,3,4,6):
                    sightLineSquares.append(nextPos)
                    curPos=nextPos
        self.sightLineSquares=sightLineSquares
        return sightLineSquares                

    def respond(self):
        return #This function gets called when you walk up to an actionable and press A. Remember to overwrite it for every subclass

    def addToSurface(self,screen,pos):
        #Draws the actionable's sprite to the provided screen at the given pos (x,y)
        screen.blit(pygame.image.load(os.path.join("sprites",self.sprite+self.facingDict[self.facingDirection]+".png")),pos)
        

class NPC(actionable): #randos who stand around and talk and don't fight
    def __init__(self,name,pos,dialog,sprite,facingDirection="South",item=False,sightLine=0):
        self.name=name
        self.dialog=dialog #a dialog menu that ends with switching to World
        self.sprite=pygame.image.load(os.path.join("sprites","npc.png")) #change this when you give npcs their own individual sprites
        self.permPos=pos#2-element list of their position in the world [X,Y]
        self.tempPos=list(self.permPos)
        self.facingDirection=facingDirection
        self.sightLine=sightLine
        #do something about telling the world about the NPCs and characters in it
        self.item=item #the item they give you, if they give you an item
        actionable.__init__(self,pos,sprite,sightLine)

    def respond(self):
        return ("menu",self.dialog)
        #bring up a menu with self.dialog

class NPCTrainer(actionable): #randos who stand around and DO fight
    def __init__(self,pos,sprite,trainer,facingDirection="South",foughtDialog=["I did my best! I have no regrets!"]):
        self.trainer=trainer
        self.sprite=pygame.image.load(os.path.join("sprites","enemy.png")) #change this when you give trainers their own individual sprites
        self.permPos=pos#2-element list of their position in the world
        self.tempPos=list(self.permPos)
        self.facingDirection=facingDirection
        self.trainer.fought=False
        self.beforeDialog=self.trainer.beforeDialog
        self.afterDialog=self.trainer.afterDialog
        self.foughtDialog=menu(foughtDialog,"dialog","self.screen.switchTo('world')","self.screen.switchTo('world')")
        actionable.__init__(self,pos,sprite,5)

    def getSightLine(self,terrainMap): #returns a list of 2-item locations that are their sightline
        if self.trainer.fought:
            return []
        else:
            return actionable.getSightLine(self,terrainMap)

    def respond(self):
        if not self.trainer.fought:
            opponent=self.trainer
            if self.trainer.beforeDialog:
                return ("menu",self.beforeDialog)
            else:
                return ("battle",opponent)
        else:
            return ("menu",self.foughtDialog)

    def activate(self,playerPos):
        if self.facingDirection=="North":
            while self.tempPos[1]!=playerPos[1]-1:
                self.tempPos[1]+=1
        elif self.facingDirection=="South":
            while self.tempPos[1]!=playerPos[1]+1:
                self.tempPos[1]-=1
        elif self.facingDirection=="West":
            while self.tempPos[0]!=playerPos[0]+1:
                self.tempPos[0]-=1
        elif self.facingDirection=="East":
            while self.tempPos[0]!=playerPos[0]-1:
                self.tempPos[0]+=1
        return self.respond()
        

 ################ init central for worlds, buildings, entrances, and associate maps           
#general policy: initialize all portals with false,
#then the buildings on the maps,
#then the mon seeds,
#then the maps themselves,
#then create the worlds containing the buildings,
#then init the portals again with their destinations set.
#Otherwise you get circular dependencies.


########## Entrances with FALSE
O1=screenChanger("O1","door",False,[1,1])

########## Buildings
B1=testBuilding(O1)


########## Maps    
testMap=[ #obsolete one-char map design
        ["x","x","x","x","x","x"],
        ["x","G","G","G","G","x"],
        ["x"," "," "," "," ","x"],        
        ["x"," "," "," "," ","x"],
        ["x","T","T","-","-","x"],
        ["x",B1," "," "," ","x"],
        ["x"," "," "," "," ","x"],
        ["x",O1," "," "," ","x"],
        ["x","x","x","x","x","x"]
                                ]

blankMap=[ #obsolete one-char map design
        ["x","x","x","x","x","x"],
        ["x"," "," "," "," ","x"],
        ["x"," "," "," "," ","x"],        
        ["x"," "," "," "," ","x"],
        ["x"," "," "," "," ","x"],
        ["x"," "," "," "," ","x"],
        ["x"," "," "," "," ","x"],
        ["x"," "," "," "," ","x"],
        ["x","x","x","x","x","x"]
                                ]

doubleMap=[
        [" G"," G"," G"," G"," G"," G"],
        ["xG"," G"," G"," G"," G","xG"],
        ["x-"," -"," -"," -"," -","x-"], 
        ["x-"," -"," -"," -"," -","x-"],
        ["x-","T ","T "," -"," -","x-"],
        ["x ","  ","  ","  ","  ","x "],
        ["x ","  ","  ","  ","  ","x "],
        ["x ","  ","  ","  ","  ","x "],
        ["x ","x ","x ","x ","  ","x "]
                                ]

buildingMap=[
        [" G"," G"," G"," G"," G"," G"],
        ["xG"," G"," G"," G"," G","xG"],
        ["x-"," -"," -"," -"," -","x-"], 
        ["x-"," -"," -"," -"," -","x-"],
        ["x-","T ","T "," -"," -","x-"],
        ["x ",(B1," "),"  ","  ","  ","x "],
        ["x ","  ","  ","  ","  ","x "],
        ["x ","  ","  ","  ","  ","x "],
        ["x ","x ","x ","x ","  ","x "]
                                ]

    

############Screen and high-level "running the game" stuff##############
    
class screen:
    #runs at start of screen, conducts background setup before first loop
    def __init__(self,xDim,yDim,curWorld):
        pygame.init()
        self.xDim=xDim #screen width in sprites, must be odd to keep player in center
        self.yDim=yDim #screen height in sprites must be odd to keep player in center
        if xDim%2==0:
            print "xDim is even, make it odd."
        if yDim%2==0:
            print "yDim is even, make it odd."
        self.screenSize=(pixel*xDim,pixel*yDim)
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(255,255,255)
        self.gameScreen.fill(self.backgroundColor)
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.curMenu=Intro
        self.activeMenus=[Intro]
        self.playerIsSurfing=False
        self.changeWorld=False
        self.mode="newMenu"
        self.curWorld=curWorld
        self.playerPos=[1,1] #Initial position [x,y] of the player.
        self.switchTo(self.mode)
        self.player=Red
        Red.facingDirection="South"
        self.curBattle=False #battle(Red,Gary,self)
        for menu in allMenus:
            menu.screen=self
        self.running=True

        #The following needs to be the last line in __init__!
        self.mainloop()
        
    
    def switchTo(self,mode):
        self.mode=mode
        if mode=="menu":
            print "vanilla menu mode"
            self.processInput=self.menuInput
            self.drawScreen=self.drawMenu
        elif mode=="newMenu":
            self.needNewSlice=True
            self.processInput=self.newMenuInput
            self.drawScreen=self.drawNewMenu
        elif mode=="world":
            self.activeMenus=[placeholderMenu]
            self.processInput=self.worldInput
            self.drawScreen=self.drawWorld
            self.worldUpdate()#make sure there's a world slice for your world.
            self.terrainDebugMode=False
            self.drawWorld()
        elif mode=="battle":
            self.activeMenus=[placeholderMenu]
            self.processInput=self.battleInput
            self.drawScreen=self.drawBattle
        else:
            print "I don't know how to switch to "+mode+". You and your expectations."
    
    def mainloop(self):
        while self.running:
            if self.mode=="menu":
                #find out what the user has done
                event=self.getInput()
                #deal with it, updating gamestate accordingly
                self.processInput(event)#this will be a different function depending on what's going on
                #draw
                self.drawScreen()#this will be a different function depending on what's going on
                self.clock.tick(self.fps)

            elif self.mode=="newMenu":
                self.needNewSlice=False
                event=self.getInput()
                self.processInput(event)
                self.drawScreen()
                self.clock.tick(self.fps)
                                         
            elif self.mode=="battle":
                event=self.getInput() #if in battle mode, then self.getInput=self.getBattleInput
                self.processInput(event) 
                self.drawScreen()
                self.clock.tick(self.fps)
                
            elif self.mode=="world":
                event=self.getInput()
                self.processInput(event)
                self.worldUpdate()
                if event:
                    self.drawScreen()
                self.clock.tick(self.fps)
        pygame.display.quit() #after you quit and running turns off, the while will exit and the display will quit
                
                    
    #find the first valid input and pass to input processor
    #if no valid input, pass Null
    def getInput(self):
        goodKeys=[K_a, K_s, K_m, K_SPACE, K_UP, K_DOWN, K_RIGHT, K_LEFT]
        #add > and < later for time warp and p for pause
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.running=False
                #WE SHOT DOWN A WINDOW
                #pygame.display.quit()#shh!
                #wE shot down a WINdow
                break
            elif event.type==KEYDOWN:
                if event.key in goodKeys:
                    return event
        return False           

    #process the input
    def menuInput(self,event):
        if event is fakeAPress:
            print "Processing a FAKE KEY!? That's unethical!"
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        else:
            self.activeMenus[-1].processInput(event, self)

    def newMenuInput(self,event):
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        elif event.key==K_SPACE and self.activeMenus[-1]==start:
            self.activeMenus=[placeholderMenu]
            self.switchTo("world")
        else:
            self.activeMenus[-1].processInput(event, self)
    
    def battleInput(self,event):
        if not event:
            return
        else:
            self.curBattle.curAction(event)

    def worldInput(self,event):
        #You should probably move all the world functions to their own class like with Battle
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        elif event.key==K_a:
            if self.player.facingDirection=="North":
                actSquare=[self.playerPos[0],self.playerPos[1]-1]
            if self.player.facingDirection=="South":
                actSquare=[self.playerPos[0],self.playerPos[1]+1]
            if self.player.facingDirection=="West":
                actSquare=[self.playerPos[0]-1,self.playerPos[1]]
            if self.player.facingDirection=="East":
                actSquare=[self.playerPos[0]+1,self.playerPos[1]]
            thingFound=self.curWorld.tempSpriteMap[actSquare[1]][actSquare[0]][0]
            if isinstance(thingFound,actionable):
                if thingFound.facingDirection!="none":
                    if self.player.facingDirection=="North":
                        thingFound.facingDirection=="South"
                    if self.player.facingDirection=="South":
                        thingFound.facingDirection=="North"
                    if self.player.facingDirection=="East":
                        thingFound.facingDirection=="West"
                    if self.player.facingDirection=="West":
                        thingFound.facingDirection=="East"
                response=thingFound.respond()
                self.processResponse(response)
        elif event.key==K_SPACE:
            self.activeMenus=[start]
            self.switchTo("newMenu")
        elif event.key==K_s:
            return
        elif event.key==K_m:#toggle terrain-debug mode
            self.terrainDebugMode=not self.terrainDebugMode  
        else: #move the player around
            if event.key==K_UP:
                self.player.facingDirection="North"
                tempPos=[self.playerPos[0],self.playerPos[1]-1]
            elif event.key==K_DOWN:
                self.player.facingDirection="South"
                tempPos=[self.playerPos[0],self.playerPos[1]+1]
            elif event.key==K_LEFT:
                self.player.facingDirection="West"
                tempPos=[self.playerPos[0]-1,self.playerPos[1]]
            elif event.key==K_RIGHT:
                self.player.facingDirection="East"
                tempPos=[self.playerPos[0]+1,self.playerPos[1]]
            self.playerPos=self.checkMove(tempPos) #checkMove should return tempPos if the attempted square is passable, playerPos otherwise
            if self.newOpponent and self.player.hasUnfaintedMons():
                self.newOpponent.heal()
                wildTrainer=wildPunkemon("Wild "+self.newOpponent.name,[self.newOpponent])
                self.newOpponent.trainer=wildTrainer
                self.curBattle=battle(self.player,wildTrainer,self)
                self.switchTo("battle")

    def processResponse(self,response):
        if response[0]=="menu":
            self.activeMenus[-1]=response[1]
            self.activeMenus[-1].curSlide=1
            self.switchTo("newMenu")
        elif response[0]=="battle":
            if self.player.hasUnfaintedMons():
                self.curBattle=battle(self.player,response[1],self)
                self.switchTo("battle")
            else:
                self.switchTo("world")

    def checkMove(self,tempPos):
        #Returns the new position after an attempted move
        #If player can move into attempted square, returns new position
        #if player cannot move into attempted square, returns old position
        #if player stepped on a screenChanger, return False to signal to worldUpdate() that it needs to handle a world change
        tryX=tempPos[0]
        tryY=tempPos[1]
        self.changeWorld=False
        self.newOpponent=False
        if tryX>=len(self.curWorld.tempTerrainMap[0]) or tryX<0:
            return self.playerPos
        if tryY>=len(self.curWorld.tempTerrainMap) or tryY<0:
            return self.playerPos
        newTerrain=self.curWorld.tempTerrainMap[tryY][tryX] #gets terrain type of square you're trying to move to
        #demons happen ##meta-comment: I have no idea to what the first comment on this line refers.
        if newTerrain==0:
            self.player.takeStep()
            return tempPos #can always walk on walkable terrain
        elif newTerrain==1:
            return self.playerPos #can never walk on impassable terrain
        elif newTerrain==2:
            self.player.takeStep()
            self.changeWorld=True
            return tempPos
        elif newTerrain==3:
            self.player.takeStep()
            self.newOpponent=self.curWorld.landMonSeed.getFight(self.player.encounterModifier) #returns mon instance or False
            return tempPos #can move into square, encounters are possible
        elif newTerrain==4: #new terrain is water
            if self.playerIsSurfing:
                self.player.takeStep()
                self.newOpponent=self.curWorld.waterMonSeed.getFight(self.player.encounterModifier)
                return tempPos #if surfing, they can step into water
            else:
                return self.playerPos #cannot into water and covered in fleas
        elif newTerrain==5: #an actionable is here
            return self.playerPos
        elif newTerrain==6:
            for item in self.curWorld.actionables:
                if tempPos in item.sightLineSquares:
                    response=item.activate(tempPos)
                    self.processResponse(response)
            return tempPos
            
        
    def getWorldSlice(self,whichMap="draw"):#pads and crops the world map.
        #[This world map has been modified from its original version. It has been formatted to fit your screen.]
        #self.curWorld,self.xDim,self.yDim,self.playerPos
        xDim=self.xDim
        yDim=self.yDim
        paddingChar=self.curWorld.paddingChar
        if whichMap=="draw":
            startDrawMap=safeCopy(self.curWorld.tempDrawMap)
        elif whichMap=="sprite":
            startDrawMap=safeCopy(self.curWorld.tempSpriteMap)
        playerX=self.playerPos[0]#might need to change this
        playerY=self.playerPos[1]#might need to change this
        topRow=playerY-(self.yDim-1)/2
        
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

        leftCol=playerX-(xDim-1)/2
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
        choppedMap[centerY][centerX]="@"+choppedMap[centerY][centerX][1]
        return choppedMap


    def worldUpdate(self):
        if self.changeWorld:
        #this means we need to change the curWorld
            self.curWorld.resetWorld()
            warpSquare=self.curWorld.tempSpriteMap[self.playerPos[1]][self.playerPos[0]][0] #warpSquare is the screenChanger instance you stepped on
            self.playerPos=warpSquare.startPos
            self.curWorld=warpSquare.destination
            self.changeWorld=False
        self.curWorld.updateMaps()#WRITE THIS FUNCTION
        self.worldSlice=self.getWorldSlice()
        self.spriteSlice=self.getWorldSlice("sprite")
            
    def drawWorld(self,surface=False):
        if not surface:
            surface=self.gameScreen
        surface.fill(self.backgroundColor)
        drawPos=[0,0]
        drawArray=self.spriteSlice
        secondList=[]
        for row in drawArray:
            drawPos[0]=0
            for cell in row:
                if isinstance(cell,tuple):
                    secondList.append(tuple(drawPos)) #handle its sprite later, but do blit the background
                    surface.blit(worldBGSpriteDict[cell[1]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                elif not self.terrainDebugMode:
                    surface.blit(worldBGSpriteDict[cell[1]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                    if cell[0]=="@":
                        surface.blit(worldFGSpriteDict[cell[0]+self.player.facingDict[self.player.facingDirection]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                    else:
                        surface.blit(worldFGSpriteDict[cell[0]],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                else:
                    player=(cell[0]=="@")
                    surface.blit(self.getTerrainTile(self.curWorld.getTerrain(cell),player),dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                drawPos[0]+=1
            drawPos[1]+=1
        for item in secondList:
            sprite = self.spriteSlice[item[1]][item[0]][0]
            drawPos=[item[0]*pixel, item[1]*pixel]
            if isinstance(sprite,(building,screenChanger,actionable)):
                sprite.addToSurface(surface,drawPos)
            else:
                print "not adding", sprite
        if surface==self.gameScreen:
            pygame.display.flip() #otherwise we're drawing to a stored image
        else:
            return surface

    def getTerrainTile(self,terrNum,player=False):
        canvas=pygame.Surface((pixel,pixel),0,32)
        colorDict={0:(200,200,200),1:(0,0,0),2:(255,0,0),3:(0,255,0),4:(0,0,255)}
        canvas.fill(colorDict[terrNum])
        if player:
            pygame.draw.circle(canvas, (255,165,0), (pixel/2,pixel/2), int(pixel*.4), 0)
        return canvas
    
    def drawMenu(self):
        self.gameScreen.fill(self.backgroundColor)
        for menu in self.activeMenus:
            if menu.oplistConstructor:
                menu.tempOplist=eval(menu.oplistConstructor)
            drawPos=[0,0]
            drawArray=menu.getArray()
            for row in drawArray:
                drawPos[0]=0
                for cell in row:
                    self.gameScreen.blit(menuSpriteDict[cell],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                    drawPos[0]+=1
                drawPos[1]+=1
        pygame.display.flip()

    def drawNewMenu(self):
        #if the screen has changed, update the background image
        if self.needNewSlice:
            self.gameSlice=self.drawWorld(self.gameSlice)
        #draw the background image
        self.gameScreen.blit(self.gameSlice,dest=(0,0))
        #DRAW ALL THE MENUS
        for menu in self.activeMenus:
            if menu==self.activeMenus[-1]:
                top=True
            else:
                top=False
            if menu.oplistConstructor:
                menu.tempOplist=eval(menu.oplistConstructor)
            drawPos=[0,0]
            drawArray=menu.getArray(top)
            for row in drawArray:
                drawPos[0]=0
                for cell in row:
                    self.gameScreen.blit(menuSpriteDict[cell],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                    drawPos[0]+=1
                drawPos[1]+=1
        pygame.display.flip()

    def drawBattle(self):
        self.drawBattleMenu() 
        self.drawBattleGraphics()
        pygame.display.flip()

    def drawBattleMenu(self): #modify this to deal with null messages?
        self.gameScreen.fill(self.backgroundColor)
        drawPos=[0,0]
        drawArray=self.curBattle.getArray()
        for row in drawArray:
            drawPos[0]=0
            for cell in row:
                self.gameScreen.blit(menuSpriteDict[cell],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                drawPos[0]+=1
            drawPos[1]+=1

    def drawBattleGraphics(self):
        #health bars
        if not self.player.curMon:
            playerHealthFraction=0.0
        else:
            playerHealthFraction=(self.player.curMon.tempStats["HP"]+0.0)/self.player.curMon.permStats["HP"]
        if not self.curBattle.enemy.curMon:
            enemyHealthFraction=0.0
        else:
            enemyHealthFraction=(self.curBattle.enemy.curMon.tempStats["HP"]+0.0)/self.curBattle.enemy.curMon.permStats["HP"]
        playerHealthBarPos=(15*pixel,15*pixel)
        enemyHealthBarPos=(2*pixel,8*pixel)
        healthBarWidth=9
        self.gameScreen.blit(self.getHealthBar(healthBarWidth,1,playerHealthFraction),playerHealthBarPos)
        self.gameScreen.blit(self.getHealthBar(healthBarWidth,1,enemyHealthFraction),enemyHealthBarPos)

        #xp bar
        mon=self.player.curMon
        if mon:
            XPSinceLast=mon.XP-mon.getXP()#XP earned since last levelup
            XPLastToNext=mon.getXP(mon.level+1)-mon.getXP()#XP between last levelup and next levelup
            XPFraction=(XPSinceLast+0.0)/(XPLastToNext)
            XPBarBlue=pygame.Rect(playerHealthBarPos[0],playerHealthBarPos[1]+pixel,healthBarWidth*pixel*XPFraction,5)
            XPBarGray=pygame.Rect(playerHealthBarPos[0]+healthBarWidth*pixel*XPFraction,playerHealthBarPos[1]+pixel,healthBarWidth*pixel*(1-XPFraction),5)
            pygame.draw.rect(self.gameScreen,(0,50,200),XPBarBlue)
            pygame.draw.rect(self.gameScreen,(150,150,150),XPBarGray)
            

        #mon names
        if self.player.curMon:
            playerMonNameSurface=self.getTextSurface(self.player.curMon.name)
            self.gameScreen.blit(playerMonNameSurface,((screenWidth-len(self.player.curMon.name)-1)*pixel,playerHealthBarPos[1]-2*pixel))
        if self.curBattle.enemy.curMon:
            enemyMonNameSurface=self.getTextSurface(self.curBattle.enemy.curMon.name)
            self.gameScreen.blit(enemyMonNameSurface,(enemyHealthBarPos[0],enemyHealthBarPos[1]-2*pixel))
        
        #total mons and mons remaining
        playerMonsUnfainted=[]
        enemyMonsUnfainted=[]
        for mon in self.curBattle.player.team:
            if mon.tempStats["HP"]==mon.permStats["HP"]:
                playerMonsUnfainted.append(2)
            elif mon.tempStats["HP"]>0:
                playerMonsUnfainted.append(1)
            else:
                playerMonsUnfainted.append(0)
        for mon in self.curBattle.enemy.team:
            if mon.tempStats["HP"]==mon.permStats["HP"]:
                enemyMonsUnfainted.append(2)
            elif mon.tempStats["HP"]>0:
                enemyMonsUnfainted.append(1)
            else:
                enemyMonsUnfainted.append(0)
        for i in range(0,len(playerMonsUnfainted)):
            if playerMonsUnfainted[i]==2: #undamaged mon, blit regular punkeball
                ballSprite=pokeball_team
            elif playerMonsUnfainted[i]: #damaged mon, blit gray punkeball
                ballSprite=pokeball_injured
            else: #fainted mon, blit darkened punkeball
                ballSprite=pokeball_faint
            self.gameScreen.blit(ballSprite,(playerHealthBarPos[0]+i*1.5*pixel,playerHealthBarPos[1]-pixel))
        for i in range(0,len(enemyMonsUnfainted)):
            if enemyMonsUnfainted[i]==2: #unfainted mon, blit regular punkeball
                ballSprite=pokeball_team
            elif enemyMonsUnfainted[i]:
                ballSprite=pokeball_injured
            else: #fainted mon, blit darkened punkeball
                ballSprite=pokeball_faint
            self.gameScreen.blit(ballSprite,(enemyHealthBarPos[0]+i*1.5*pixel,enemyHealthBarPos[1]-pixel))
            
        #status markers
        markerWidth=35
        playerMonStatusColors=[]
        enemyMonStatusColors=[]
        playerMon=self.curBattle.player.curMon
        enemyMon=self.curBattle.enemy.curMon
        for status in statusFlags: #list of potentially displayed status ailments
            if playerMon and playerMon.status[status]:
                playerMonStatusColors.append(statusFlags[status])
            if enemyMon and enemyMon.status[status]:
                enemyMonStatusColors.append(statusFlags[status])
        for i in range(0,len(playerMonStatusColors)):
            flag=playerMonStatusColors[i]
            position=(playerHealthBarPos[0]-markerWidth*(i+1),playerHealthBarPos[1])
            self.gameScreen.blit(flag,position)
        for i in range(0,len(enemyMonStatusColors)):
            flag=enemyMonStatusColors[i]
            position=(enemyHealthBarPos[0]+pixel*healthBarWidth+markerWidth*i,enemyHealthBarPos[1])
            self.gameScreen.blit(flag,position)
            

    def getHealthBar(self,cellsLong,cellsHigh,value):
        #takes a length and height in cells and a floating point (0,1] fraction-of-health-left
        #returns a surface for blitting
        healthBarSurface=pygame.Surface((pixel*cellsLong,pixel*cellsHigh),0,32)
        barLength=(cellsLong-2*cellsHigh)*pixel+2*cellsHigh*pixel*11/15
        posBarLength=ceil(barLength*value) #length in (screen, not game) pixels that is full
        negBarLength=barLength-posBarLength
        if value>=0.5:
            color=(78,171,24)
        elif value>=0.2:
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

    def getTextSurface(self,string):
        textSurface=pygame.Surface((pixel*len(string),pixel),0,32)
        for i in range(0,len(string)):
            charImage=menuSpriteDict[string[i]]
            textSurface.blit(charImage,(pixel*i,0))
        return textSurface

#################Generating individual things
###### Global variables (semi-permanent)
IDnum=0 #increment this when a new punkemon is generated
numMoves=4
pixel=15 #side length of sprite grid unit in pixels
screenWidth=25
screenHeight=21
encourageList=["It's not over!","Get 'em!","I choose you!","You can do it!"]

placeholderSquirtle=Squirtle(8,"Squirtle")
Red=PC("Red","female",[placeholderSquirtle],20) # Squirtle is a placeholder. You needn't start with Squirtle if you don't want to. *coughbutyoushouldcough*



pokeball_team=pygame.image.load(os.path.join("sprites","pokeball_team.png"))
pokeball_injured=pygame.image.load(os.path.join("sprites","pokeball_injured.png"))
pokeball_faint=pygame.image.load(os.path.join("sprites","pokeball_faint.png"))

poisonFlag=pygame.image.load(os.path.join("sprites","flagPsn.png"))
burnedFlag=pygame.image.load(os.path.join("sprites","flagBrn.png"))
frozenFlag=pygame.image.load(os.path.join("sprites","flagFrz.png"))
sleepFlag=pygame.image.load(os.path.join("sprites","flagSlp.png"))
paralyzedFlag=pygame.image.load(os.path.join("sprites","flagPar.png"))
confusedFlag=pygame.image.load(os.path.join("sprites","flagCon.png"))
statusFlags={"poisoned":poisonFlag,"burned":burnedFlag,"frozen":frozenFlag,
                  "sleep":sleepFlag,"paralyzed":paralyzedFlag,"confused":confusedFlag}


rivalName="Should Not Display"

###### Menu instances (self,oplist,mode,execOnA,execOnS,rollable=False,oplistConstructor=False,screen=False) sorted by world or speaker
placeholderMenu=menu(["You should never see this."],"dialog","self.screen.switchTo('world')","self.screen.switchTo('world')")
########### Typha menus
falseChoice=menu(["Boy","Girl"],"choice","Red.gender=self.oplist[self.curPos-1]\nself.replaceMenu(boy)","pass")
nickChoice=menu(["Choose a nickname:","ASSHAT","ASSFACE","BUTTHAT","BUTTFACE","FACEHAT","ASSBUTT",'"GARY"'],"titledChoice","garyActionable.trainer.name=self.oplist[self.curPos-1]\ngaryBefore.oplist[0]=garyActionable.trainer.name+garyBefore.oplist[0]\nself.replaceMenu(menuDict[self.oplist[self.curPos-1]])","pass")
starterMonChoice=menu(["Bulbasaur","Charmander","Squirtle"],"choice","self.pickStarter(self.oplist[self.curPos-1])","pass")
noDice=menu(["Since it seems I can't talk either of you two out of it~","Your adventure in the world of PUNKEMON fighting starts NOW. Grab a mon and get going!"],"dialog","self.replaceMenu(starterMonChoice)","pass")
doItAnyway=menu(["You can't scare me.","I'll be the best!"],"choice","self.replaceMenu(noDice)","pass")
talkOut=menu(["I'll tell you what I told him:\nThe fighting circuit ain't no nursery school.","You've got a better chance of ending up in jail or a body bag than as a PUNKEMON CHAMPION."],"dialog","self.replaceMenu(doItAnyway)","pass")
Intro=menu(["Yo!\nWelcome to the world of Punkemon~","My name is TYPHA.\nPeople in this hood, they call me the PUNKEMON PROFESSA.",
                  "There are creatures called PUNKEMON all up in dis world.","Some people think PUNKEMON are monsters.\nAin't totally wrong~","Some people keep 'em as pets.\nOthers use them in fights.",
                  "Me, I used to do that.\nNow I'm goin' straight.","I'm gonna study PUNKEMON as a profession.\nLab coat and everything.","When you're hiding behind that computer, it's hard to tell who you are.",
                  "Are you a boy, or a girl?"],"dialog","self.replaceMenu(falseChoice)","pass")
boy=menu(["You remember my little bro.\nYou've been at each other's throats ever since you were kids.","What was your charming nickname for him again?"],"dialog","self.replaceMenu(nickChoice)","pass")
girl=boy #code as political statement, or lazy programmer? #bothisgood
#The above line is dead code, but I haven't deleted it because I want to keep the joke.
asshat=menu(['Oh, yeah. "Asshat."Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
assface=menu(['Oh, yeah. "Assface."Ha!  You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
butthat=menu(['Oh, yeah. "Butthat." Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
buttface=menu(['Oh, yeah. "Buttface." Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
facehat=menu(['Oh, yeah. "Facehat." Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
assbutt=menu(['Oh, yeah. "Assbutt." Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")
GaryNickname=menu(['Oh, yeah. "Gary". Ha! You have such a way with words~'],"dialog","self.replaceMenu(talkOut)","pass")

########### Start menu and its descendents
start=menu(["Punkemon","Wikidex","Items","longtest","longtesttitled","Stats","Save"],"choice","self.addToMenuStack(menuDict[self.oplist[self.curPos-1]])","self.screen.switchTo('world')",True)
startPunkemon=menu(False,"choice","pass","self.backUpMenuStack()",True,"list(Red.teamAsString())")
startWikidex=menu(False,"dialog","pass","self.backUpMenuStack()",True,"Red.wikidexAsList()")
startItems=menu(False,"choice","self.selectItemOutsideBattle()","self.backUpMenuStack()",True,"start.displayItemsList()")
itemChooseMon=menu(False,"choice","self.itemOutsideBattle(self.curPos-1)","self.backUpMenuStack()",True,"Red.teamAsString()")
longtest=menu(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29"],"choice","self.backUpMenuStack()","self.backUpMenuStack()")
longtesttitled=menu(["Title","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29"],"titledChoice","self.backUpMenuStack()","self.backUpMenuStack()")
startStats=menu(["Stats not implemented yet"],"dialog","self.backUpMenuStack()","self.backUpMenuStack()")
saveGame=menu(["all is vanity\nand the pursuit\n         of the wind\nyou cannot save yet"],"dialog","self.backUpMenuStack()","self.backUpMenuStack()")

########### Menus from the inescapableHellscape test world
despairSign=menu(["There is no escape from the inescapable hellscape.","Not for you~\n ~not for him."],"dialog","self.screen.switchTo('world')","self.screen.switchTo('world')")
garyBefore=menu([": Hey! How did you get here?"],"dialog","self.screen.processResponse(('battle',Gary))","self.screen.processResponse(('battle',Gary))",False)
garyAfter=menu(["Gary: Aww, man!"],"dialog","self.screen.switchTo('world')","self.screen.switchTo('world')")

menuDict={"Boy": boy,"Girl":girl,"FalseChoice":falseChoice,
          "nickChoice":nickChoice,"ASSHAT":asshat,"ASSFACE":assface,"BUTTHAT":butthat,"BUTTFACE":buttface,"FACEHAT":facehat,"ASSBUTT":assbutt,'"GARY"':GaryNickname,
          "talkOut":talkOut,"doItAnyway":doItAnyway,"noDice":noDice, "You can't scare me.":noDice,"I'm gonna be the best!":noDice,
          "Punkemon":startPunkemon,"Wikidex":startWikidex,"Items":startItems,"longtest":longtest,"longtesttitled":longtesttitled,"Stats":startStats,"Save":saveGame}






###check double type later
######Pokemon instance creation
##Initialize all pokemon with: level, name (optional), trainer (optional)
starterBulbasaur=Bulbasaur(8,"Bulbasaur")
betaBulbasaur=Bulbasaur(20,"Ivysaur")
powerBulbasaur=Bulbasaur(50,"Venusaur")
starterCharmander=Charmander(8,"Charmander")
betaCharmander=Charmander(20,"Charmeleon")
powerCharmander=Charmander(50,"Charizard")
starterSquirtle=Squirtle(8,"Squirtle")
betaSquirtle=Squirtle(20,"Wortortle")
powerSquirtle=Squirtle(50,"Blastoise")
derpy=Derp(30,"derpy")
Rattata6=Rattata(6,"Rattata")
Pidgey6=Pidgey(6,"Pidgey")
hovis=Hovisquirrel(6,"Hovisquirrel")
hypnotoad=Hypnotoad(6,"Hypnotoad")


########## Mon seeds
Rattata5=Rattata(5,"Rattata")
Pidgey5=Pidgey(5,"Pidgey")
basicRouteSeed=monSeed({Pidgey5:1,Rattata5:1},10)
allRattataSeed=monSeed({Rattata:1},10) #fuck pidgeys, I'm trying to debug here
starterSeed=monSeed({starterBulbasaur:1,starterCharmander:1,starterSquirtle:1},20)

########## Worlds
#inescapableHellscape=world(False,testMap,6,9,basicRouteSeed,False)
emptyHellscape=world(False,blankMap,6,9)
doubleHellscape=world(False,doubleMap,6,9,basicRouteSeed,False," w")
inescapableHellscape=world(False,buildingMap,6,9,starterSeed,False," w") #change back to basicRouteSeed later

########## Entrances with INSIDES
O1.destination=inescapableHellscape

######Hard sets of things that should be dynamically generated (Yeah testing!)
Red.inventory["Potion"]=5
Red.inventory["Super potion"]=5
Red.inventory["Repel"]=1
Red.inventory["Revive"]=4
Red.inventory["Punkeball"]=5
Red.inventory["Water stone"]=1
Red.inventory["Fire stone"]=1

Gary=character([starterBulbasaur],"Gary","wait for it",100,garyBefore,garyAfter,"normal")

garyActionable=NPCTrainer([4,0],"red",Gary,"West")
signActionable=NPC("sign",[0,0],despairSign,"sign","none")
inescapableHellscape.actionables.append(garyActionable)
inescapableHellscape.actionables.append(signActionable)


game=screen(screenWidth,screenHeight,inescapableHellscape) #START

#############List of Abominations Unto Nuggan
#Squirtles that think they're Charmanders
#Charmanders that know electric moves
#Everything is named Bulbasaur
#The number of times my computer crashed while I was coding this
#Rattatas attacking themselves
#bool("False")=True
#circular dependencies, because they involve circular dependence
#up and down arrows being interpreted as weird non-ASCII characters
#trying to navigate the battle menus based on the first letter of each of the first two options
#C h a r m a n d e r r a n a w a y !
#Charmander learning Splash...twice.
#eternal rival battle
#Two Garys. That's 100% more Garys than we had yesterday and 100% more Garys than we want. (And none of them is Garys Vakarian.)
#healh bar aspect ratios of 12:1 or 12:5
