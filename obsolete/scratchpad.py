class thing:
    def __init__(self,number,otherNumber):
        self.number=number
        self.otherNumber=otherNumber

    def duplicate(self,newNumber):
        newThing=self(newNumber,self.otherNumber)
        return newThing


firstThing=thing(1,2)
secondThing=firstThing.duplicate(3)
print firstThing.number
print secondThing.number
