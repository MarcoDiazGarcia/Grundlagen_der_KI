import random
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#Agent Class with his current Position(x, y)
class Agent:
    x = 0
    y = 0
    bumped = False
    arrows = 1

    def getCoordinates(self):
        return (self.x, self.y)

    def hasArrow(self):
        return self.arrows > 0

#One Cell in the 4x4 gamefield
class WumpusWorldCell:
    pit = False
    breeze = False
    wumpus = False
    stench = False
    gold = False

    def display(self):
        displayString = ""
        if self.pit:
            displayString += "P"
        if self.breeze:
            displayString += "B"
        if self.wumpus:
            displayString += "W"
        if self.stench:
            displayString += "S"
        if self.gold:
            displayString += "G"

        if len(displayString) == 0:
            displayString = "   "
        elif len(displayString) == 1:
            displayString = " " + displayString + " "
        elif len(displayString) == 2:
            displayString += " "

        return displayString

#The Whole Wumpus-World field which is a 2 Dimensional 4x4 Array of WumpusWorldCell
class WumpusWorld:
    agent = Agent()

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


    def cellIsPit(self, x, y):
        return self.world[y][x].pit

    def cellIsBreeze(self, x, y):
        return self.world[y][x].breeze

    def cellIsWumpus(self, x, y):
        return self.world[y][x].wumpus

    def cellIsStench(self, x, y):
        return self.world[y][x].stench

    def cellIsGold(self, x, y):
        return self.world[y][x].gold

    def cellIsAgent(self, x, y):
        return x == self.agent.x and y == self.agent.y

    def moveAgentUp(self):
        if self.agent.y < 3:
            self.agent.y += 1
            self.agent.bumped = False
        else:
            self.agent.bumped = True

    def moveAgentDown(self):
        if self.agent.y > 0:
            self.agent.y -= 1
            self.agent.bumped = False
        else:
            self.agent.bumped = True

    def moveAgentRight(self):
        if self.agent.x < 3:
            self.agent.x += 1
            self.agent.bumped = False
        else:
            self.agent.bumped = True

    def moveAgentLeft(self):
        if self.agent.x > 0:
            self.agent.x -= 1
            self.agent.bumped = False
        else:
            self.agent.bumped = True

    def gameOver(self):
        return self.cellIsPit(self.agent.x, self.agent.y) or self.cellIsWumpus(self.agent.x, self.agent.y)

    def gameWon(self):
        return self.cellIsGold(self.agent.x, self.agent.y)

    def play(self):
        while not (self.gameOver() or self.gameWon()):
            clearConsole()
            self.display();
            action = input("Action? [move/shoot]: ")
            direction = input("Direction? [up/down/left/right]: ")

            if action == "move":
                if direction == "up":
                    self.moveAgentUp()
                elif direction == "down":
                    self.moveAgentDown()
                elif direction == "right":
                    self.moveAgentRight()
                elif direction == "left":
                    self.moveAgentLeft()
            elif action == "shoot":
                if direction == "up":
                    self.shootUp()
                elif direction == "down":
                    self.shootDown()
                elif direction == "right":
                    self.shootRight()
                elif direction == "left":
                    self.shootLeft()

        clearConsole()
        self.display();


    def display(self):
        displayString = "+-------+-------+-------+-------+\n"
        for y in range(3,-1,-1):
            displayString += "|"
            for x in range(4):
                displayString += " " + self.world[y][x].display()
                if x == self.agent.x and y == self.agent.y:
                    displayString += " A |"
                else:
                    displayString += "   |"

            displayString += "\n+-------+-------+-------+-------+\n"

        print(displayString)


agent = Agent()

wumpusWorld = WumpusWorld()

wumpusWorld.play()
