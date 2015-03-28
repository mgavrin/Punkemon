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
exec(battlesCode.read())

######### this thing
fakeAPress=pygame.event.Event(KEYDOWN,{"key":K_a})
fakeBPress=pygame.event.Event(KEYDOWN,{"key":K_s})
fakeUpPress=pygame.event.Event(KEYDOWN,{"key":K_UP})
fakeDownPress=pygame.event.Event(KEYDOWN,{"key":K_DOWN})
fakeLeftPress=pygame.event.Event(KEYDOWN,{"key":K_LEFT})
fakeRightPress=pygame.event.Event(KEYDOWN,{"key":K_RIGHT})

###################### Action Items for next work session #############
#bug involving switching mons when you go second: sending-out messages displayed after enemy attacks new mon instead of old.
#revisit menu structures
#pad world map-sections with rocks or trees or purple elephants
#get [walk around in the world-->meet NPC-->start shit-->finish shit-->walk around in the world] running
#pull battles into their own file.
#Maybe also pull the mon class and creation of all the mon species into their own file?
#create poliwag and poliwhirl so hypnotoad isn't just hanging there
#Add EVs
#evolution
#do the sprite stuff for battles (HP bars and whatnot)
#don't put the player sprite on the world slice. You need to put it on the screen *on top of* the world slice.
#world and terrain sprites


############Story notes muthafuckas!
###The first pokemon pusher (local equivalent of pokemart) is named Marty. The others are named increasingly weird spellings of Marty.

###Pokedex and PC system belong to Typha's university; she sneaks you access and
###charges you to store mons above the party five.
###Dex is Typha's thesis project; you and rival are collecting data for her.
###Rival's and your seen-punkemon/caught-punkemon appear in the same dex with a mark for who caught them;
###contest between you and Rival to get the most--for <s>SCIENCE</s> bragging rights!
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
        

    def setNext(self,target): #sets menu to which to return upon pressing B
        self.nextMenu=target

    def getNext(self): #returns nextMenu
        return self.nextMenu

    def processInput(self, event, screen):
        if event.type==KEYDOWN:
            if self.curSlide<len(self.dialog):
                self.curSlide+=1
            else:
                oldMenu=self
                newMenu=oldMenu.getNext()
                screen.curMenu=newMenu
                if newMenu.nextMenuMeta=="previous":
                    newMenu.setNext(oldMenu)
                self.curSlide=1


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
        for i in range(0,len(finalLines)):
            finalLines[i]=finalLines[i].ljust(self.maxChars)
            
        ##Characterize and print the array       
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


class battleMenu:
    def __init__(self,curMode,oplist):
        self.curMode=curMode #either "choice" or "dialog"
        self.oplist=oplist #list of messages if dialog, list of choices if choice
        self.length=len(self.oplist)
        self.curPos=1 #choice # or place in the messages list
        self.drawArray=[] #list of sprite
        self.maxChars=20
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
            array=self.getArrayChoice()
        elif self.curMode=="dialog":
            array=self.getArrayDialog()
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
        opAr=[["*"]]
        for i in range(0,maxLength+1): #+1 for cursor
            opAr[0].append("=")
        opAr[0].append("*")
        #assemble menu line for a given entry
        for op in self.oplist:
            opString=str(op)
            tmp=["|"," "] #open line with pipe and space for cursor
            tmpStr=opString.ljust(maxLength)#buffer item to max length, +1 for cursor
            for char in tmpStr:#stick in one char at a time
                tmp.append(char)
            tmp.append("|")#close line with pipe
            opAr.append(tmp)
        opAr.append(opAr[0]) #bottom border is same as top
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
            
            
        

        
########### Punkemon, because there need to be some mons in this mon-battling game ############

class punkemon:
    def __init__(self,species,nation,specNum,level,learnSpeed,baseStats,baseXPworth,learnDict,nickname=False,trainer=False):
        #statVariables should be a list with base stats for the species plus anything else necessary to calculate attk, def, etc.
        self.species=species
        self.specNum=specNum
        if nickname:
            self.name=nickname
        else:
            self.name=species
        self.nation=nation
        global IDnum
        self.ID=IDnum
        IDnum+=1
        self.level=level
        self.learnSpeed=learnSpeed #rate of leveling with respect to XP
        self.XP=self.getXP()
        self.baseStats=baseStats
        self.baseXPworth=baseXPworth
        self.IVs=self.getIVs()
        self.EVs=[0,0,0,0,0] #accumulates with battles
        self.permStats=self.getPermStats()#stats right after healing
        self.tempStats=dict(self.permStats)#stats after effects of damage and stat-altering moves
        self.accuracy=100 #reset this at the start of every battle
        self.evasion=100 #reset this at the start of every battle
        self.critRate=self.permStats["Speed"]/512.0
        self.status={"poisoned":False,"burned":False,"frozen":False,"sleep":False,"paralyzed":False,"flinched":False,
                     "confused":False,"trapped":False,"multiple":False,"seeded":False,"charging":False,"justSentOut":False} #poison/burn/freeze/sleep/paralysis/flinch/confused
        self.canMove=True
        self.learnDict=learnDict #learnable moves
        self.curMoves=self.getMoves(level)
        self.curMove=self.curMoves[0]
        #THIS IS A TERRIBLE HACK
        #hopefully this never ends up running this specific move.
        #It's just so battle doesn't freak out before they first-turn flinch.
        self.curPP=self.getPP()
        self.whenToStop=False #total number of turns on the current multiple move
        self.trainer=trainer
        self.monsFought=[] #punkemon fought in the current battle, to be awarded XP if self faints
        self.moveToLearn=False

    def __repr__(self):
        return self.name #hahahaha!

    def __str__(self):
        return self.name

    def getIVs(self):#generates stats for 0-15 biased towards mean)
        IVs=[];
        for i in range(0,5):
            IVs.append(randint(0,7)+randint(0,8))
            #d8 plus d9, zero-index
        return IVs

        
    #method for calculating attack, defense, etc.
    def getPermStats(self): #returns [Attack, Defense, HP, Speed, Special]
        permStats={}
        #WARNING: never divide ints, it auto-floors! Always float() at least one argument
        permStats["Attack"]=floor(((self.IVs[0]+self.baseStats[0]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        permStats["Defense"]=floor(((self.IVs[1]+self.baseStats[1]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        permStats["HP"]=floor(((self.IVs[2]+self.baseStats[2]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+10)
        permStats["Speed"]=floor(((self.IVs[3]+self.baseStats[3]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        permStats["Special"]=floor(((self.IVs[4]+self.baseStats[4]+float(self.EVs[0]**.5)/float(8)+50)*self.level)/50+5)
        return permStats

    def getXP(self,level=False): #returns the minimum number of XP necessary to be at the specified level
        if not level:
            level=self.level
        if self.learnSpeed=="slow":
            return 5*level**3/4
        elif self.learnSpeed=="medium":
            return level**3
        elif self.learnSpeed=="fast":
            return 4*level**3/5

    def getPP(self):
        curPP=[]
        for m in self.curMoves:
            curPP.append(m.maxPP)
        return curPP

    def getMoves(self,level):
        moveLevels=self.learnDict.keys() #levels at which a mon learns new moves
        curLevel=0
        moveSet=[]
        while curLevel<=level:
            if curLevel in moveLevels:
                moveSet.append(self.learnDict[curLevel])
            curLevel+=1
        return moveSet[-4:]

    def getCanMove(self): #poison/burn/freeze/sleep/paralysis/flinch/confused
        canMove=True
        messages=[]
        if self.status["flinched"]  or self.status["sleep"] or self.status["frozen"] or self.status["justSentOut"]:
            if self.status["flinched"]:
                self.status["flinched"]=False #flinching only lasts one turn
                messages.append(self.name + " flinched!")
            elif self.status["justSentOut"]:
                encouragement=encourageList[randint(0,len(encourageList)-1)]
                if isinstance(self.trainer,PC):
                    messages.append("Go "+self.name+"!")
                    messages.append(encouragement)
                else:
                    messages.append(self.trainer.name+": Go "+self.name+"!")
                    messages.append(self.trainer.name+": "+encouragement)
            elif self.status["sleep"]:
                messages.append(self.name+" is asleep.")
            elif self.status["frozen"]:
                messages.append(self.name+" is frozen.")
            self.status["multiple"]=False#c-c-c-combo breaker!
            canMove=False
        elif self.status["paralyzed"]:
            if randint(1,4)==4:
                self.status["multiple"]=False#c-c-c-combo breaker!
                messages.append(self.name + " is fully paralyzed!")
                canMove=False       
        elif self.status["trapped"]:
            self.status["trapped"]=False
            self.status["charging"]=False
            self.status["multiple"]=False#c-c-c-combo breaker!
            messages.append(self.name + " is trapped and cannot move!")
            canMove=False
        
        elif self.curMove.sideEffect:
            #if there is an effect
            effectWords=self.curMove.sideEffect.split()
            #break effect down into words
            moveType=effectWords[0]#we only care if this becomes charging or multiple
            if moveType=="charging":
                if effectWords[1]=="offscreen":
                    duration=2 #fly and dig charge for one turn, then activate
                else:
                    duration=int(effectWords[1])
            if moveType=="multiple":
                enemyCanMove=not(effectWords[1]=="False" or effectWords[1]=="false")
            if moveType=="charging" and not self.status["charging"]:
                #need to start charging, should only happend on first turn of charging move
                self.status["charging"]=1
            if moveType=="multiple" and not self.status["multiple"]:
                #need to start a multiple move, should only happend on first turn of multiple move
                self.status["multiple"]=1
                self.whenToStop=randint(2,5)
                #for the moment, all multiple moves have random duration
                #this duration will be 2-5 turns
                
            #continuing charging/multiple attacks
            if moveType=="charging":
                if self.status["charging"]==duration:
                    self.status["charging"]=False
                    canMove=True #charging is done, reset and move
                else:
                    self.status["charging"]+=1
                    messages.append(self.name+" is about to use "+str(self.curMove)+"!")
                    canMove=False #still charging, don't move
            if moveType=="multiple":
                if self.status["multiple"]==self.whenToStop:
                    self.status["multiple"]=False #multiple move is over, back to normal
                    
                canMove=True #unlike charging moves, multiple moves go every turn for their duration
                    
            
        return (canMove,messages)

    def getStatusDamage(self,enemy):
        messages=[]
        if self.status["burned"] or self.status["poisoned"]:
            if self.status["burned"]:
                hurtingStatus="burn"
            else:
                hurtingStatus="poison"
            tempHP=self.tempStats["HP"]
            permHP=self.permStats["HP"]
            damage=floor(float(permHP)/16)
            messages.append(self.name+" took "+str(damage)+" damage from "+str(hurtingStatus)+"!")
            self.tempStats["HP"]-=damage
        if self.status["seeded"]:
            damage=floor(float(self.permStats["HP"])/16)
            self.tempStats["HP"]-=damage
            enemy.tempStats["HP"]+=damage
            if enemy.tempStats["HP"]>enemy.permStats["HP"]:
                enemy.tempStats["HP"]=enemy.permStats["HP"]
            messages.append(str(enemy)+" sapped "+str(damage)+" health with Leech Seed!")
        if self.status["trapped"]:
            pass
        return messages

    def getEffectSuccess(self, effectWord):
        if (effectWord=="burned" or effectWord=="poisoned") and (self.status["burned"] or self.status["poisoned"]):
            return False
        if (effectWord=="frozen" or effectWord=="sleep" or effectWord=="paralyzed") and (self.status["frozen"] or self.status["sleep"] or self.status["paralyzed"]):
            return False
        return True

    def heal(self):
        self.curPP=self.getPP()
        self.tempStats=dict(self.permStats)
        for key in self.status.keys():
            self.status[key]=False

    def getLevelFromXP(self):
        for level in range(self.level,102):
            XPforLevel=self.getXP(level)
            if XPforLevel>self.XP:#if you don't have enough XP for level n, return n-1
                return level-1
    
    def awardXP(self,enemyTeam,communism=False):#self: the mon that just fainted; enemyTeam: the set of mons that may have had a hand in that
        #awards XP to every mon in monsFought based on wildness, base worth, level, and number of mons sharing XP
        #Communism shares half the XP pool among the unfainted mons that fought and the other half among the unfainted mons that didn't,
        #whereas capitalism shares the whole pool among the unfainted mons that fought.
        messages=[]
        newMoveInfo=(False,False)
        if self.trainer: #trainer pokemon bonus factor
            isWild=1.5
        else:
            isWild=1
        XPPool=isWild*self.baseXPworth*self.level/7.0
        monsSharing=[]
        for mon in self.monsFought: #all the mons the fainted mon faced
            if mon.tempStats["HP"]>0: #mon is not fainted, gets a share of XP
                monsSharing.append(mon)
        if not communism:
            oneMonXP=XPPool/len(monsSharing) #number of XP awarded to each individual mon involved
        else:
            oneMonXP=.5*XPPool/len(monsSharing)
        for mon in monsSharing:
            mon.XP+=oneMonXP
            messages.append(mon.name+" gained "+str(int(oneMonXP))+" XP!")
        if communism:
            print "GLORY TO ARSTOTSKA"
            moocherMons=[]
            for mon in enemyTeam:
                if mon.tempStats["HP"]>0 and mon not in monsSharing:
                    moocherMons.append(mon)
            for mon in moocherMons:
                mon.XP+=oneMonXP
                messages.append(mon.name+" gained "+str(int(oneMonXP))+" XP!")
        for mon in enemyTeam:
            correctLevel=mon.getLevelFromXP()
            if correctLevel!=mon.level:
                levelResults=mon.levelUp(correctLevel-mon.level)
                levelingMessages=levelResults[0]
                newMoveInfo=levelResults[1]
                messages+=levelingMessages
        return [messages,newMoveInfo] #list of messages and a tuple of (move instance,mon instance)
                    

    def levelUp(self,number=1):
        levelingMessages=[]
        moveOnDeck=False
        oldLevel=self.level
        self.level+=number
        self.stats=self.getPermStats()
        levelingMessages.append(self.name+" grew to level "+str(self.level)+"!")
        if isinstance(self.trainer,PC):
            for level in self.learnDict.keys():
                if level>oldLevel and level<=self.level:
                    newMove=self.learnDict[level]
                    if len(self.curMoves)<4:
                        self.curMoves.append(newMove)
                        levelingMessages.append(self.name+" learned "+newMove.name+"!")
                    else:
                        levelingMessages.append(self.name+" can now learn "+newMove.name+".")
                        levelingMessages.append("But "+self.name+" can only know 4 moves.")
                        moveOnDeck=newMove
        else:
            self.getMoves(self.level) #other trainers' mons just take the four highest-level moves available
        #FIX the thing where it tries to teach a move every time a mon levels. Fix it in the function that sets interrupt.
        return [levelingMessages,(moveOnDeck,self)]
                
        #######ADD SHIT HERE. Shit like changing the available moves, asking a player if they want to change the available moves, etc.


#################### Puttin' on the MOVES ###################

class move:
    def __init__(self,name,basePwr, baseAcc, maxPP, nation, sideEffect, message=False, fastMove=False, critRate=1):#sideEffect can be string or False
            self.name=name
            self.basePwr=basePwr
            self.baseAcc=baseAcc
            self.maxPP=maxPP
            self.nation=nation
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
        if (defender.curMove.sideEffect and "offscreen" in defender.curMove.sideEffect):
            if defender.status["charging"]:
                hit=False,[] #auto-miss on dig and fly
        if attacker.status["confused"] and randint(0,1)==0:
            messages.append(attacker,"hurt itself in its confusion!")
            attacker.tempStats["HP"]-=hitYourself.getDamage(attacker,defender)
            hit=False
        
            
        
        else:
            if attacker.status["confused"]:
                messages.append(attacker+" attacked despite confusion!")
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
        typeMod=1
        typeMod*=typeDict[self.nation,defender.nation[0]]
        if len(defender.nation)>1:
            typeMod*=typeDict[self.nation,defender.nation[1]]
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
        
    def getDamage(self,attacker,defender):
        modifier=self.getModifier(attacker, defender)
        attackerAttack=attacker.tempStats["Attack"]
        defenderDefense=defender.tempStats["Defense"]
        damage=float(2*attacker.level+10)/250*attackerAttack/defenderDefense*self.basePwr*modifier
        return ceil(damage)

    def getEffect(self,attacker,defender):
        #The logic behind this is complicated.
        #Some moves' effects are 3-word phrases of the form "[pokemon][accuracy/evasion][degree of change]".
        #Others are 3-word phrases of the form "[pokemon][stat][degree of change].
        #Still others are 2-word phrases of the form "[percent chance][possible status effect]",
        #And a final group are 2-word phrases of the form "[charging or multiple][number of turns or whether enemy is trapped]".
        #These possibilities are handled in the above order, with the exception of charging and multiple,
        #which must be handled before the damage is calculated and, therefore, before getEffect.

        messages=[]
        if self.sideEffect:
            #if there is an effect
            effectWords=self.sideEffect.split()
            #break effect down into words

            #handle accuracy/evasion effects
            if effectWords[1]=="accuracy" or effectWords[1]=="evasion":
                if effectWords[0]=="self":
                    call="attacker"
                    messages.append(attacker.name+self.message)
                else:
                    call="defender"
                    messages.append(defender.name+self.message)
                call+="."+effectWords[1]
                call+="*=1.4**"+effectWords[2]
                exec(call)
            #handle all other stat effects
            elif len(effectWords)==3:
                #if effect is a stat move
                if effectWords[0]=="self":
                    attacker.tempStats[effectWords[1]]*=1.4**int(effectWords[2])
                    messages.append(attacker.name+self.message)
                elif effectWords[0]=="enemy":
                    defender.tempStats[effectWords[1]]*=1.4**int(effectWords[2])
                    messages.append(defender.name+self.message)
            
            #handle 2-word status effects
            elif effectWords[0]!="charging" and effectWords[0]!="multiple": #e.g. sleep, burn, etc.
                fail=False
                if self.basePwr==0 and not defender.getEffectSuccess(effectWords[1]):
                    fail=True
                if randint(0,99)<int(effectWords[0]) and not fail:
                    defender.status[effectWords[1]]=True
                    messages.append(defender.name+self.message)
                    #messages.append(str(defender)+" became "+effectWords[1]+"!")
                if fail:
                    messages.append("But it failed!")
                


            #handle multiple
            elif effectWords[0]=="multiple" and attacker.status["multiple"]: #multiple move
                 enemyCanMove=not(effectWords[1]=="False" or effectWords[1]=="false")
                 if not enemyCanMove: #enemy cannot move
                     defender.status["trapped"]=True
        return messages

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

############ People (player and NPCs)
class character:
    def __init__(self,team,name,sprite,money,AI="normal",rewardItem=False):
        self.team=team
        self.name=name
        self.sprite=sprite
        #put some sprite code here when you have sprites
        self.money=money #money you get for beating them, or your money if it's you
        self.AI=AI #whether character is player, npc, bad-AI npc or good-AI npc
        self.curMon=team[0] #mon that goes out when battle starts

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
        #messages.append(self.name+" was defeated!") #RE-EXAMINE
        #put some end-of-battle stuff here
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

        

##############Sprites! ###########################
terrainDict={"T":1,"x":1,"-":0,"G":3,"w":4,"O":2," ":0,"B1":1}
    
class sprite:
    def __init__(self,longName,screenName,fileLocation,screen,pos,terrain=False,destination=False):
        self.longName=longName #(e.g. "tree", "mart", "rock")
        self.screenName=screenName#(e.g. T, X, @)
        self.fileLoc=fileLocation #file name and any necessary path
        self.screen=screen
        self.pos=pos #A two-element list with the coordinates of the top left corner (from top left of screen, +y is down)
        self.drawMap=self.screen.drawMap
        self.drawMap[pos[0]][pos[1]]=self.screenName #put the square in the draw map
        self.terrain=terrain
        #0=passable, 1=impassable, 2=screen change, 3=encounter, 4=water
        self.destination=destination
        #if not False, this will be a 2-element list with new world instance and initial player coordinates upon entering that world
        self.terrainMap=self.screen.terrainMap
        self.terrainMap[pos[0]][pos[1]]=self.terrain #put the square in the terrain map



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

    def addToMap(self,terrainMap, spriteMap,xpos,ypos):
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
                    spriteMap[curY][curX]=char      
                else:
                    # just set terrain to the appropriate type:
                    terrainMap[curY][curX]=char 
                curX+=1 #increment the x position as we move across the row                    
            curY+=1   #increment row at end of each row...
            curX=xpos #...and reset the x to the position of the lefthand side of the building
        #Once done with that, add ourself to the appropriate spot in the spriteMap:
        spriteMap[ypos][xpos]=self
        #Now done with the map, end this function...


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

##    def __str__(self):
##        return self.sprite

    
        
class world:
    def __init__(self,screen,inputMap,dimx,dimy):
        #inputMap will be a nested list of screenNames indicating the pattern of sprites. Example:
##        [
##        ["x","x","x","x","x","x"],
##        ["x","G","G","G","G","x"],
##        ["x"," "," "," "," ","x"],        
##        ["x"," "," "," "," ","x"],
##        ["x","T","T","-","-","x"],
##        ["x","B1"," "," "," ","x"],             
##        ["x"," "," "," "," ","x"],
##        ["x"," "," "," "," ","x"],            
##        ["x","x","x","x","x","x"]
##                                ]
        
        self.screen=screen
        self.drawMap=inputMap
        self.dimx=dimx
        self.dimy=dimy
        self.buildingDict={}
        #maps building names to coordinates
        self.terrainMap=self.getTerrainMap(inputMap,dimx,dimy)
        self.spriteMap=self.getSpriteMap(inputMap)
        #getSpriteMap will overwrite portions of terrainMap, and therefore needs to be called second
        self.drawMap=self.getDrawMap(inputMap)

    def getSpriteMap(self,inputMap): #also puts buildings in terrainMap
        #Create a set of nested lists of the right size...
        spriteMap=[]
        for i in range(0,self.dimy):
            row=[]
            for j in range(0,self.dimx):
                row.append("?")
            spriteMap.append(row)

        #Now fill them out based on inputMap...
        ypos=0
        for row in inputMap:
            xpos=0
            for char in row:
                if isinstance(char,building): #check if building
                    self.buildingDict[char]=[xpos,ypos]
                elif isinstance(char,screenChanger):
                    spriteMap[ypos][xpos]=char
                else:
                    spriteMap[ypos][xpos]=char
                xpos+=1 #increment the x position after each char
            ypos+=1 #increment the y position after each row
        for item in self.buildingDict.keys(): #do buildings last so nothing gets pasted over them
            buildingPos=self.buildingDict[item] 
            item.addToMap(self.terrainMap,spriteMap,buildingPos[0],buildingPos[1])
        return spriteMap
            

    def getTerrainMap(self,inputMap,dimx,dimy):
        terrainMap=[]
        xpos=1
        ypos=1
        for row in inputMap:
            terrainMap.append([])
            for char in row:
                try:
                    nextSpriteType=terrainDict[char] #get the class to instantiate
                except:
                    if isinstance(char,screenChanger):
                        nextSpriteType=2
                    elif isinstance(char,building):
                        nextSpriteType=1
                    else:
                        print "what the fuck you doin."
                        print char,"is not what you wanted."
                    terrainMap[-1].append(nextSpriteType)   
                else:
                    terrainMap[-1].append(nextSpriteType)                     
                xpos+=1
            if len(terrainMap[-1])!=dimx:
                print "You bolloxed up the input map. Stop sucking so hard."
            xpos=0
            ypos+=1
        if len(terrainMap)!=dimy:
            print "You bolloxed up the input map. Stop sucking so hard."
        return terrainMap

    def getDrawMap(self,inputMap):
        drawMap=[]
        for row in inputMap:
            newRow=[]
            for char in row:
                if isinstance(char,screenChanger):
                    newChar=char.sprite
                elif isinstance(char,building):
                    newChar=char.shortName
                else:
                    newChar=char
                newRow.append(newChar)
            drawMap.append(newRow)
        return drawMap
            

 ################ init central for worlds, buildings, entrances, and associate maps           
#general policy: initialize all portals with false,
#then the buildings on the maps,
#then the maps themselves,
#then create the worlds containing the buildings,
#then init the portals again with their destinations set.
#Otherwise you get circular dependencies.


########## Entrances with FALSE
O1=screenChanger("O1","filler",False,[1,1])

########## Buildings
B1=testBuilding(O1)

########## Maps    
testMap=[
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

########## Worlds
inescapableHellscape=world(False,testMap,6,9)

########## Entrances with INSIDES
O1.destination=inescapableHellscape

    

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
        self.background=pygame.image.load("jedipunzel.jpg")
        self.screenSize=(pixel*xDim,pixel*yDim)
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(255,255,255)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.curMenu=Intro
        self.mode="battle"
        self.switchTo(self.mode)
        self.curWorld=curWorld
        self.playerPos=[1,1] #Initial position of the player. Fix this later, it will drop you in a rock
        #self.worldSlice=self.getWorldSlice() #PUT THIS BACK later, when you have a world larger than your screen
        #a nested list, the subsection of the drawMap of the curWorld that is visible on the screen
        self.playerIsSurfing=False
        self.changeWorld=False
        self.curBattle=battle(Red,Gary,self)
        

        #The following needs to be the last line in __init__!
        self.mainloop()
        
    
    def switchTo(self,mode):
        self.mode=mode
        if mode=="menu":
            self.processInput=self.menuInput
            self.drawScreen=self.drawMenu
        elif mode=="world":
            self.processInput=self.worldInput
            self.drawScreen=False
        elif mode=="battle":
            self.processInput=self.battleInput
            self.drawScreen=self.drawBattle
        else:
            print "I don't know how to switch to "+mode+". You and your expectations."
    
    def mainloop(self):
        while True:
            if self.mode=="menu":
                #find out what the user has done
                event=self.getInput()
                #deal with it, updating gamestate accordingly
                self.processInput(event)#this will be a different function depending on what's going on
                #update broader game state
                self.update() 
                #draw
                self.drawScreen()#this will be a different function depending on what's going on
                self.clock.tick(self.fps)
                                         
            elif self.mode=="battle":
                event=self.getInput() #if in battle mode, then self.getInput=self.getBattleInput
                self.processInput(event) 
                self.drawScreen() ##WRITE THIS FUNCTION
                
                
            elif self.mode=="world":
                event=self.getInput()
                self.processInput(event)
                self.worldUpdate()
                if event:
                    print "----",self.playerPos,"-------"
                    for i in self.worldSlice:
                        print i
                    
                    
    

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
        if event is fakeAPress:
            print "Processing a FAKE KEY!? That's unethical!"
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        else:
            self.curMenu.processInput(event, self)
    
    def battleInput(self,event):
        if not event:
            return
        else:
            self.curBattle.curAction(event)

    def worldInput(self,event):
        #You should probably move all the world functions to their own class like with Battle
        if not event:
            return #if the player has done nothing worth noting, do nothing.
        elif event.key==K_a or event.key==K_s:
            return
        else: #move the player around
            if event.key==K_UP:
                tempPos=[self.playerPos[0],self.playerPos[1]-1]
            elif event.key==K_DOWN:
                tempPos=[self.playerPos[0],self.playerPos[1]+1]
            elif event.key==K_LEFT:
                tempPos=[self.playerPos[0]-1,self.playerPos[1]]
            elif event.key==K_RIGHT:
                tempPos=[self.playerPos[0]+1,self.playerPos[1]]
            self.playerPos=self.checkMove(tempPos) #checkMove should return tempPos if the attempted square is passable, playerPos otherwise

    def checkMove(self,tempPos):
        #Returns the new position after an attempted move
        #If player can move into attempted square, returns new position
        #if player cannot move into attempted square, returns old position
        #if player stepped on a screenChanger, return False to signal to worldUpdate() that it needs to handle a world change
        tryX=tempPos[0]
        tryY=tempPos[1]
        self.changeWorld=False
        newTerrain=self.curWorld.terrainMap[tryY][tryX] #gets terrain type of square you're trying to move to
        #demons happen
        if newTerrain==0:
            return tempPos #can always walk on walkable terrain
        elif newTerrain==1:
            return self.playerPos #can never walk on impassable terrain
        elif newTerrain==2:
            self.changeWorld=True
            return tempPos
        elif newTerrain==3:
            #set encountersOn to True
            return tempPos #can move into square, encounters are possible
        elif newTerrain==4: #new terrain is water
            if self.playerIsSurfing:
                return tempPos #if surfing, they can step into water
            else:
                return self.playerPos #cannot into water and covered in fleas
        
            
        
    def getWorldSlice(self): #self.curWorld,self.xDim,self.yDim,self.playerPos
        fullDrawMap=self.curWorld.drawMap
        topRow=self.playerPos[1]-(self.yDim-1)/2 #y coordinate of top row
        bottomRow=topRow+self.yDim #y coordinate of bottom row
        leftCol=self.playerPos[0]-(self.xDim-1)/2 #x coordinate of left column
        rightCol=leftCol+self.xDim #y coordinate of bottom row
        #now make the new map
        fatSlice=fullDrawMap[topRow:bottomRow]
        #now you have a map of the right height but too wide
        worldSlice=[]
        for row in fatSlice:
            shortRow=row[leftCol:rightCol]
            worldSlice.append(shortRow)
        centerx=(self.xDim-1)/2
        centery=(self.yDim-1)/2
        worldSlice[centery][centerx]="@"
        return worldSlice

    def worldUpdate(self):
        if self.changeWorld:
        #this means we need to change the curWorld
            warpSquare=self.curWorld.spriteMap[self.playerPos[1]][self.playerPos[0]] #warpSquare is the screenChanger instance you stepped on
            self.playerPos=warpSquare.startPos
            self.curWorld=warpSquare.destination
            self.changeWorld=False
        self.worldSlice=self.getWorldSlice()
            
        

    def update(self):
        pass

    def drawASCII(self):
        pass
    def drawMenu(self):
        self.gameScreen.fill(self.backgroundColor)
        drawPos=[0,0]
        drawArray=self.curMenu.getArray()
        for row in drawArray:
            drawPos[0]=0
            for cell in row:
                self.gameScreen.blit(menuSpriteDict[cell],dest=[drawPos[0]*pixel, drawPos[1]*pixel])
                drawPos[0]+=1
            drawPos[1]+=1
        pygame.display.flip()

    def drawBattle(self):
        self.gameScreen.fill(self.backgroundColor)
        drawPos=[0,0]
        drawArray=self.curBattle.getArray()
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
pixel=15 #side length of sprite grid unit in pixels
encourageList=["It's not over!","Get 'em!","I choose you!","You can do it!"]        
  

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
Intro=dialogMenu(["Yo!\nWelcome to the world of Punkemon~","My name is TYPHA.\nPeople in this hood, they call me the PUNKEMON PROFESSA.",
                  "There are creatures called PUNKEMON all up in dis world.","Some people think PUNKEMON are monsters.\nAin't totally wrong~","Some people keep 'em as pets.\nOthers use them in fights.",
                  "Me, I used to do that.\nNow I'm goin' straight.","I'm gonna study PUNKEMON as a profession.\nLab coat and everything.","When you're hiding behind that computer, it's hard to tell who you are.",
                  "Are you a boy, or a girl?"],"menu",falseChoice)
boy=dialogMenu(["You remember my little bro.\nYou've been at each other's throats ever since you were kids.","What was your charming nickname for him again?"],"menu",nickChoice)
girl=dialogMenu(["You remember my little bro.\nYou've been at each other's throats ever since you were kids.","What was your charming nickname for him again?"],"menu",nickChoice)
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
##Initialize moves with: name,basePwr, baseAcc, maxPP, nation, sideEffect, fastMove=False, critRate=1
##Basic moves
tackle=move("Tackle",35,95,35,"Normal",False)
growl=move("Growl",0,100,40,"Normal","enemy Attack -1","'s attack fell!")
tailWhip=move("Tail Whip",0,100,40,"Normal","enemy Defense -1","'s defense fell!")
scratch=move("Scratch",40,100,35,"Normal",False)

##Bulbasaur
leechSeed=move("Leech Seed",0,90,10,"Grass","100 seeded", " was seeded!")
vineWhip=move("Vine Whip",35,100,10,"Grass",False)
poisonPowder=move("Poisonpowder",0,75,35,"Poison","100 poisoned"," was poisoned!")
razorLeaf=move("Razor Leaf",55,95,25,"Grass",False)
growth=move("Growth",0,100,40,"Normal","self Special 1","'s special rose!")
sleepPowder=move("Sleep Powder",0,75,15,"Grass","100 sleep"," fell asleep!")
solarBeam=move("Solar Beam",120,100,10,"Grass","charging 2")#####needs to charge! #contemplate and/or add a special message here

##Charmander
ember=move("Ember",40,100,25,"Fire","10 burn"," was burned!")
leer=move("Leer",0,100,30,"Normal","enemy Defense -1","'s defense fell!")
####Add rage?
slash=move("Slash",70,100,20,"Normal",False,False,8)#high crit rate
flamethrower=move("Flamethrower",95,100,15,"Fire","10 burned"," was burned!")
fireSpin=move("Fire Spin",15,70,15,"Fire","multiple False"," is caught in the vortex!")#special message here won't display because you haven't handled charging and multiple

##Squirtle
bubble=move("Bubble",20,100,30,"Water",False)
waterGun=move("Water Gun",40,100,25,"Water",False)
bite=move("Bite",60,100,25,"Normal","10 flinch"," flinched!")
withdraw=move("Withdraw",0,100,40,"Water","self Defense 1","'s defense rose!")
skullBash=move("Skull Bash",100,100,15,"Normal","charging 2")#contemplate/add special message
hydroPump=move("Hydro Pump",120,80,5,"Water",False)

#rattata
quickAttack=move("Quick Attack",40,100,30,"Normal",False,True)
hyperFang=move("Hyper Fang",80,90,15,"Normal","90 flinched"," flinched!")

#pidgey
gust=move("Gust",40,100,35,"Normal",False)
wingAttack=move("Wing Attack",35,100,35,"Flying",False)
fly=move("Fly",90,95,15,"Flying","charging offscreen")#contemplate/add special message

#hovisquirrel aka vulpix
roar=move("Roar",0,100,20,"Normal",False)##currently does jack shit, make analogous to whirlwind
confuseRay=move("Confuse Ray",0,100,10,"Ghost","100 confused"," became confused!")

#hypnotoad aka poliwrath
hypnosis=move("Hypnosis",0,60,20,"Psychic","100 sleep"," fell asleep!")
doubleSlap=move("Double slap",15,85,10,"Normal","multiple False")
bodySlam=move("Body slam",85,100,15,"Normal","30 paralyzed"," became paralyzed!")

#random fun stuff and moves that test important features
thundershock=move("Thundershock",100,90,15,"Electric","30 paralyzed"," became paralyzed!")
sandAttack=move("Sand Attack",0,90,20,"Normal","enemy accuracy -1","'s accuracy fell!")##mul by 1.4^-1
splash=move("Splash",0,100,20,"Water",False)
engineering=move("Engineering",200,100,100,"Dragon","100 confused"," became confused!",True,10)
hitYourself=move("hitYourself",40,200,100,"Fail",False,False,0)
struggle=move("Struggle",50,100,"Normal",False,False,1)
wrap=move("Wrap",15,90,20,"Normal","multiple False")
dig=move("Dig",80,100,10,"Ground","charging offscreen")#contemplate/add special message



###Mon species creation
##Initialize all species with:
##species,nation,specNum,level,learnSpeed,baseStats,baseXPworth,allMoves=[]
    
class bulbasaur(punkemon):
    def __init__(self,level,name="bulbasaur",trainer=False):
        learnDict={0:tackle,1:growl,7:leechSeed,13:vineWhip,20:poisonPowder,27:razorLeaf,34:growth,41:sleepPowder,48:solarBeam}
        punkemon.__init__(self,"Bulbasaur",["Grass"],1,level,"medium",[49,49,45,45,65],64,learnDict,name,trainer)
        
class charmander(punkemon):
    def __init__(self,level,name="charmander",trainer=False):
        learnDict={0:scratch,1:growl,9:ember,15:leer,30:slash,38:flamethrower,46:fireSpin}###Add rage at 22 once you have it coded!
        punkemon.__init__(self,"Charmander",["Fire"],4,level,"medium",[52,43,39,65,50],62,learnDict,name,trainer)
        
class squirtle(punkemon):
    def __init__(self,level,name="squirtle",trainer=False):
        learnDict={0:tackle,1:tailWhip,8:bubble,15:waterGun,22:bite,28:withdraw,35:skullBash,42:hydroPump}
        punkemon.__init__(self,"Squirtle",["Water"],7,level,"medium",[48,65,44,43,50],63,learnDict,name,trainer)
     
class rattata(punkemon):
    def __init__(self,level,name="rattata",trainer=False):
        learnDict={0:tackle,1:tailWhip,7:quickAttack,14:hyperFang}
        punkemon.__init__(self,"Rattata",["Normal"],19,level,"medium",[56,35,30,72,25],51,learnDict,name,trainer)

class pidgey(punkemon):
    def __init__(self,level,name="pidgey",trainer=False):
        learnDict={0:gust,5:sandAttack,12:quickAttack,28:wingAttack}#19 whirlwind but that's dumb
        punkemon.__init__(self,"Pidgey",["Flying"],16,level,"medium",[45,40,40,56,35],50,learnDict,name,trainer)

class derp(punkemon):
    def __init__(self,level,name="derp",trainer=False):
        learnDict={0:tackle,1:growl,13:vineWhip,20:poisonPowder,27:razorLeaf,34:growth,41:sleepPowder,48:solarBeam}
        punkemon.__init__(self,"Derp",["Fail"],0,2,"slow",[0,0,0,0,0],64,{0:splash},name,trainer)

class Rob(punkemon):
    def __init__(self,level,name="Rob Davidoff",trainer=False):
        learnDict={0:tackle,1:Engineering,13:vineWhip,20:poisonPowder,27:razorLeaf,34:growth,41:sleepPowder,48:solarBeam}
        punkemon.__init__(self,"Rob",["Dragon"],200,level,"fast",[70,70,70,70,70],99,learnDict,name,trainer)

class lizardSpock(punkemon):
    def __init__(self,level,name="lizardSpock",trainer=False):
        learnDict={0:tackle,1:wrap,2:slash}#rock, paper, scissors aka tackle, wrap, slash
        punkemon.__init__(self,"Lizard Spock",["Water"],152,level,"fast",[49,49,45,45,65],64,learnDict,name,trainer)

class hovisquirrel(punkemon): #our analogue of vulpix; a squirrel with a flaming tail, for Rob's coworker Greg Hovis
    def __init__(self,level,name="hovisquirrel",trainer=False):
        learnDict={0:tailWhip,1:ember,16:quickAttack,21:roar,28:confuseRay,35:flamethrower,42:fireSpin}
        punkemon.__init__(self,"Hovisquirrel",["Fire"],37,level,"medium",[41,40,38,65,65],60,learnDict,name,trainer)

class hypnotoad(punkemon): #our analogue of polywrath
    def __init__(self,level,name="hypnotoad",trainer=False):
        learnDict={0:hypnosis,1:waterGun,2:doubleSlap,3:bodySlam}
        punkemon.__init__(self,"Hypnotoad",["Water","Fighting"],62,level,"medium",[85,95,90,70,70],255,learnDict,name,trainer)
        
###check double type later
######Pokemon instance creation
##Initialize all pokemon with: level, name (optional), trainer (optional)
starterBulbasaur=bulbasaur(8,"Bulbasaur")
betaBulbasaur=bulbasaur(20,"Ivysaur")
powerBulbasaur=bulbasaur(50,"Venusaur")
starterCharmander=charmander(8,"Charmander")
betaCharmander=charmander(20,"Charmeleon")
powerCharmander=charmander(50,"Charizard")
starterSquirtle=squirtle(8,"Squirtle")
betaSquirtle=squirtle(20,"Wortortle")
powerSquirtle=squirtle(50,"Blastoise")
derpy=derp(30,"derpy")
rattata=rattata(6,"Rattata")
pidgey=pidgey(6,"Pidgey")
hovis=hovisquirrel(6,"Hovisquirrel")
hypnotoad=hypnotoad(6,"Hypnotoad")

######Hard sets of things that should be dynamically generated (Yeah testing!)
Red=PC("Red","female",[starterSquirtle,hypnotoad],20)
starterSquirtle.trainer=Red
hypnotoad.trainer=Red

Gary=character([powerBulbasaur],"Gary","wait for it",100,"normal")
powerBulbasaur.trainer=Gary


game=screen(41,11,inescapableHellscape) #START

#############List of Abominations Unto Nuggan
#Squirtles that think they're Charmanders
#Charmanders that know electric moves
#Everything is named Bulbasaur
#The number of times my computer crashed while I was coding this
#rattatas attacking themselves
#bool("False")=True
#circular dependencies, because they involve circular dependence
#up and down arrows being interpreted as weird non-ASCII characters
#trying to navigate the battle menus based on the first letter of each of the first two options
#C h a r m a n d e r r a n a w a y !
#Charmander learning Splash...twice.
