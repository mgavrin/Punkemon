######Move instances
##Initialize moves with: name,basePwr, baseAcc, maxPP, nation, special, sideEffect, message, fastMove=False, critRate=1
##Basic moves
tackle=move("Tackle",35,95,35,"Normal",False,False)
growl=move("Growl",0,100,40,"Normal",False,"enemy Attack -1","'s attack fell!")
tailWhip=move("Tail Whip",0,100,40,"Normal",False,"enemy Defense -1","'s defense fell!")
scratch=move("Scratch",40,100,35,"Normal",False,False)

##Bulbasaur
leechSeed=move("Leech Seed",0,90,10,"Grass",False,"100 seeded", " was seeded!")
vineWhip=move("Vine Whip",35,100,10,"Grass",False,False)
poisonPowder=move("Poisonpowder",0,75,35,"Poison",False,"100 poisoned"," was poisoned!")
razorLeaf=move("Razor Leaf",55,95,25,"Grass",False,False)
growth=move("Growth",0,100,40,"Normal",False,"self Special 1","'s special rose!")
sleepPowder=move("Sleep Powder",0,75,15,"Grass",False,"100 sleep"," fell asleep!")
solarBeam=move("Solar Beam",120,100,10,"Grass",True,"charging 2")#####needs to charge! #contemplate and/or add a special message here

##Charmander
ember=move("Ember",40,100,25,"Fire",True,"10 burn"," was burned!")
leer=move("Leer",0,100,30,"Normal",False,"enemy Defense -1","'s defense fell!")
####Add rage?
slash=move("Slash",70,100,20,"Normal",False,False,False,False,8)#high crit rate
flamethrower=move("Flamethrower",95,100,15,"Fire",True,"10 burned"," was burned!")
fireSpin=move("Fire Spin",15,70,15,"Fire",True,"multiple False"," is caught in the vortex!")#special message here won't display because you haven't handled charging and multiple

##Squirtle
bubble=move("Bubble",20,100,30,"Water",True,False)
waterGun=move("Water Gun",40,100,25,"Water",True,False)
bite=move("Bite",60,100,25,"Normal",False,"10 flinch"," flinched!")
withdraw=move("Withdraw",0,100,40,"Water",False,"self Defense 1","'s defense rose!")
skullBash=move("Skull Bash",100,100,15,"Normal",False,"charging 2")#contemplate/add special message
hydroPump=move("Hydro Pump",120,80,5,"Water",True,False)

#Rattata
quickAttack=move("Quick Attack",40,100,30,"Normal",False,False,True)
hyperFang=move("Hyper Fang",80,90,15,"Normal",False,"90 flinched"," flinched!")

#Pidgey
gust=move("Gust",40,100,35,"Normal",True,False)
wingAttack=move("Wing Attack",35,100,35,"Flying",False,False)
fly=move("Fly",90,95,15,"Flying",False,"charging offscreen")#contemplate/add special message

#Hovisquirrel aka vulpix
roar=move("Roar",0,100,20,"Normal",False,False)##currently does jack shit, make analogous to whirlwind
confuseRay=move("Confuse Ray",0,100,10,"Ghost",False,"100 confused"," became confused!")

#hypnotoad aka poliwrath and evolutions
hypnosis=move("Hypnosis",0,60,20,"Psychic",False,"100 sleep"," fell asleep!")
doubleSlap=move("Double slap",15,85,10,"Normal",False,"multiple False")
bodySlam=move("Body slam",85,100,15,"Normal",False,"30 paralyzed"," became paralyzed!")
amnesia=move("Amnesia",0,200,20,"Psychic",False,"self special 2","'s special greatly rose!")

#eevee and eeveelutions
takeDown=move("Takedown",90,85,20,"Normal",False, "exec attacker.tempStats['HP']-=eval(effectWords[2]) 0.25*self.getDamage(attacker,defender)",False)
#the third effectWord gets eval'd; it's an expression for the amount of recoil damage
thunderWave=move("Thunder Wave",0,100,20,"Electric",False,"100 paralyzed"," became paralyzed!")
agility=move("Agility",0,200,30,"Psychic",False,"self Speed 2","'s Speed rose!")
pinMissile=move("Pin Missile",25,95,20,"Bug",False,"chain randint(2,5)")
thunder=move("Thunder",110,70,10,"Electric",True,"10 paralyzed"," became paralyzed!")
auroraBeam=move("Aurora Beam",65,100,20,"Ice",True,"10 attack","'s attack fell!")
acidArmor=move("Acid Armor",0,200,20,"Poison",False,"self Defense 2","'s defense greatly rose!")
#Add Haze if you ever feel like a masochist
mist=move("Mist",0,200,30,"Ice",False,"exec attacker.immuneToStatMoves=True"," is shrouded in mist!")
smog=move("Smog",20,70,20,"Poison",True,"40 poisoned"," became poisoned!")
#Add rage to flareon's learnDict if you ever implement it for the char* line




#random fun stuff and moves that test important features
thunderShock=move("Thundershock",100,90,15,"Electric",True,"30 paralyzed"," became paralyzed!")
sandAttack=move("Sand Attack",0,90,20,"Normal",False,"enemy accuracy -1","'s accuracy fell!")##mul by 1.4^-1
splash=move("Splash",0,100,20,"Water",False,False)
engineering=move("Engineering",200,100,100,"Dragon",True,"100 confused"," became confused!",True,10)
hitYourself=move("hitYourself",40,200,100,"Fail",False,False,False,0)
struggle=move("Struggle",50,100,"Normal",False,False,False,1)
wrap=move("Wrap",15,90,20,"Normal",False,"multiple False")
dig=move("Dig",80,100,10,"Ground",False,"charging offscreen")#contemplate/add special message
focusEnergy=move("Focus Energy",0,200,30,"Normal",False,"self critRate 4"," is getting pumped!")
doubleKick=move("Double Kick",30,100,30,"Fighting",False,"chain 2")
