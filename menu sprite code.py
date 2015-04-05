menuSpriteDict={}
for letter in string.ascii_uppercase:
    uppercaseCode="cap"+str(letter)+'=pygame.image.load(os.path.join("Font","'+str(letter)+'.png"))'
    exec(uppercaseCode)
    menuSpriteDict[str(letter)]=eval("cap"+str(letter))
for letter in string.ascii_uppercase:
    lowercaseCode="low"+str(letter)+'=pygame.image.load(os.path.join("Font","low'+str(letter)+'.png"))'
    exec(lowercaseCode)
    menuSpriteDict[str(letter.lower())]=eval("low"+str(letter))
for number in string.digits:
    numberCode="num"+str(number)+'=pygame.image.load(os.path.join("Font","num'+str(number)+'.png"))'
    exec(numberCode)
    menuSpriteDict[str(number)]=eval("num"+str(number))
space=pygame.image.load(os.path.join("Font","space.png"))
menuSpriteDict[" "]=space
comma=pygame.image.load(os.path.join("Font","comma.png"))
menuSpriteDict[","]=comma
period=pygame.image.load(os.path.join("Font","dot.png"))
menuSpriteDict["."]=period
exclaim=pygame.image.load(os.path.join("Font","bang.png"))
menuSpriteDict["!"]=exclaim
question=pygame.image.load(os.path.join("Font","question.png"))
menuSpriteDict["?"]=question
apostrophe=pygame.image.load(os.path.join("Font","apostrophe.png"))
menuSpriteDict["'"]=apostrophe #'"'"'"'"'"'"'"
quote=pygame.image.load(os.path.join("Font","quote.png"))
menuSpriteDict['"']=quote #'"'"'"'"'"'"'"
dash=pygame.image.load(os.path.join("Font","dash.png"))
menuSpriteDict["-"]=dash
colon=pygame.image.load(os.path.join("Font","colon.png"))
menuSpriteDict[":"]=colon
slash=pygame.image.load(os.path.join("Font","slash.png"))
menuSpriteDict["/"]=slash
openParen=pygame.image.load(os.path.join("Font","openparen.png"))
menuSpriteDict["("]=openParen
closeParen=pygame.image.load(os.path.join("Font","closeparen.png"))
menuSpriteDict[")"]=closeParen
ellipsis=pygame.image.load(os.path.join("Font","ellipses.png"))
menuSpriteDict["~"]=ellipsis
hashTag=pygame.image.load(os.path.join("Font","hash.png"))
menuSpriteDict["#"]=hashTag
percent=pygame.image.load(os.path.join("Font","percent.png"))
menuSpriteDict["%"]=percent    
cornerBallTL=pygame.image.load(os.path.join("Font","pokeballTL.png"))
menuSpriteDict["*TL"]=cornerBallTL    
cornerBallTR=pygame.image.load(os.path.join("Font","pokeballTR.png"))
menuSpriteDict["*TR"]=cornerBallTR    
cornerBallBL=pygame.image.load(os.path.join("Font","pokeballBL.png"))
menuSpriteDict["*BL"]=cornerBallBL    
cornerBallBR=pygame.image.load(os.path.join("Font","pokeballBR.png"))
menuSpriteDict["*BR"]=cornerBallBR
horPipe=pygame.image.load(os.path.join("Font","horpipe.png"))
menuSpriteDict["="]=horPipe
vertPipe=pygame.image.load(os.path.join("Font","vertpipe.png"))
menuSpriteDict["|"]=vertPipe
TPipe=pygame.image.load(os.path.join("Font","topPipe.png"))
menuSpriteDict["T="]=TPipe
LPipe=pygame.image.load(os.path.join("Font","leftPipe.png"))
menuSpriteDict["L|"]=LPipe
BPipe=pygame.image.load(os.path.join("Font","botPipe.png"))
menuSpriteDict["B="]=BPipe
RPipe=pygame.image.load(os.path.join("Font","rightPipe.png"))
menuSpriteDict["R|"]=RPipe
cursor=pygame.image.load(os.path.join("Font","cursor.png"))
menuSpriteDict[">"]=cursor
