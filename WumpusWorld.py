import random
import os
import bcolors

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

#The Whole Wumpus-World field which is a 2 Dimensional 4x4 Array of WumpusWorldCell
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

    #starts the game and waits for the users actions
    def play(self):
        while not (self.gameOver() or self.gameWon()):
            clearConsole()
            self.displayHidden();

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
        self.display();

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


wumpusWorld = WumpusWorld()
wumpusWorld.play()
