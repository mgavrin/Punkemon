test=[]
for row in range(0,7):
    tmprow=[]
    for col in range(0,5):
        tmprow.append(str(row) + str(col))
    test.append(tmprow)


xDim=5
yDim=5

playerX=2
playerY=4

topRow= playerY - (yDim-1)/2
newRow=[]
for i in range(0,len(test[0])):
    newRow.append("  ")
test= -topRow*[newRow]+test
if topRow <0:
    topRow = 0
bottomRow = yDim + topRow
bottomPad= bottomRow - len(test)
test= test + bottomPad*[newRow]

leftCol = playerX - (xDim-1)/2
for i in range(0,len(test)):
    test[i]= -leftCol*["  "] + test[i]
if leftCol <0:
    leftCol = 0
rightCol = xDim + leftCol
rightPad = rightCol - len(test[0])
for i in range(0,len(test)):
    test[i]= test[i] + rightPad*["  "]

chop=[]  
for line in test[topRow:bottomRow]:
    chop.append( line[leftCol:rightCol])
centerX=(xDim-1)/2
centerY=(yDim-1)/2

chop[centerY][centerX]="me"
print leftCol, rightCol
for line in chop:
    print line
