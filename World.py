class world:
    def __init__(self,screen,inputMap,dimx,dimy,landMonSeed=False,waterMonSeed=False,paddingChar="x"):
        #paddingChar is the screenName of the sprite displayed
        #if you're close enough to the edge of the world to see off it.
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
        self.dimx=dimx
        self.dimy=dimy
        self.landMonSeed=landMonSeed
        self.waterMonSeed=waterMonSeed
        self.paddingChar=paddingChar
        self.buildingDict={}
        #maps building names to coordinates
        self.permTerrainMap=self.getPermTerrainMap(inputMap,dimx,dimy)
        self.permSpriteMap=self.getPermSpriteMap(inputMap)
        #getSpriteMap will overwrite portions of terrainMap, and therefore needs to be called second
        self.permDrawMap=self.getPermDrawMap(inputMap)
        self.actionables=[]#add these later, there are enough init args as is
          

    def getPermTerrainMap(self,inputMap,dimx,dimy):
        terrainMap=[]
        xpos=1
        ypos=1
        for row in inputMap:
            terrainMap.append([])
            for char in row:
                if isinstance(char,str):
                    nextSpriteType=self.getTerrain(char)
                elif isinstance(char,tuple):
                    if isinstance(char[0],screenChanger):
                        nextSpriteType=2
                    if isinstance(char[0],building):
                        nextSpriteType=1
                    if isinstance(char[0],actionable):
                        nextSpriteType=self.getTerrain(" "+char[1])
                else:
                    print "Cannot handle terrain ",char
                terrainMap[-1].append(nextSpriteType)                        
                xpos+=1
            if len(terrainMap[-1])!=dimx:
                print "You bolloxed up the input map. Stop sucking so hard."
            xpos=0
            ypos+=1
        if len(terrainMap)!=dimy:
            print "You bolloxed up the input map. Stop sucking so hard."
        return terrainMap

    def getTerrain(self,char):
        #terrainDict={"T":1,"x":1,"-":0,"G":3,"w":4,"O":2," ":0,"B1":1}
        #0=passable, 1=impassable, 2=screenChanger, 3=land with encounters, 4=water
        #list of foreground sprites:
            #x=rock, T=tree, space=empty, (@=player)
        #list of background sprites:
            #G=tall grass, space=short grass, -=dirt, w=water

##        doubleMap=[
##        ["xG","xG","xG","xG","xG","xG"],
##        ["xG"," G"," G"," G"," G","xG"],
##        ["x-"," -"," -"," -"," -","x-"], 
##        ["x-"," -"," -"," -"," -","x-"],
##        ["x-","T ","T "," -"," -","x-"],
##        ["x ","  ","  ","  ","  ","x "],
##        ["x ","  ","  ","  ","  ","x "],
##        ["x ","  ","  ","  ","  ","x "],
##        ["x ","x ","x ","x ","x ","x "]
##                                ]
        if len(char)==1: #old map
            return terrainDict[char]
        elif len(char)==2:
            #need to create a mapping from 2 chars to 0,1,3,4 (2 is handled)
            tmpTerr=-1
            if char[1] in [" ","-"]:
                tmpTerr=0
            if char[1] in ["G"]:#list will later include encounter-dirt in caves
                tmpTerr=3
            if char[1]=="w":
                tmpTerr=4
            if char[0] in ["T","x"]:
                tmpTerr=1
            if tmpTerr!=-1:
                return tmpTerr
            else:
                print "Cannot parse terrain of ",char

    
    def getPermSpriteMap(self,inputMap): #also puts buildings in terrainMap
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
                if isinstance(char,tuple):
                    if isinstance(char[0],building):
                        self.buildingDict[char]=[xpos,ypos]
                else:
                    spriteMap[ypos][xpos]=char
                xpos+=1 #increment the x position after each char
            ypos+=1 #increment the y position after each row
        for item in self.buildingDict.keys(): #do buildings last so nothing gets pasted over them
            buildingPos=self.buildingDict[item]
            item[0].addToMap(self.permTerrainMap,spriteMap,buildingPos[0],buildingPos[1],item[1])
        return spriteMap

    def getPermDrawMap(self,inputMap): #This function does nothing, but it gets called in places, so leave it alone.
        drawMap=[]
        for row in inputMap:
            newRow=[]
            for char in row:
                newRow.append(char)
            drawMap.append(newRow)
        return drawMap

    def getTempTerrainMap(self):
        self.tempTerrainMap=safeCopy(self.permTerrainMap)
        for item in self.actionables:
            #fill appropriate spaces:
            self.tempTerrainMap[item.tempPos[1]][item.tempPos[0]]=5
            #5 at their pos,
            sightLineSquares=item.getSightLine(self.permTerrainMap)
            for square in sightLineSquares:
                self.tempTerrainMap[square[1]][square[0]]=6
            #6s in their sightlines
        return self.tempTerrainMap

    def getTempSpriteMap(self):
        self.tempSpriteMap=safeCopy(self.permSpriteMap)
        for item in self.actionables:
            self.tempSpriteMap[item.tempPos[1]][item.tempPos[0]]=(item,self.permSpriteMap[item.tempPos[1]][item.tempPos[0]][1])
        return self.tempSpriteMap

    def getTempDrawMap(self):
        self.tempDrawMap=safeCopy(self.permDrawMap)
        for item in self.actionables:
            self.tempDrawMap[item.tempPos[1]][item.tempPos[0]]=(item,self.permDrawMap[item.tempPos[1]][item.tempPos[0]][1])
        return self.tempDrawMap

    def updateMaps(self):
        self.getTempTerrainMap()
        self.getTempSpriteMap()
        self.getTempDrawMap()

    def getActiveTrainer(self,pos):
        for looker in self.actionables:
            if pos in looker.sightLineSquares:
                return looker

    def resetWorld(self):
        for item in self.actionables:
            item.tempPos=item.permPos

    def setRegion(self,ground,newVal,square,secondSquare=False):
        if not secondSquare:
            self.setSquare(square,ground,newVal)
            return
        else:
            row1=square[1]
            row2=secondSquare[1]
            col1=square[0]
            col2=secondSquare[0]
            if row1>row2:
                row1,row2=row2,row1
            if col1>col2:
                col1,col2=col2,col1
        for row in range(row1,row2+1):
            for col in range(col1,col2+1):
                self.setSquare([col,row],ground,newVal)
            

    def setSquare(self,square,ground,newVal):
        if ground not in ["foreground","background"]:
            print "ERROR: invalid foreground/background selection of",newVal
        if (ground=="background" and newVal not in worldBGSpriteDict):
            print "ERROR: invalid choice of background for",newVal,square
        if (ground=="foreground" and newVal not in worldFGSpriteDict):
            print "ERROR: invalid choice of foreground for",newVal,square
        row=square[1]
        col=square[0]
        oldStr=self.permSpriteMap[row][col]
        if ground=="foreground":
            self.permSpriteMap[row][col]=newVal+oldStr[1]
        elif ground=="background":
            self.permSpriteMap[row][col]=oldStr[0]+newVal
        self.permTerrainMap[row][col]=self.getTerrain(self.permSpriteMap[row][col])
        
        




            

worldBGSpriteDict={}
water=pygame.image.load(os.path.join("sprites","water.png"))
worldBGSpriteDict["w"]=water
grass=pygame.image.load(os.path.join("sprites","g.png"))
worldBGSpriteDict[" "]=grass
tallGrass=pygame.image.load(os.path.join("sprites","t.png"))
worldBGSpriteDict["G"]=tallGrass
dirt=pygame.image.load(os.path.join("sprites","p.png"))
worldBGSpriteDict["-"]=dirt

healthBarLeft=pygame.image.load(os.path.join("sprites","barEndLeft.png"))
healthBarRight=pygame.image.load(os.path.join("sprites","barEndRight.png"))
healthBarMiddle=pygame.image.load(os.path.join("sprites","barMiddle.png"))

worldFGSpriteDict={}
rock=pygame.image.load(os.path.join("sprites","b.png"))
worldFGSpriteDict["x"]=rock
tree=pygame.image.load(os.path.join("sprites","tree.png"))
worldFGSpriteDict["T"]=tree
blank=pygame.image.load(os.path.join("sprites","blank.png"))
worldFGSpriteDict[" "]=blank
player=pygame.image.load(os.path.join("sprites","player.png"))
worldFGSpriteDict["@"]=player
playerU=pygame.image.load(os.path.join("sprites","player_U.png"))
worldFGSpriteDict["@_U"]=playerU
playerL=pygame.image.load(os.path.join("sprites","player_L.png"))
worldFGSpriteDict["@_L"]=playerL
playerR=pygame.image.load(os.path.join("sprites","player_R.png"))
worldFGSpriteDict["@_R"]=playerR
playerD=pygame.image.load(os.path.join("sprites","player_D.png"))
worldFGSpriteDict["@_D"]=playerD
