test=[]
for row in range(0,7):
    tmprow=[]
    for col in range(0,5):
        tmprow.append(str(row) + str(col))
    test.append(tmprow)
xDim=3
yDim=5

centerX=(xDim-1)/2
centerY=(yDim-1)/2

playerX=centerX
playerY=centerY
topRow= playerY - (yDim-1)/2
bottomRow= topRow + yDim - 1
newRow=[]
for i in range(0,len(test[0])):
    newRow.append("  ")
test= -topRow*[newRow]+test
topRow = 0
bottomRow = yDim + topRow
bottomPad= bottomRow - len(test)
test= test + bottomPad*[newRow]

leftCol = playerX - (xDim-1)/2
rightCol = leftCol + yDim - 1
for i in range(0,len(test)):
    test[i]= -leftCol*["  "] + test[i]
leftCol = 0
rightCol = xDim
rightPad = xDim - len(test[0])
for i in range(0,len(test)):
    test[i]= test[i] + rightPad*["  "]

centerX=(xDim-1)/2
centerY=(yDim-1)/2
test[centerY][centerX]="me"
    
for line in test[topRow:bottomRow]:
    print line[leftCol:rightCol]
