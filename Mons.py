########### Punkemon, because there need to be some mons in this mon-battling game ############
########## Imports from elsewhere
import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *
import os
import string

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
        self.critRate=self.permStats["Speed"]/512.0 #reset this at the start of every battle
        self.status={"poisoned":False,"burned":False,"frozen":False,"sleep":False,"paralyzed":False,"flinched":False,
                     "confused":False,"trapped":False,"multiple":False,"seeded":False,"charging":False,"justSentOut":False,"leaving":False,"usingItem":False} #poison/burn/freeze/sleep/paralysis/flinch/confused
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
        self.immuneToStatMoves=False

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
        if self.status["leaving"]:
            self.status["leaving"]=False
            canMove=False
            encouragement=encourageList[randint(0,len(encourageList)-1)]
            if isinstance(self.trainer,PC):
                messages.append("Go "+self.trainer.curMon.name+"!")
                messages.append(encouragement)
            else:
                messages.append(self.trainer.name+": Go "+self.trainer.curMon.name+"!")
                messages.append(self.trainer.name+": "+encouragement)
        elif self.status["flinched"]  or self.status["sleep"] or self.status["frozen"] or self.status["justSentOut"] or self.status["usingItem"]:
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
            elif self.status["usingItem"]:
                messages.append(self.trainer.name+" used "+self.trainer.lastItem.name+"!")
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
        if not len(monsSharing)==0: #everybody fainted, punt.
            if not communism:
                oneMonXP=XPPool/len(monsSharing) #number of XP awarded to each individual mon involved
            else:
                oneMonXP=.5*XPPool/len(monsSharing)
            for mon in monsSharing:
                old=mon.XP
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
            EVPool=list(self.baseStats)
            oneMonEVs=[]
            for ev in EVPool:
                oneMonEVs.append(float(ev)/len(monsSharing))
            for mon in monsSharing:
                for i in range(0,len(EVPool)):
                    mon.EVs[i]+=oneMonEVs[i]
            for mon in enemyTeam:
                correctLevel=mon.getLevelFromXP()
                if correctLevel!=mon.level and not isinstance(mon.trainer,wildPunkemon):
                    levelResults=mon.levelUp(correctLevel-mon.level)
                    levelingMessages=levelResults[0]
                    newMoveInfo=levelResults[1]
                    messages+=levelingMessages
            return [messages,newMoveInfo] #list of messages and a tuple of (move instance,mon instance)
        
        else:
            return([],(False,False))

    def levelUp(self,number=1):
        levelingMessages=[]
        moveOnDeck=False
        oldLevel=self.level
        self.level+=number
        newPermStats=self.getPermStats()
        self.updateTempStats(newPermStats)
        self.permStats=newPermStats
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
        if self.level>=self.evolveLevel>0: #returns true if self.evolveLevel isn't False and self.level>self.evolveLevel
            self.duplicate(False,self.nextEvolution)
            levelingMessages.append(self.name+" evolved into "+self.nextEvolution+"!")
            #change this to be voluntary, if and when you can be arsed
        return [levelingMessages,(moveOnDeck,self)]

    def updateTempStats(self,newPermStats):
        for stat in self.permStats.keys():
            difference=newPermStats[stat]-self.permStats[stat]
            self.tempStats[stat]+=difference

    def duplicate(self,newTrainer=False,newName=False,newSpecies=False):
        #use this to create new mon instances during capture and evolution
        if not newTrainer:
            newTrainer=self.trainer
        if not newSpecies:
            newSpecies=self.species
        if not newName:
            newName=self.name
        #Do something to prevent all ivysaurs being named "Bulbasaur" and/or capitalization issues
        newMonStr="newMon="+newSpecies+"("+str(self.level)+","+"'"+newName+"'"+")"
        exec(newMonStr)
        newMon.trainer=newTrainer
        if self in newTrainer.team:
            newTrainer.team[newTrainer.team.index(self)]=newMon
            if self==newTrainer.curMon:
                newTrainer.curMon=newMon
        else:
            newTrainer.team.append(newMon)
            #Add a case to put it in newTrainer.PCMons if the team is full
        newMon.XP=self.XP
        newMon.tempStats=self.tempStats
        newMon.updateTempStats(newMon.permStats)
        newMon.curMoves=self.curMoves
        newMon.IVs=self.IVs
        return newMon

###Mon species creation
##Initialize all species with:
##species,nation,specNum,level,learnSpeed,baseStats,baseXPworth,allMoves=[]
    
class Bulbasaur(punkemon):
    def __init__(self,level,name="Bulbasaur",trainer=False):
        self.evolveStone=False
        self.evolveLevel=16 #change this back to 16 when you're done testing!
        self.nextEvolution="Ivysaur"
        learnDict={0:tackle,1:growl,7:leechSeed,13:vineWhip,20:poisonPowder,27:razorLeaf,34:growth,41:sleepPowder,48:solarBeam}
        punkemon.__init__(self,"Bulbasaur",["Grass"],1,level,"medium",[49,49,45,45,65],64,learnDict,name,trainer)

class Ivysaur(punkemon):
    def __init__(self,level,name="Ivysaur",trainer=False):
        self.evolveStone=False
        self.evolveLevel=32
        self.nextEvolution="Venusaur"
        #FIX THE base stats, type
        learnDict={0:tackle, 1:growl, 2:leechSeed,13:vineWhip, 22:poisonPowder,30:razorLeaf,38:growth,46:sleepPowder,54:solarBeam}
        punkemon.__init__(self,"ivysaur",["Grass","Poison"],1,level,"medium",[62,63,60,60,80],141,learnDict,name,trainer)

class Venusaur(punkemon):
    def __init__(self,level,name="Venusaur",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        #Fix the base stats and type
        learnDict={0:tackle,1:growl,7:leechSeed,13:vineWhip,22:poisonPowder,30:razorLeaf,43:growth,55:sleepPowder,65:solarBeam}
        punkemon.__init__(self,"Venusaur",["Grass","Poison"],1,level,"medium",[82,83,80,80,100],208,learnDict,name,trainer)
        
class Charmander(punkemon):
    def __init__(self,level,name="Charmander",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:scratch,1:growl,9:ember,15:leer,30:slash,38:flamethrower,46:fireSpin}###Add rage at 22 once you have it coded!
        punkemon.__init__(self,"Charmander",["Fire"],4,level,"medium",[52,43,39,65,50],62,learnDict,name,trainer)
        
class Squirtle(punkemon):
    def __init__(self,level,name="Squirtle",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:tailWhip,8:bubble,15:waterGun,22:bite,28:withdraw,35:skullBash,42:hydroPump}
        punkemon.__init__(self,"Squirtle",["Water"],7,level,"medium",[48,65,44,43,50],63,learnDict,name,trainer)
     
class Rattata(punkemon):
    def __init__(self,level,name="Rattata",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:tailWhip,7:quickAttack,14:hyperFang}
        punkemon.__init__(self,"Rattata",["Normal"],19,level,"medium",[56,35,30,72,25],51,learnDict,name,trainer)

class Pidgey(punkemon):
    def __init__(self,level,name="Pidgey",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:gust,5:sandAttack,12:quickAttack,28:wingAttack}#19 whirlwind but that's dumb
        punkemon.__init__(self,"Pidgey",["Flying"],16,level,"medium",[45,40,40,56,35],50,learnDict,name,trainer)

class Eevee(punkemon):
    def __init__(self,level,name="Eevee",trainer=False):
        self.evolveLevel=False
        self.evolveStone=["water","fire","thunder"]
        self.evolveDict={"water":"Vaporeon","fire":"Flareon","thunder":"Jolteon"}
        learnDict={0:tackle,1:tailWhip,8:sandAttack,16:growl,23:quickAttack,30:bite,36:focusEnergy,42:takeDown} #add these moves
        punkemon.__init__(self,"Eevee",["Normal"],16,level,"fast",[55,50,55,55,65],92,learnDict,name,trainer)

class Jolteon(punkemon):
    def __init__(self,level,name="Jolteon",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:sandAttack,2:quickAttack,3:thunderShock,31:thunderShock,40:thunderWave,42:doubleKick,44:agility,48:pinMissile,54:thunder}
        punkemon.__init__(self,"Jolteon",["Electric"],16,level,"fast",[65,60,65,130,110],197,learnDict,name,trainer)

class Vaporeon(punkemon):
    def __init__(self,level,name="Vaporeon",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:sandAttack,2:quickAttack,3:waterGun,27:quickAttack,31:waterGun,36:auroraBeam,37:tailWhip,40:bite,42:acidArmor,48:mist,54:hydroPump}#add haze maybe
        punkemon.__init__(self,"Vaporeon",["Water"],16,level,"fast",[65,60,130,65,110],196,learnDict,name,trainer)

class Flareon(punkemon):
    def __init__(self,level,name="Flareon",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:sandAttack,2:quickAttack,3:ember,27:quickAttack,31:ember,37:tailWhip,40:bite,42:leer,44:fireSpin,54:flamethrower}#add rage maybe
        punkemon.__init__(self,"Flareon",["Fire"],16,level,"fast",[130,60,65,65,110],198,learnDict,name,trainer)

class Derp(punkemon):
    def __init__(self,level,name="Derp",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        punkemon.__init__(self,"Derp",["Normal"],0,2,"slow",[0,0,0,0,0],64,{0:splash},name,trainer)

class Rob(punkemon):
    def __init__(self,level,name="Rob Davidoff",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:Engineering,13:vineWhip,20:poisonPowder,27:razorLeaf,34:growth,41:sleepPowder,48:solarBeam}
        punkemon.__init__(self,"Rob",["Dragon"],200,level,"fast",[70,70,70,70,70],99,learnDict,name,trainer)

class LizardSpock(punkemon):
    def __init__(self,level,name="LizardSpock",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tackle,1:wrap,2:slash}#rock, paper, scissors aka tackle, wrap, slash
        punkemon.__init__(self,"LizardSpock",["Water"],152,level,"fast",[49,49,45,45,65],64,learnDict,name,trainer)

class Hovisquirrel(punkemon): #our analogue of vulpix; a squirrel with a flaming tail, for Rob's coworker Greg Hovis
    def __init__(self,level,name="Hovisquirrel",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:tailWhip,1:ember,16:quickAttack,21:roar,28:confuseRay,35:flamethrower,42:fireSpin}
        punkemon.__init__(self,"Hovisquirrel",["Fire"],37,level,"medium",[41,40,38,65,65],60,learnDict,name,trainer)

class Poliwag(punkemon): 
    def __init__(self,level,name="Poliwag",trainer=False):
        self.evolveLevel=25
        self.evolveStone=False
        self.nextEvolution="Poliwhirl"
        learnDict={0:bubble,16:hypnosis,19:waterGun,25:doubleSlap,31:bodySlam,38:amnesia,45:hydroPump}
        punkemon.__init__(self,"Poliwag",["Water"],62,level,"medium",[50,40,40,90,40],77,learnDict,name,trainer)

class Poliwhirl(punkemon): 
    def __init__(self,level,name="Poliwhirl",trainer=False):
        self.evolveLevel=False
        self.evolveStone=["water"]
        self.nextEvolution="Hypnotoad"
        #Fix learnDict, XP yield, base stats
        learnDict={0:hypnosis,1:waterGun,2:bubble,16:hypnosis,19:waterGun,26:doubleSlap,33:bodySlam,41:amnesia,49:hydroPump}
        punkemon.__init__(self,"Poliwhirl",["Water"],62,level,"medium",[65,65,65,90,50],131,learnDict,name,trainer)

class Hypnotoad(punkemon): #our analogue of polywrath
    def __init__(self,level,name="Hypnotoad",trainer=False):
        self.evolveStone=False
        self.evolveLevel=False
        learnDict={0:hypnosis,1:waterGun,2:doubleSlap,3:bodySlam}
        punkemon.__init__(self,"Hypnotoad",["Water","Fighting"],62,level,"medium",[85,95,90,70,70],255,learnDict,name,trainer)
        
