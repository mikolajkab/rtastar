import turtle
import time
import random
import numpy
import math
from operator import attrgetter


MAZE_HEIGHT = 14
MAZE_WIDTH = 14
STEP_COST = 3

POPULATION = [0, 1]
WEIGHTS = [0.5, 0.5]

window = turtle.Screen()
window.bgcolor("black")
window.title("Real-time A* algorithm")
window.setup(MAZE_HEIGHT*30, MAZE_WIDTH*30)


class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)

    def go_up(self):
        self.goto(self.xcor(), self.ycor() + 25)

    def go_down(self):
        self.goto(self.xcor(), self.ycor() - 25)

    def go_left(self):
        self.goto(self.xcor() - 25, self.ycor())

    def go_right(self):
        self.goto(self.xcor() + 25, self.ycor())


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isWall = [False]
        self.isGoal = False
        self.h = '-'
        self.h_prime = '-'
        self.f = '-'

    def setWall(self, wall):
        self.isWall = wall

    def getWall(self):
        return self.isWall

    def setH(self, h):
        self.h = h

    def getH(self):
        return self.h

    def setF(self, f):
        self.f = f

    def getF(self):
        return self.f

    def setGoal(self):
        self.isGoal = True

    def getGoal(self):
        return self.isGoal


LAYOUT = [[1, 1, 1, 1, 1],
          [1, 0, 0, 0, 1],
          [1, 0, 1, 0, 1],
          [1, 0, 1, 0, 1],
          [1, 1, 1, 1, 1]]

LAYOUT = [[1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 1, 1, 0, 1],
          [1, 1, 0, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 1, 1],
          [1, 0, 1, 1, 0, 0, 1],
          [1, 0, 0, 0, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 1]]

LAYOUT = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


class Maze:
    def __init__(self, layout):
        self.maze = []
        for x in range(len(layout)):
            row = []
            for y in range(len(layout[0])):
                tile = Tile(x, y)
                if layout[x][y] == 1:
                    tile.setWall([True])
                row.append(tile)
            self.maze.append(row)

    def getMaze(self):
        return self.maze

    def setCost(self, x_goal, y_goal):
        visited = set()
        goal = self.maze[x_goal][y_goal]
        goal.setGoal()
        queue = [goal]
        goal.setH(0)
        while queue:
            actual = queue.pop(0)
            if actual not in visited:
                visited.add(actual)
                queue.extend(self.checkAdjacentAndSetCost(actual))

    def printCost(self):
        costTable = []
        for x in range(len(self.maze)):
            costRow = []
            for y in range(len(self.maze[x])):
                costRow.append(self.maze[x][y].getH())
            costTable.append(costRow)
        print(numpy.matrix(costTable))

    def checkAdjacentAndSetCost(self, tile):
        adjacent = []
        adjacent.append(self.maze[tile.x+1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y+1])
        adjacent.append(self.maze[tile.x-1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y-1])

        unvisited = []
        for t in adjacent:
            if t.getWall() == [0] and t.getH() == '-':
                t.setH(tile.getH()+random.randint(1, 3))
                unvisited.append(t)
        return unvisited

    def generateDescendants(self, tile):
        adjacent = []
        adjacent.append(self.maze[tile.x+1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y+1])
        adjacent.append(self.maze[tile.x-1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y-1])

        descendants = []
        for t in adjacent:
            if t.getWall() == [0]:
                descendants.append(t)
        return descendants

    def getMinH(self, tiles):
        tileMinH = min(tiles, key=attrgetter('h'))
        return tileMinH.getH()+STEP_COST

    def getTileMinF(self, tiles):
        return min(tiles, key=attrgetter('f'))

    def getTileSecondMinF(self, tiles):
        tileMinF = self.getTileMinF(tiles)
        if len(tiles) > 1:
            return self.getTileMinF(list(set(tiles)-set([tileMinF])))
        else:
            return tileMinF

    def RTAStar(self, x_start, y_start):
        actual = self.maze[x_start][y_start]
        listing = []
        wykaz = []
        descendants = self.generateDescendants(actual)
        actual.setF(self.getMinH(descendants))
        ancestor = None
        iter = 0
        while actual.getGoal() != True:
            iter += 1
            print("\n**** ITERATION", iter, "****")
            print("actual:", (actual.x, actual.y),
                  "h", actual.h, "f", actual.f)
            descendants = self.generateDescendants(actual)
            # descendants_temp = [
            #     x for x in descendants if x not in wykaz]
            # descendants = descendants_temp
            if ancestor in descendants:
                descendants.remove(ancestor)
            # for descendant in descendants:
                # print("desc:", (descendant.x, descendant.y))
            for descendant in descendants:
                descendants_prime = self.generateDescendants(descendant)
                descendants_prime.remove(actual)
                # print("descendant:", (descendant.x, descendant.y),
                #       "h", descendant.h, "f", descendant.f)
                if descendant.h == 0:
                    descendant.h_prime = 0
                    descendant.setF(STEP_COST)
                elif descendants_prime:
                    # for dp in descendants_prime:
                    #     print("descendant_prime:", (dp.x, dp.y))
                    # print("minH_prime", (descendant.x, descendant.y),
                    #       self.getMinH(descendants_prime))
                    descendant.setH(self.getMinH(descendants_prime))
                    descendant.h_prime = self.getMinH(descendants_prime)

                    # print("minF", (descendant.x, descendant.y),
                    #       self.getMinH(descendants_prime)+STEP_COST)
                    descendant.setF(self.getMinH(
                        descendants_prime)+STEP_COST)
                else:
                    descendant.h_prime = actual.h+STEP_COST
            for descendant in descendants:
                descendant.h = descendant.h_prime

            if ancestor and (actual.x, actual.y) not in wykaz:
                # print("ancestorH", (ancestor.x, ancestor.y), ancestor.h)
                ancestor.setF(ancestor.getH()-STEP_COST)
                # print("ancestorF", (ancestor.x, ancestor.y), "f", ancestor.f)
                descendants.append(ancestor)
            for descendant in descendants:
                print("descendant:", (descendant.x, descendant.y),
                      "h", descendant.h, "f", descendant.f)
            tileSecondMinF = self.getTileSecondMinF(descendants)
            # print("tileSecondMinF:", (tileSecondMinF.x, tileSecondMinF.y))
            # for descendant in descendants:
            #     print("descendant:", (descendant.x, descendant.y))
            new = self.getTileMinF(descendants)
            print("new:", (new.x, new.y),
                  "h", new.h, "f", new.f)
            actual.setH(tileSecondMinF.getF())
            listing.append(actual)
            if (actual.x, actual.y) not in wykaz:
                wykaz.append((actual.x, actual.y))
            ancestor = actual
            print("actual:", (actual.x, actual.y),
                  "h", ancestor.h, "f", ancestor.f)

            actual = new

            # for item in listing:
            #     print("listing:", (item.x, item.y))

            self.printCost()

        print("\n****Found goal at", (actual.x, actual.y),  "****")
        listing.append(actual)
        # for item in listing:
        #     print("listing:", (item.x, item.y))
        l = [(item.x, item.y) for item in listing]
        print("\n listing:", l)
        wykaz.append((actual.x, actual.y))
        print("\n wykaz", wykaz)


def display_maze(maze):
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            isWall = maze[x][y].getWall()
            screen_x = -len(maze[0])/2*25 + (y * 25)
            screen_y = len(maze)/2*25 - (x * 25)

            if isWall == [True]:
                wall.goto(screen_x, screen_y)
                wall.stamp()


wall = Wall()

maze = Maze(LAYOUT)
display_maze(maze.getMaze())
maze.setCost(5, 6)
maze.printCost()
maze.RTAStar(1, 9)

# turtle.done()

# Keyboard
# turtle.listen()
# turtle.onkey(player.go_up, "Up")
# turtle.onkey(player.go_down, "Down")
# turtle.onkey(player.go_left, "Left")
# turtle.onkey(player.go_right, "Right")

window.tracer(0)

while True:
    window.update()

    # time.sleep(0)
