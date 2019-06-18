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
window.title("Real-time A* algorithm: maze")
window.setup(MAZE_HEIGHT*300, MAZE_WIDTH*300, 100, 100)
# window.setworldcoordinates(0, 994.80, 1060.80, 0)


class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.penup()
        self.speed(0)

    def setColor(self, color):
        self.color(color)


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isWall = [False]
        self.isGoal = False
        self.h = '-'
        self.h_prime = '-'
        self.f = '-'
        self.id = 0

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


LAYOUT1 = [[1, 1, 1, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 1, 0, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 1, 1]]

LAYOUT2 = [[1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 1, 1, 0, 1],
           [1, 1, 0, 0, 0, 0, 1],
           [1, 0, 0, 1, 0, 1, 1],
           [1, 0, 1, 1, 0, 0, 1],
           [1, 0, 0, 0, 0, 1, 1],
           [1, 1, 1, 1, 1, 1, 1]]

LAYOUT3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
    def __init__(self, layout, wall, node):
        self.wall = wall
        self.node = node
        self.maze = []
        id = 0
        for x in range(len(layout)):
            row = []
            for y in range(len(layout[0])):
                tile = Tile(x, y)
                id += 1
                tile.id = id
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
        self.markTile(actual, "green")
        self.wall.speed(0)
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
            self.markTile(actual, "blue")
            self.printCost()

        print("\n****Found goal at", (actual.x, actual.y),  "****")
        listing.append(actual)
        self.markTile(actual, "red")
        # for item in listing:
        #     print("listing:", (item.x, item.y))
        l = [(item.x, item.y) for item in listing]
        print("\n listing:", l)
        wykaz.append((actual.x, actual.y))
        print("\n wykaz", wykaz)

    def markTile(self, tile, color):
        screen_x = -len(self.maze[0])/2*25 + (tile.y * 25) - 500
        screen_y = len(self.maze)/2*25 - (tile.x * 25)
        self.wall.goto(screen_x, screen_y)
        self.wall.setColor(color)
        self.wall.stamp()

    def display(self):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y].getWall() == [True]:
                    self.markTile(self.maze[x][y], "white")
                if self.maze[x][y].getGoal() == True:
                    self.markTile(self.maze[x][y], "red")

    def display_graph(self):
        vertexDict = {}
        edgeList = []
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                tile = self.maze[x][y]
                if tile.getWall() != [True]:
                    screen_x = -len(self.maze[0])*25 + (tile.y * 50)
                    screen_y = len(self.maze)*25 - (tile.x * 50)
                    v = Vertex(tile.id, screen_x, screen_y, tile.h)
                    vertexDict[tile.id] = v

                    adjacent = self.generateDescendants(tile)
                    for a in adjacent:
                        if a.id > tile.id:
                            edge = Edge(a.id, tile.id)
                            edgeList.append(edge)

        for edge in edgeList:
            x1 = float(vertexDict[edge.v1].x)
            y1 = float(vertexDict[edge.v1].y)
            x2 = float(vertexDict[edge.v2].x)
            y2 = float(vertexDict[edge.v2].y)
            self.node.penup()
            self.node.goto(x1, y1)
            self.node.pendown()
            self.node.goto(x2, y2)
            if edge.weight != 0:
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                self.node.penup()
                self.node.goto(x, y)
                self.node.write(str(edge.weight), align="right",
                                font=("Arial", 12, "normal"))

        for vertexId in vertexDict:
            vertex = vertexDict[vertexId]
            x = vertex.x
            y = vertex.y
            self.node.penup()
            self.node.goto(x, y-10)

            self.node.pendown()
            self.node.fillcolor(0.8, 1, 0.4)
            self.node.begin_fill()
            self.node.circle(10)
            self.node.end_fill()
            self.node.penup()
            self.node.goto(x+2, y+11)
            self.node.write(vertex.label, align="right",
                            font=("Arial", 12, "bold"))


class Node(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("white")
        self.penup()
        self.speed(100)


class Vertex:
    def __init__(self, vertexId, x, y, label):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label


class Edge:
    def __init__(self, v1, v2, weight=3):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


wall = Wall()
node = Node()
maze = Maze(LAYOUT2, wall, node)
maze.setCost(1, 1)
maze.display()
maze.display_graph()
maze.RTAStar(1, 5)

turtle.done()
