import random
import os
import bcolors

NO_ACTION = -1
MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
SHOOT_UP = 4
SHOOT_RIGHT = 5
SHOOT_DOWN = 6
SHOOT_LEFT = 7

#clears the Console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

#Agent Class with his current Position(x, y)
class Agent:
    x = 0
    y = 0
    points = 0
    bumped = False
    hearedDeathScream = False
    arrows = 1
    amountKnownStenches = 0
    lastMove = NO_ACTION
    movedBack = False

    #Initialising the knowledgebase field as an array of KnowledgeBaseWumpusWorldCell
    def __init__(self):
        self.knowledgeBase = []

        for y in range(4):
            row = []
            for x in range(4):
                row.append(KnowledgeBaseWumpusWorldCell())

            self.knowledgeBase.append(row)

    def numberAdjacentCells(self, x, y):
        if (x == 0 or x == 3) and (y == 0 or y == 3):
            return 2
        elif x == 0 or x == 3 or y == 0 or y == 3:
            return 3
        else:
            return 4

    def recheckForWumpus(self):
        amountPossibleWumpus = 0
        for y in range(4):
            for x in range(4):
                if self.knowledgeBase[y][x].isPit() and self.knowledgeBase[y][x].mightBeWumpus():
                    self.knowledgeBase[y][x].setIsNotWumpus()
                elif self.knowledgeBase[y][x].mightBeWumpus():
                    amountPossibleWumpus += 1
        if amountPossibleWumpus == 1:
            for y in range(4):
                for x in range(4):
                    if self.knowledgeBase[y][x].mightBeWumpus():
                        self.knowledgeBase[y][x].setIsWumpus()
                        self.knowledgeBase[y][x].setIsNotPit()

    def checkCellForPit(self, x, y):
        if y >= 0 and y <= 3 and x >= 0 and x <= 3:
            numberBreezes = 0
            # If the cell is known as the wumpus or a free cell it can't be a pit
            if not (self.knowledgeBase[y][x].isWumpus() or self.knowledgeBase[y][x].free):
                #If we already know there a pit return true
                if self.knowledgeBase[y][x].isPit():
                    return True
                # If an adjacent cell of the to be checked cell was visited before and it isn't a breeze the cell to be checked is free
                if y < 3:
                    if self.knowledgeBase[y + 1][x].visited:
                        if self.knowledgeBase[y + 1][x].breeze:
                            numberBreezes += 1
                        else:
                            self.knowledgeBase[y][x].free
                if y > 0:
                    if self.knowledgeBase[y - 1][x].visited:
                        if self.knowledgeBase[y - 1][x].breeze:
                            numberBreezes += 1
                        else:
                            self.knowledgeBase[y][x].free
                if x < 3:
                    if self.knowledgeBase[y][x + 1].visited:
                        if self.knowledgeBase[y][x + 1].breeze:
                            numberBreezes += 1
                        else:
                            self.knowledgeBase[y][x].free
                if x > 0:
                    if self.knowledgeBase[y][x - 1].visited:
                        if self.knowledgeBase[y][x - 1].breeze:
                            numberBreezes += 1
                        else:
                            self.knowledgeBase[y][x].free

                if not self.knowledgeBase[y][x].free:
                    # If the number of breezes around the cell to be checked is equal to its amount of adjacent cells the cell is set as a pit
                    # If the number of breezes is less it might be a pit
                    if numberBreezes == self.numberAdjacentCells(x, y):
                        self.knowledgeBase[y][x].setIsPit()
                    else:
                        self.knowledgeBase[y][x].setMightBePit()

                    return True
                else:
                    return False

    def checkCellForWumpus(self, x, y):
        if y >= 0 and y <= 3 and x >= 0 and x <= 3:
            numberStenches = 0
            # If the cell is known as the wumpus or a free cell it can't be a pit
            if not (self.knowledgeBase[y][x].isPit() or self.knowledgeBase[y][x].free):
                #If we already know there a pit return true
                if self.knowledgeBase[y][x].isWumpus():
                    return True
                # If an adjacent cell of the to be checked cell was visited before and it isn't a breeze the cell to be checked is free
                if y < 3:
                    #print("up    ==> V: ", self.knowledgeBase[y + 1][x].visited, " | S: ", self.knowledgeBase[y + 1][x].stench)
                    if self.knowledgeBase[y + 1][x].visited:
                        if self.knowledgeBase[y + 1][x].stench:
                            numberStenches += 1
                        else:
                            self.knowledgeBase[y][x].free
                if y > 0:
                    #print("down  ==> V: ", self.knowledgeBase[y - 1][x].visited, " | S: ", self.knowledgeBase[y - 1][x].stench)
                    if self.knowledgeBase[y - 1][x].visited:
                        if self.knowledgeBase[y - 1][x].stench:
                            numberStenches += 1
                        else:
                            self.knowledgeBase[y][x].free
                if x < 3:
                    #print("right ==> V: ", self.knowledgeBase[y][x + 1].visited, " | S: ", self.knowledgeBase[y][x + 1].stench)
                    if self.knowledgeBase[y][x + 1].visited:
                        if self.knowledgeBase[y][x + 1].stench:
                            numberStenches += 1
                        else:
                            self.knowledgeBase[y][x].free
                if x > 0:
                    #print("left  ==> V: ", self.knowledgeBase[y][x - 1].visited, " | S: ", self.knowledgeBase[y][x - 1].stench)
                    if self.knowledgeBase[y][x - 1].visited:
                        if self.knowledgeBase[y][x - 1].stench:
                            numberStenches += 1
                        else:
                            #print("setting free")
                            self.knowledgeBase[y][x].free

                #print("free: ", self.knowledgeBase[y][x].free)
                if not self.knowledgeBase[y][x].free:
                    # If the number of breezes around the cell to be checked is equal to its amount of adjacent cells the cell is set as a pit
                    # If the number of breezes is less it might be a pit
                    if numberStenches >= 3:
                        self.knowledgeBase[y][x].setIsWumpus()
                        self.knowledgeBase[y][x].setIsNotPit()
                    else:
                        if numberStenches == self.amountKnownStenches:
                            self.knowledgeBase[y][x].setMightBeWumpus()
                        else:
                            self.knowledgeBase[y][x].setIsNotWumpus()

                    return True
                else:
                    self.knowledgeBase[y][x].setIsNotWumpus()
                    return False

    def setCurrentCellVisited(self):
        self.knowledgeBase[self.y][self.x].visited = True
        self.knowledgeBase[self.y][self.x].free = True
        self.knowledgeBase[self.y][self.x].setIsNotPit()
        self.knowledgeBase[self.y][self.x].setIsNotWumpus()

    def setAdjacentCellsFree(self):
        if self.y < 3:
            self.knowledgeBase[self.y + 1][self.x].free = True
        if self.y > 0:
            self.knowledgeBase[self.y - 1][self.x].free = True
        if self.x < 3:
            self.knowledgeBase[self.y][self.x + 1].free = True
        if self.x > 0:
            self.knowledgeBase[self.y][self.x - 1].free = True

    def evalBreeze(self, x, y):
        if self.knowledgeBase[y][x].breeze:
            numberPossiblePits = 0
            # Check adjecent cells if they are or might be a pit
            if self.checkCellForPit(x, y + 1):
                numberPossiblePits += 1
            if self.checkCellForPit(x, y - 1):
                numberPossiblePits += 1
            if self.checkCellForPit(x + 1, y):
                numberPossiblePits += 1
            if self.checkCellForPit(x - 1, y):
                numberPossiblePits += 1

            if numberPossiblePits == 1:
                if y < 3:
                    if self.knowledgeBase[y + 1][x].mightBePit():
                        self.knowledgeBase[y + 1][x].setIsPit()
                if y > 0:
                    if self.knowledgeBase[y - 1][x].mightBePit():
                        self.knowledgeBase[y - 1][x].setIsPit()
                if x < 3:
                    if self.knowledgeBase[y][x + 1].mightBePit():
                        self.knowledgeBase[y][x + 1].setIsPit()
                if x > 0:
                    if self.knowledgeBase[y][x - 1].mightBePit():
                        self.knowledgeBase[y][x - 1].setIsPit()

    def evalStench(self, x, y):
        if self.knowledgeBase[y][x].stench:
            numberPossibleWumpus = 0
            # Check adjecent cells if they are or might be a pit
            if self.checkCellForWumpus(x, y + 1):
                numberPossibleWumpus += 1
            if self.checkCellForWumpus(x, y - 1):
                numberPossibleWumpus += 1
            if self.checkCellForWumpus(x + 1, y):
                numberPossibleWumpus += 1
            if self.checkCellForWumpus(x - 1, y):
                numberPossibleWumpus += 1

            if numberPossibleWumpus == 1:
                if y < 3:
                    if self.knowledgeBase[y + 1][x].mightBeWumpus():
                        self.knowledgeBase[y + 1][x].setIsWumpus()
                if y > 0:
                    if self.knowledgeBase[y - 1][x].mightBeWumpus():
                        self.knowledgeBase[y - 1][x].setIsWumpus()
                if x < 3:
                    if self.knowledgeBase[y][x + 1].mightBeWumpus():
                        self.knowledgeBase[y][x + 1].setIsWumpus()
                if x > 0:
                    if self.knowledgeBase[y][x - 1].mightBeWumpus():
                        self.knowledgeBase[y][x - 1].setIsWumpus()

    def senseBreeze(self, cell):
        return cell.breeze

    def senseStench(self, cell):
        return cell.stench

    def sense(self, cell):
        emptyCell = True

        for y in range(4):
            for x in range(4):
                self.knowledgeBase[y][x].setIsNotPit()
                self.knowledgeBase[y][x].setIsNotWumpus()

        if self.senseBreeze(cell):
            emptyCell = False
            self.knowledgeBase[self.y][self.x].breeze = True
        if self.senseStench(cell):
            emptyCell = False
            self.knowledgeBase[self.y][self.x].stench = True
            self.amountKnownStenches += 1

        self.setCurrentCellVisited()

        if emptyCell:
            self.setAdjacentCellsFree()

        for y in range(4):
            for x in range(4):
                self.evalStench(x, y)

        for y in range(4):
            for x in range(4):
                self.evalBreeze(x, y)

        self.recheckForWumpus()

        self.display()

    def evalAction(self):
        if self.y < 3:
            if self.knowledgeBase[self.y + 1][self.x].free or not self.knowledgeBase[self.y + 1][self.x].isBlocked():
                if not self.movedBack and self.lastMove != MOVE_DOWN:
                    movedBack = False
                    return MOVE_UP
            if self.movedBack and self.lastMove != MOVE_DOWN:
                if not self.knowledgeBase[self.y + 1][self.x].isDeadly() and not self.knowledgeBase[self.y + 1][self.x].visited:
                    movedBack = False
                    return MOVE_UP
        if self.x < 3:
            if self.knowledgeBase[self.y][self.x + 1].free or not self.knowledgeBase[self.y][self.x + 1].isBlocked():
                if not self.movedBack and self.lastMove != MOVE_LEFT:
                    movedBack = False
                    return MOVE_RIGHT
            if self.movedBack and self.lastMove != MOVE_LEFT:
                if not self.knowledgeBase[self.y][self.x + 1].isDeadly() and not self.knowledgeBase[self.y][self.x + 1].visited:
                    movedBack = False
                    return MOVE_RIGHT
        if self.y > 0:
            if self.knowledgeBase[self.y - 1][self.x].free or not self.knowledgeBase[self.y - 1][self.x].isBlocked():
                if not self.movedBack and self.lastMove != MOVE_UP:
                    movedBack = False
                    return MOVE_DOWN
            if self.movedBack and self.lastMove != MOVE_UP:
                if not self.knowledgeBase[self.y - 1][self.x].isDeadly() and not self.knowledgeBase[self.y - 1][self.x].visited:
                    movedBack = False
                    return MOVE_DOWN
        if self.y > 3:
            if self.knowledgeBase[self.y][self.x - 1].free or not self.knowledgeBase[self.y][self.x - 1].isBlocked():
                if not self.movedBack and self.lastMove != MOVE_RIGHT:
                    movedBack = False
                    return MOVE_LEFT
            if self.movedBack and self.lastMove != MOVE_RIGHT:
                if not self.knowledgeBase[self.y][self.x - 1].isDeadly() and not self.knowledgeBase[self.y][self.x - 1].visited:
                    movedBack = False
                    return MOVE_LEFT

        if self.lastMove == NO_ACTION:
            return MOVE_UP
        elif self.lastMove == MOVE_UP:
            movedBack = not self.movedBack
            return MOVE_DOWN
        elif self.lastMove == MOVE_RIGHT:
            movedBack = not self.movedBack
            return MOVE_LEFT
        elif self.lastMove == MOVE_DOWN:
            movedBack = not self.movedBack
            return MOVE_UP
        elif self.lastMove == MOVE_LEFT:
            movedBack = not self.movedBack
            return MOVE_RIGHT

    #Agent moves up, if he bumpes into a wall he saves that in "bumped"
    def moveUp(self):
        self.points -= 1
        if self.y < 3:
            self.y += 1
            self.bumped = False
        else:
            self.bumped = True

    #Agent moves down, if he bumpes into a wall he saves that in "bumped"
    def moveDown(self):
        self.points -= 1
        if self.y > 0:
            self.y -= 1
            self.bumped = False
        else:
            self.bumped = True

    #Agent moves right, if he bumpes into a wall he saves that in "bumped"
    def moveRight(self):
        self.points -= 1
        if self.x < 3:
            self.x += 1
            self.bumped = False
        else:
            self.bumped = True

    #Agent moves left, if he bumpes into a wall he saves that in "bumped"
    def moveLeft(self):
        self.points -= 1
        if self.x > 0:
            self.x -= 1
            self.bumped = False
        else:
            self.bumped = True

    #returns wether the agent has arrows left or not
    def hasArrows(self):
        return self.arrows > 0

    #If the agent has arrows left he consumes(shoots) one arrow
    #Returning wether he was able to shoot or not
    def shoot(self):
        self.points -= 10
        if self.hasArrows():
            self.arrows -= 1
            return True
        else:
            return False

    #Set the "hearedDeathScream" variable
    def hearsDeathScream(self):
        self.hearedDeathScream = True

    #Displays the whole WumpusWorldField in the Console
    def display(self):
        displayString = "+-------+-------+-------+-------+\n"
        for y in range(3,-1,-1):
            displayString += "|"
            for x in range(4):
                displayString += " " + self.knowledgeBase[y][x].toString()
                displayString += " |"

            displayString += "\n+-------+-------+-------+-------+\n"

        print(displayString)

#One Cell in the 4x4 gamefield
class WumpusWorldCell:
    pit = False
    breeze = False
    wumpus = False
    stench = False
    gold = False

    #Returns a string representation of the Cell --> it is always 3 letters long
    def toString(self):
        displayString = ""
        numberAttributes = 0
        if self.pit:
            displayString += bcolors.CBLUEB + "P" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.breeze:
            displayString += bcolors.CBLUE + "B" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.wumpus:
            displayString += bcolors.CREDB + "W" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.stench:
            displayString += bcolors.CRED + "S" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.gold:
            displayString += bcolors.CDARKYELLOWB + "G" + bcolors.CDEFAULT
            numberAttributes += 1

        if numberAttributes == 0:
            displayString = "   "
        elif numberAttributes == 1:
            displayString = " " + displayString + " "
        elif numberAttributes == 2:
            displayString += " "

        return displayString

#WumpusWorldCell in the Knowledgebase
class KnowledgeBaseWumpusWorldCell:
    pit = 0;
    breeze = False;
    wumpus = 0;
    stench = False;
    gold = False;
    free = False;
    visited = False;

    def mightBePit(self):
        return self.pit == 1

    def isPit(self):
        return self.pit == 2

    def mightBeWumpus(self):
        return self.wumpus == 1

    def isWumpus(self):
        return self.wumpus == 2

    def setIsNotPit(self):
        self.pit = 0

    def setMightBePit(self):
        self.pit = 1

    def setIsPit(self):
        self.pit = 2

    def setIsNotWumpus(self):
        self.wumpus = 0

    def setMightBeWumpus(self):
        self.wumpus = 1

    def setIsWumpus(self):
        self.wumpus = 2

    def isDeadly(self):
        return self.isPit() or self.isWumpus()

    def isDangerous(self):
        return self.mightBePit() or self.mightBeWumpus()

    def isBlocked(self):
        return self.isDeadly() or self.isDangerous()

    #Returns a string representation of the Cell --> it is always 3 letters long
    def toString(self):
        displayString = ""
        numberAttributes = 0
        if self.mightBePit():
            displayString += bcolors.CBLUEB + "p" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.isPit():
            displayString += bcolors.CBLUEB + "P" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.breeze:
            displayString += bcolors.CBLUE + "B" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.mightBeWumpus():
            displayString += bcolors.CREDB + "w" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.isWumpus():
            displayString += bcolors.CREDB + "W" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.stench:
            displayString += bcolors.CRED + "S" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.gold:
            displayString += bcolors.CDARKYELLOWB + "G" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.free:
            displayString += bcolors.CGREENB + "F" + bcolors.CDEFAULT
            numberAttributes += 1
        if self.visited:
            displayString += bcolors.CGREEN + "V" + bcolors.CDEFAULT
            numberAttributes += 1

        if numberAttributes == 0:
            displayString = "     "
        elif numberAttributes == 1:
            displayString = "  " + displayString + "  "
        elif numberAttributes == 2:
            displayString = "  " + displayString + " "
        elif numberAttributes == 3:
            displayString = " " + displayString + " "
        elif numberAttributes == 4:
            displayString += " "

        return displayString

#The Whole Wumpus-World field which is a 2 Dimensional 4x4 Array of WumpusWorldCell with 3 Pits, 1 Wumpus and 1 Gold
class WumpusWorld:
    agent = Agent()

    #Initiating the WumpusWorldField with the 3 pits and corresponding breezes
    #the wumpus and its stenches as well as the gold
    def __init__(self):
        self.world = []

        for y in range(4):
            row = []
            for x in range(4):
                row.append(WumpusWorldCell())

            self.world.append(row)

        #Create 3 Pits with Breezes nearby
        i = 0
        while i < 3:
            x = random.randrange(0, 4, 1)
            y = random.randrange(0, 4, 1)
            if not(self.cellIsAgent(x, y) or self.cellIsPit(x, y) or self.cellIsBreeze(x, y)):
                self.world[y][x].pit = True
                if x > 0:
                    self.world[y][x-1].breeze = True
                if x < 3:
                    self.world[y][x+1].breeze = True
                if y > 0:
                    self.world[y-1][x].breeze = True
                if y < 3:
                    self.world[y+1][x].breeze = True

                i += 1

        #Create Wumpus with Stenches nearby
        i = 0
        while i < 1:
            x = random.randrange(0, 4, 1)
            y = random.randrange(0, 4, 1)
            if not(self.cellIsAgent(x, y) or self.cellIsPit(x, y)):
                self.world[y][x].wumpus = True
                if x > 0:
                    self.world[y][x-1].stench = True
                if x < 3:
                    self.world[y][x+1].stench = True
                if y > 0:
                    self.world[y-1][x].stench = True
                if y < 3:
                    self.world[y+1][x].stench = True

                i += 1

        #Create Gold
        i = 0
        while i < 1:
            x = random.randrange(0, 4, 1)
            y = random.randrange(0, 4, 1)
            if not(self.cellIsAgent(x, y) or self.cellIsPit(x, y) or self.cellIsWumpus(x, y)):
                self.world[y][x].gold = True

                i += 1

    #Returns wether the given cell contains a pit or not
    def cellIsPit(self, x, y):
        return self.world[y][x].pit

    #Returns wether the given cell contains a breeze or not
    def cellIsBreeze(self, x, y):
        return self.world[y][x].breeze

    #Returns wether the given cell contains the wumpus or not
    def cellIsWumpus(self, x, y):
        return self.world[y][x].wumpus

    #Returns wether the given cell contains a stench or not
    def cellIsStench(self, x, y):
        return self.world[y][x].stench

    #Returns wether the given cell contains the gold or not
    def cellIsGold(self, x, y):
        return self.world[y][x].gold

    #Return wether the given cell is Empty
    def cellIsEmpty(self, x, y):
        return not (self.cellIsPit(x, y) or self.cellIsBreeze(x, y) or self.cellIsWumpus(x, y) or self.cellIsStench(x, y) or self.cellIsGold(x, y))

    #Returns wether the given cell contains the agent or not
    def cellIsAgent(self, x, y):
        return x == self.agent.x and y == self.agent.y

    #Agent shoots an arrow up
    #If the Wumpus is being hit, the agent hears its death scream
    def shootUp(self):
        self.agent.shoot()
        x = self.agent.x
        for y in range(self.agent.y, 4):
            if self.cellIsWumpus(x, y):
                self.agent.hearsDeathScream()

    #Agent shoots an arrow down
    #If the Wumpus is being hit, the agent hears its death scream
    def shootDown(self):
        self.agent.shoot()
        x = self.agent.x
        for y in range(self.agent.y, -1, -1):
            if self.cellIsWumpus(x, y):
                self.agent.hearsDeathScream()

    #Agent shoots an arrow right
    #If the Wumpus is being hit, the agent hears its death scream
    def shootRight(self):
        self.agent.shoot()
        y = self.agent.y
        for x in range(self.agent.x, 4):
            if self.cellIsWumpus(x, y):
                self.agent.hearsDeathScream()

    #Agent shoots an arrow left
    #If the Wumpus is being hit, the agent hears its death scream
    def shootLeft(self):
        self.agent.shoot()
        y = self.agent.y
        for x in range(self.agent.x, -1, -1):
            if self.cellIsWumpus(x, y):
                self.agent.hearsDeathScream()

    #Returns wether the game is lost or not
    def gameOver(self):
        return self.cellIsPit(self.agent.x, self.agent.y) or (self.cellIsWumpus(self.agent.x, self.agent.y) and not self.agent.hearedDeathScream)

    #Return wether the game is won or not
    def gameWon(self):
        return self.cellIsGold(self.agent.x, self.agent.y)

    #Displays the whole WumpusWorldField in the Console
    def display(self):
        displayString = "+-------+-------+-------+-------+\n"
        for y in range(3,-1,-1):
            displayString += "|"
            for x in range(4):
                displayString += " " + self.world[y][x].toString()
                if self.cellIsAgent(x, y):
                    displayString += " " + bcolors.CGREEN + bcolors.CBLINK + "A" + bcolors.CDEFAULT + " |"
                else:
                    displayString += "   |"

            displayString += "\n+-------+-------+-------+-------+\n"

        print(displayString)

        if self.agent.bumped:
            print("Agent bumped into a wall!\n")
        if self.agent.hearedDeathScream:
            print("Agent heard wumpus death scream!\n")

    #Displays the WumpusWorldField but only the Cell containing the Agent is visible
    def displayHidden(self):
        displayString = "+-------+-------+-------+-------+\n"
        for y in range(3,-1,-1):
            displayString += "|"
            for x in range(4):
                if self.cellIsAgent(x, y):
                    displayString += " " + self.world[y][x].toString() + " " + bcolors.CGREEN + bcolors.CBLINK + "A" + bcolors.CDEFAULT + " |"
                else:
                    displayString += "       |"

            displayString += "\n+-------+-------+-------+-------+\n"

        print(displayString)

        if self.agent.bumped:
            print("Agent bumped into a wall!\n")
        if self.agent.hearedDeathScream:
            print("Agent heard wumpus death scream!\n")

    #starts the game and waits for the users actions
    def play(self):
        while not (self.gameOver() or self.gameWon()):
            clearConsole()
            self.display();

            correctInput = False
            while not correctInput:
                action = input("Action? [move/shoot]: ")
                correctInput = action in ("move", "m", "shoot", "s")

            correctInput = False
            while not correctInput:
                direction = input("Direction? [up/down/left/right]: ")
                correctInput = direction in ("up", "u", "down", "d", "left", "l", "right", "r")

            if action in ("move", "m"):
                if direction in ("up", "u"):
                    self.agent.moveUp()
                elif direction in ("down", "d"):
                    self.agent.moveDown()
                elif direction in ("right", "r"):
                    self.agent.moveRight()
                elif direction in ("left", "l"):
                    self.agent.moveLeft()
            elif action in ("shoot", "s"):
                if direction in ("up", "u"):
                    self.shootUp()
                elif direction in ("down", "d"):
                    self.shootDown()
                elif direction in ("right", "r"):
                    self.shootRight()
                elif direction in ("left", "l"):
                    self.shootLeft()

        clearConsole()
        if self.gameOver():
            self.agent.points -= 1000
            print(bcolors.CRED + bcolors.CBOLD + "GAME OVER" + bcolors.CDEFAULT)
        elif self.gameWon():
            self.agent.points += 1000
            print(bcolors.CGREEN + bcolors.CBOLD + "CONGRATULATIONS" + bcolors.CDEFAULT)

        print("You finished with ", self.agent.points, " points.\n")
        self.display()

    def playKI(self):
        while not (self.gameOver() or self.gameWon()):
            clearConsole()
            self.display();
            self.agent.sense(self.world[self.agent.y][self.agent.x])

            action = input("Press Enter for next move: ")

            move = self.agent.evalAction()

            if move == MOVE_UP:
                self.agent.moveUp()
            elif move == MOVE_DOWN:
                self.agent.moveDown()
            elif move == MOVE_RIGHT:
                self.agent.moveRight()
            elif move == MOVE_LEFT:
                self.agent.moveLeft()
            elif move == SHOOT_UP:
                self.shootUp()
            elif move == SHOOT_DOWN:
                self.shootDown()
            elif move == SHOOT_RIGHT:
                self.shootRight()
            elif move == SHOOT_LEFT:
                self.shootLeft()

            self.agent.lastMove = move

        clearConsole()
        if self.gameOver():
            self.agent.points -= 1000
            print(bcolors.CRED + bcolors.CBOLD + "GAME OVER" + bcolors.CDEFAULT)
        elif self.gameWon():
            self.agent.points += 1000
            print(bcolors.CGREEN + bcolors.CBOLD + "CONGRATULATIONS" + bcolors.CDEFAULT)

        print("You finished with ", self.agent.points, " points.\n")
        self.display()

wumpusWorld = WumpusWorld()
wumpusWorld.playKI()
