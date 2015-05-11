################# Battles ####################   
class battle:
    def __init__(self,player,enemy,screen):
        self.player=player
        self.enemy=enemy
        self.screen=screen
        self.screenMessage=""
        self.curMenu=battleMenu("dialog",["bananaHammock"])
        screen.curBattle=self
        player.curMon=player.team[0]
        enemy.curMon=enemy.team[0]
        self.setupBattle()
        self.curPhase="start" # Options:"start", "initial input", "first attack", "second attack","between attacks", "after attacks"
        self.oldPhase="just started"
        self.needToInterrupt=[] #list of things we need to interrupt the turn order for:
                                #forced mon-switches, new moves, evolution, etc.
        self.switchTo("start")
        
    def getArray(self):
        return self.curMenu.getArray()#If you queried the wrong level, kick it down the chain of command
        
    def setupBattle(self):
        #resets all accuracies and evasions to 100, and all temporary statuses to False
        self.battleOver=False
        for mon in self.player.team+self.enemy.team:
            mon.accuracy=100
            mon.evasion=100
            mon.tempStats["Attack"]=mon.permStats["Attack"]
            mon.tempStats["Defense"]=mon.permStats["Defense"]
            mon.tempStats["Speed"]=mon.permStats["Speed"]
            mon.tempStats["Special"]=mon.permStats["Special"]
            mon.critRate=mon.permStats["Speed"]/512.0
            mon.immuneToStatMoves=False
            mon.status["confused"]=False
            mon.status["flinched"]=False
            mon.status["trapped"]=False
            mon.status["multiple"]=False
            mon.status["charging"]=False
            mon.monsFought=[]
        if self.enemy.curMon.species not in self.player.monsSeen:
            self.player.monsSeen.append(self.enemy.curMon.species)

    def switchTo(self,nextMenu): #switches to a new menu within the battle
        self.oldPhase=self.curPhase #phase of the battle
        self.phase=0 #phase of the current subroutine
        self.curMenu.curPos=1 #reset pointer on previous menu so it shows up in the right place
        if nextMenu=="start":
            self.curAction=self.startBattle
            self.curMenu.switchMenu([self.enemy.name+" wants to fight!"],"dialog")
        elif nextMenu=="choose":
            self.curPhase="initial input"
            self.curAction=self.getPlayerChoice
            self.curMenu.switchMenu(["Fight","Punkemon","Item","Flee"],"choice")
            self.player.curMon.status["justSentOut"]=False
            self.enemy.curMon.status["justSentOut"]=False
            self.player.curMon.status["usingItem"]=False
            self.enemy.curMon.status["usingItem"]=False #included for when we give gym leaders items
            
        elif nextMenu=="Fight":
            self.curPhase="initial input"
            self.curAction=self.getPlayerMove
            self.curMenu.switchMenu(list(self.player.curMon.curMoves),"choice")
                        
        elif nextMenu=="Punkemon":
            self.curPhase="initial input"
            self.curAction=self.getNextMon
            self.curMenu.switchMenu(list(self.player.team),"choice")
                        
        elif nextMenu=="Item":
            self.curPhase="initial input" #change back to between attacks if it crashes
            self.curAction=self.useItem
            invList=self.player.inventory.keys()
            opList=[]#list of useable options and their numbers
            for item in range(0,len(invList)):
                i=invList[item]#i is now the item name
                opList.append(i+" ("+str(self.player.inventory[i])+")") #show number available
            invMode="choice"
            if opList==[]:
                opList=["You don't have any items."]
                invMode="dialog"
            self.curMenu.switchMenu(opList,invMode)

        elif nextMenu=="Get target mon":
            self.curPhase="initial input"
            self.phase=0
            self.curAction=self.getTargetMon
            self.curMenu.switchMenu(self.player.team,"choice")

        elif nextMenu=="Process ball": #remove this if you get catching set up and don't start using it
            print "You need to actually fill out the switchTo process ball block"
            
        elif nextMenu=="Flee":
            succeed=self.computeFlee()
            if succeed:
                self.curMenu.switchMenu([self.player.curMon.name+" ran away!"],"dialog")
                self.battleOver=True
                self.screen.switchTo("world")                
            else:
                self.curMenu.switchMenu(["Can't escape!"],"dialog")
                self.curAction=self.cantRun 
                
        elif nextMenu=="Start attack":
            self.curPhase="initial input"
            self.curMenu.switchMenu(self.setupAttack(),"dialog")
            self.curAction=self.displayResults
                        
        elif nextMenu=="Next attack": #execute turn, next mon to attack...attacks.
            if self.oldPhase=="initial input":
                self.curPhase="first attack"
            elif self.oldPhase=="first attack" or self.oldPhase=="between attacks":
                self.curPhase="second attack"
            elif self.oldPhase=="second attack" or self.oldPhase=="after attacks":
                self.switchTo("choose") #That's right, recursion motherfuckas!
            if self.curPhase=="first attack" or self.curPhase=="second attack":
                self.curMenu.switchMenu(self.runAttack(),"dialog") #does the damage and whatnot, then return a list of messages explaining what happened
                self.curAction=self.displayResults
            
        elif nextMenu=="Mon Switch":
            if self.oldPhase=="first attack":
                self.curPhase="between attacks"
            else:
                self.curPhase="after attacks"
            self.curAction=self.forceNextMon
            self.phase=0
            self.curMenu.switchMenu(list(self.player.team),"choice")

        elif nextMenu=="New move":
            self.curAction=self.teachMove
            self.phase=0
            self.curMenu.switchMenu(["Overwrite a move and learn "+self.moveOnDeck.name,"Keep current moves"],"choice")

        elif nextMenu=="Display Results":
            self.curAction=self.displayResults
            
        elif nextMenu=="End":
            self.curMenu.options=[]
            if self.player.curMon:
                victor=self.player
                loser=self.enemy
                self.enemy.fought=True
            else:
                victor=self.enemy
                loser=self.player
            victor.money+=loser.money/2
            if self.player.getNumUnfainted>0:
                self.phase=0
                if not isinstance(self.enemy,wildPunkemon):
                    self.curAction=self.processWin
                    self.curMenu.switchMenu([self.player.name+" got "+str(loser.money/2)+" PunkeBucks for winning!"],"dialog")
                    #we need to get the pokedollarsign sprite into the font file
                else:
                    #wild punkemon don't have end dialogs, so we don't need process win, and they don't have money either
                    self.screen.switchTo("world")
            else:
                self.curAction=self.processLose
                self.curMenu.switchMenu([self.player.name+" whited out!"],"dialog")
        else:
            print "I don't know how to switch to", nextMenu

        
    def startBattle(self,event):
        if not event:
            pass
        elif event.key==K_a or event.key==K_s:
            if self.phase==0:
                if isinstance(self.enemy,wildPunkemon):
                    messageList=["Go, "+self.player.curMon.name+"!"]
                else:
                    messageList=[self.enemy.name+" sent out "+self.enemy.curMon.name+"!","Go, "+self.player.curMon.name+"!"]
                self.curMenu.switchMenu(messageList,"dialog")
                self.phase=1
            else:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.switchTo("choose")
            

    def getPlayerChoice(self,event):
        #this function is called 24 times/sec when the player is looking at the fight/switch/bag/run menu.
        if not event:
            pass #user did nothing. Act casual.
        elif event.key==K_UP:
            self.curMenu.curPos-=1
            if self.curMenu.curPos==0:
                self.curMenu.curPos=self.curMenu.length
        elif event.key==K_DOWN:
            self.curMenu.curPos+=1
            if self.curMenu.curPos>self.curMenu.length:
                self.curMenu.curPos=1
        elif event.key==K_a:
            self.switchTo(self.curMenu.getNext()) #call our hella handy switchTo function to switch to the menu for Fight, Punkemon, Item, or Flee

    def getPlayerMove(self,event):
        #called 24x/sec while staring at the move list screen
        if not event:
            pass
        elif event.key==K_UP:
            self.curMenu.curPos-=1
            if self.curMenu.curPos==0:
                self.curMenu.curPos=self.curMenu.length
        elif event.key==K_DOWN:
            self.curMenu.curPos+=1
            if self.curMenu.curPos>self.curMenu.length:
                self.curMenu.curPos=1
        elif event.key==K_s:
            self.switchTo("choose")
        elif event.key==K_a:
            self.player.curMon.curMove=self.player.curMon.curMoves[self.curMenu.curPos-1] #Way too many scurvy curs
            self.switchTo("Start attack")
            
    def getNextMon(self,event):
        if not event:
            pass
        elif self.phase==0:
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curMenu.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_s:
                self.switchTo("choose")
            elif event.key==K_a:
                mon=self.player.team[self.curMenu.curPos-1]
                if mon.tempStats["HP"]!=0 and mon is not self.player.curMon:
                    self.player.nextMon=mon
                    #do some screen stuff to display the new mon
                    self.player.nextMon.status["justSentOut"]=True
                    #prevent the old mon from getting a last attack in
                    print self.player.curMon.name,"leaving set"
                    self.player.curMon.status["leaving"]=True
                    self.switchTo("Start attack")
                elif mon is self.player.curMon:
                    self.phase=1
                    self.curMenu.switchMenu([mon.name+" is already out!"],"dialog")
                else:
                    self.phase=1
                    self.curMenu.switchMenu(["There's no will to fight!"],"dialog")
        elif self.phase==1 and (event.key==K_a or event.key==K_s):
            self.phase=0
            self.curMenu.switchMenu(list(self.player.team),"choice")

    def forceNextMon(self,event): #called if your mon faints
        if not event:
            pass
        elif self.phase==0:
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_a:
                mon=self.player.team[self.curMenu.curPos-1]
                if mon.tempStats["HP"]!=0:
                    self.player.curMon=mon
                    if self.curPhase=="between attacks":
                        #if still in the first half-turn and the one about to go just fainted, the new one doesn't get to go
                        self.player.curMon.status["justSentOut"]=True
                    #do some screen stuff to display the new mon
                    self.curMenu.switchMenu(["Come on, " + self.player.curMon.name + "!"],"dialog")
                    self.switchTo("Display Results") #Will go back to display results and handle any other interrupts
                else:
                    self.phase=1
                    self.curMenu.switchMenu(["There's no will to fight!"],"dialog")
        elif self.phase==1:
            self.phase=0
            self.curMenu.switchMenu(list(self.player.team),"choice")

    def teachMove(self,event):
        if not event:
            pass
        elif self.phase==0:#choosing whether to overwrite. curpos=1 means overwrite, curpos=2 means don't.
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_a:
                if self.curMenu.curPos==1:
                    moveNamesList=[]
                    for move in self.monToTeach.curMoves:
                        moveNamesList.append(move.name)
                        self.phase=1
                    self.curMenu.switchMenu(moveNamesList,"choice")
                elif self.curMenu.curPos==2:
                    self.switchTo("Display Results")
        elif self.phase==1:
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_a: #the only block that gets us out of this fifty-if pileup
                oldMove=self.monToTeach.curMoves[self.curMenu.curPos-1]
                self.monToTeach.curMoves[self.curMenu.curPos-1]=self.moveOnDeck
                self.curMenu.switchMenu([self.monToTeach.name+" forgot "+oldMove.name+" and learned "+self.moveOnDeck.name]+".","dialog")
                self.monToTeach=False
                self.moveOnDeck=False
                self.switchTo("Display Results")
            elif event.key==K_s:
                self.phase=0
                self.curMenu.switchMenu(["Overwrite a move and learn "+self.moveOnDeck.name,"Keep current moves"],"choice")

    def useItem(self,event):
        if not event:
            pass
        else:
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curMenu.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_a:#sets up item use, but doesn't execute it (that's in getCanMove when we announce it)
                if len(self.player.inventory)>0:
                    selected=self.player.inventory.keys()[self.curMenu.curPos-1]
                    itemToUse=itemDict[selected]#maps from name to item instance
                    self.player.lastItem=itemToUse
                    self.player.curMon.curMove="item"
                    self.player.curMon.status["usingItem"]=True
                if itemToUse.isLegal==item.ballLegal:#This is a trashy hack and I should feel bad
                    if isinstance(self.enemy,wildPunkemon):
                        caught=itemToUse.use(itemToUse,self.player,self.enemy.curMon)
                        if caught:
                            if not self.enemy.curMon.species in self.player.monsCaught:
                                self.player.monsCaught.append(self.enemy.curMon.species)
                            gameScreen=self.screen
                            self.screen.activeMenus=[menu([self.enemy.curMon.name+" was caught!"],"dialog","self.screen.switchTo('world')","pass",False,False,self.screen)]
                            self.screen.switchTo("newMenu")
                    else:
                        self.curMenu.switchMenu(["What are you smoking? Now's not the time for that!"],"dialog")
                else:
                    self.switchTo("Get target mon")
            elif event.key==K_s:
                self.switchTo("choose")

    def getTargetMon(self,event):
        if not event:
            pass
        elif self.phase==0:
            if event.key==K_UP:
                self.curMenu.curPos-=1
                if self.curMenu.curPos==0:
                    self.curMenu.curPos=self.curMenu.length
            elif event.key==K_DOWN:
                self.curMenu.curPos+=1
                if self.curMenu.curPos>self.curMenu.length:
                    self.curMenu.curPos=1
            elif event.key==K_s:
                self.switchTo("Item")
            elif event.key==K_a:
                mon=self.player.team[self.curMenu.curPos-1]
                if self.player.lastItem.isLegal(self.player.lastItem,mon,True): #change this to legal-item-use conditional function
                    self.itemTargetMon=mon
                    self.switchTo("Start attack")
                else:
                    self.phase=1
                    self.curMenu.switchMenu(["What are you smoking? Now's not the time for that!"],"dialog")
        elif self.phase==1:
            if event.key==K_s or event.key==K_a:
                self.phase=0
                self.curMenu.switchMenu(self.player.team,"choice")


    def computeFlee(self):
        yourSpeed=self.player.curMon.tempStats["Speed"]
        theirSpeed=self.enemy.curMon.tempStats["Speed"]
        if ((theirSpeed/4.0)%256)==0:
            succeed=True
        else:
            fleeChance=yourSpeed*32.0/((theirSpeed/4.0)%256)+30
            #technically the 30 should be multiplied
            #by the number of times you've tried to run since you last attacked,
            #but I can't be arsed.
            randomNumber=randint(0,256)
            if randomNumber<fleeChance:
                succeed=True
            else:
                succeed=False
        return succeed

    def cantRun(self,event):
        self.switchTo("choose")
                    
    def setupAttack(self):
        #runs all the pre-attack preliminaries and assembles messages.
        #Gets some HP information and displays it, gets the enemy's next move, gets the move order, then gets out

        #Potential cases:
        #1) Pokemon fainted on first attack, already moved. Do not set flinch to true, second mon gets its attack in on the new pokemon regardless of relative speed.
        #2) Pokemon fainted on first attack, has not yet moved. Incoming mon doesn't get to attack, so we need to set flinch to True.
        #3) Pokemon fainted at end of second attack. End combat round as usual, don't set flinch, let next round sort it out.
        #4) Both pokemon faint on first attack. Should be handled fine under combination of case 1&2.
        #5) Both pokemon faint on second attack. Handled fine as a special case of case 3.
        #Note to us: put a check that whofainted.curMon is Second after the first instance, anad only the first instance, of attack().
        #Also, when you have a bowl of chips and a bowl of dip, stick your hand in the former, not the latter.
        
        player=self.player
        enemy=self.enemy
        self.needToInterrupt=[]
        messages=[]
        self.addToMonsFought()
        playerHPPercent=round(float(player.curMon.tempStats["HP"]/player.curMon.permStats["HP"]*100),3)
        enemyHPPercent=round(float(enemy.curMon.tempStats["HP"]/enemy.curMon.permStats["HP"]*100),3)
        messages.append( "Your "+str(player.curMon)+" has "+str(player.curMon.tempStats["HP"])+" HP "+"("+str(playerHPPercent)+"%)")
        messages.append( "Enemy "+str(enemy.curMon)+" has "+str(enemy.curMon.tempStats["HP"])+" HP "+"("+str(enemyHPPercent)+"%)")
        #self.player.curMon.curMove=self.player.getNextMove() #superceded, take this out when you're sure you don't need it
        self.enemy.curMon.curMove=self.enemy.getNextMove()
        (self.first,self.second)=self.getMoveOrder(self.player,self.enemy)
        self.curAttacker=self.first #the player instance currently attacking
        self.curDefender=self.second #the player instance currently defending
        return messages

    def runAttack(self):
        #runs self.curAttacker's attack on curDefender, does effects and returns a set of messages
        messages=[]
        self.addToMonsFought() #if we put mons in the XP list before every attack, we'll never have one faint before getting added.
        attackMessages=self.Attack(self.curAttacker.curMon,self.curDefender.curMon)
        messages+=attackMessages
        faintResults=self.checkFaint()
        whoFainted=faintResults[0]
        XPMessages=faintResults[1]
        if whoFainted:
            for character in whoFainted:
                messages.append(str(character.curMon)+" fainted!")
                messages+=XPMessages
                if character==self.enemy:
                    (character.curMon,monMessages)=character.getNextMon()
                    if character.curMon and self.curPhase=="first attack":
                        #if still in the first half-turn and the one about to go just fainted, the new one doesn't get to go
                        character.curMon.status["justSentOut"]=True
                    messages+=monMessages
                if character==self.player:
                    character.curMon=False #serves as flag that we need to switch to getPlayerMon
                    self.needToInterrupt.append("Mon Switch") #flags that we need to break between attacks and switch to Force Next Mon
                if character.getNumUnfainted()==0:
                    self.battleOver=True
                    if character==self.player:
                        messages.append(character.name+" is out of pokemon!")
                    elif not isinstance(character,wildPunkemon):
                        messages.append(character.name+" was defeated!")
        #done with the half-turn, switch attacking and defending characters
        self.curAttacker,self.curDefender=self.curDefender,self.curAttacker
        return messages

    def displayResults(self,event):
        if event.key==K_a or event.key==K_s:
            if not self.curMenu.getNext(): #If we have messages, go to the next one. If we're out of messages,
                if self.needToInterrupt!=[]: #try popping the interrupt queue.
                    nextThing=self.needToInterrupt.pop(0)
                    if isinstance(nextThing,tuple):
                        self.moveOnDeck=nextThing[0]
                        self.monToTeach=nextThing[1]
                        self.switchTo("New move")
                    elif not self.battleOver: #forced mon switch, not a tuple, and we need to switch because the battle's not done
                        self.switchTo(nextThing)
                    else:
                        self.switchTo("End")
                elif self.battleOver:
                    self.switchTo("End")
                else:
                    self.switchTo("Next attack")
    
    def processWin(self,event):
        if self.enemy.afterDialog:
                    self.screen.activeMenus[-1]=self.enemy.afterDialog
                    self.screen.switchTo("newMenu")
        else:
            self.screen.switchTo("world")

    def processLose(self,event):
        self.screen.switchTo("world")
        #change this eventually so it heals your team and puts you in the last punkemon center you visited
    
    def getMoveOrder(self,player,enemy): 
        #calculate who moves first
        first=player;second=enemy #only change this if enemy goes first
        #check for item usage, which always goes first
        if player.curMon.curMove=="item":
            return (first,second)
        #calculate speeds
        ownSpeed=player.curMon.tempStats["Speed"]
        enemySpeed=enemy.curMon.tempStats["Speed"]
        #if both or neither using fast moves
        if player.curMon.curMove.fastMove==enemy.curMon.curMove.fastMove:
            #Speed duel
            if ownSpeed<enemySpeed:
                first=enemy;second=player
                ##Note: as currently implemented, player wins ties.
        else: #if one fast move in play
            #if your fast move, run your move first
            if enemy.curMon.curMove.fastMove:
                first=enemy;second=player
        #print first.curMon,"goes first" #longcat is long, firstMon is first
        return (first,second)

    def Attack(self,attacker,defender):
        #run twice with (firstMon, secondMon) and (secondMon, firstMon)
        #Handle attacks (hits and damage)
        messages=[]
        #make sure the mons involved are the updated ones
        if attacker.trainer.nextMon:
            attacker.trainer.curMon=attacker.trainer.nextMon
            attacker.trainer.nextMon=False
        if defender.trainer.nextMon:
            defender.trainer.curMon=defender.trainer.nextMon
            defender.trainer.nextMon=False
        (canMove,canMoveMessages)=attacker.getCanMove()
        messages+=canMoveMessages
        if attacker.curMove=="item":
            messages.append(self.player.lastItem.use(self.player.lastItem,self.player,self.itemTargetMon))
        if canMove:
            move=attacker.curMove
            messages.append(str(attacker)+" used "+str(move)+"!")
            index=attacker.curMoves.index(move)
            attacker.curPP[index]-=1
            (hit,hitMessages)=move.getHit(attacker,defender)
            messages+=hitMessages
            if hit:
                if move.sideEffect and move.sideEffect[0:5]=="chain":
                    numHits=eval(move.sideEffect[6:])
                else:
                    numHits=1
                for i in range(0,numHits):
                    damage=move.getDamage(attacker,defender)
                    if damage>0:
                        #messages.append(str(attacker)+" hits for "+str(damage)+" damage!")
                        pass
                    else:
                        pass #this is where special messages go if/when you want them
                    defender.tempStats["HP"]-=damage
                    messages+=attacker.curMove.getEffect(attacker,defender)
        statusMessages=attacker.getStatusDamage(defender)
        messages+=statusMessages
        return messages

    def checkFaint(self): # calls awardXP where needed, returns fainted mon or False
        fainted=[]
        XPMessages=[]
        if self.player.curMon.tempStats["HP"]<=0:
            self.player.curMon.tempStats["HP"]=0 #prevent negative hit points
            fainted.append(self.player)
            XPMessages+=self.player.curMon.awardXP(self.enemy.team)[0]
            self.player.curMon.monsFought=[]
        if self.enemy.curMon.tempStats["HP"]<=0:
            self.enemy.curMon.tempStats["HP"]=0 #prevent negative hit points
            fainted.append(self.enemy)
            XPResults=self.enemy.curMon.awardXP(self.player.team)
            XPMessages+=XPResults[0]
            if XPResults[1][0]:#need to interrupt for a new move
                self.needToInterrupt.append(XPResults[1])#interrupt queue now contains the move instance to teach and who to
            self.enemy.curMon.monsFought=[]
        return [fainted,XPMessages]

    def addToMonsFought(self): #if you're not sure whether or not to call this function, call it. It can never fuck anything up.
        if self.player.curMon not in self.enemy.curMon.monsFought: #add player's mon to enemy's mon's list
            self.enemy.curMon.monsFought.append(self.player.curMon)
        if self.enemy.curMon not in self.player.curMon.monsFought: #add enemy's mon to player's mon's list
            self.player.curMon.monsFought.append(self.enemy.curMon)
        if self.enemy.curMon.species not in self.player.monsSeen:
            self.player.monsSeen.append(self.enemy.curMon.species)
            

    
