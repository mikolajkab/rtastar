import turtle
import random
import numpy
import ast
import argparse

from operator import attrgetter

STEP_COST = 3


def windowSetup():
    window = turtle.Screen()
    window.bgcolor("black")
    window.title(
        "Przeszukiwanie RTA*. Problem „przejścia przez labirynt”")
    window.screensize()
    window.setup(width=1.0, height=0.95)


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


class Vertex:
    def __init__(self, vertexId, x, y, label):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        self.isGoal = False


class Edge:
    def __init__(self, v1, v2, weight=3):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


class Node(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.fillcolor(0, 0, 0)
        self.shape("circle")
        self.penup()
        self.speed(0)

    def draw(self, x, y, label, color, position):
        self.goto(x, y)
        self.color(color)
        self.stamp()
        self.goto(x+position, y+10)
        self.write(label, "left", font=("Arial", 16, "bold"))


class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.penup()
        self.speed(0)


class Line(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("white")
        self.penup()
        self.speed(0)

    def draw(self, _x1, _y1, _x2, _y2):
        x1 = float(_x1)
        y1 = float(_y1)
        x2 = float(_x2)
        y2 = float(_y2)
        self.penup()
        self.goto(x1, y1)
        self.pendown()
        self.goto(x2, y2)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        self.penup()
        self.goto(x, y)
        self.write(str(STEP_COST), align="right",
                   font=("Arial", 14, "normal"))


LAYOUT1 = [[1, 1, 1, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 1, 0, 1],
           [1, 0, 0, 0, 1],
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

LAYOUT4 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

LAYOUT5 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
           [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


class App:
    def __init__(self, layout, wall, node, line):
        self.wall = wall
        self.node = node
        self.line = line
        self.maze = []
        id = 0
        for x in range(len(layout)):
            row = []
            for y in range(len(layout[0])):
                tile = Tile(x, y)
                id += 1
                tile.id = id
                if layout[x][y] == 1:
                    tile.isWall = [True]
                row.append(tile)
            self.maze.append(row)

    def setCost(self, x_goal, y_goal):
        visited = set()
        goal = self.maze[x_goal][y_goal]
        goal.isGoal = True
        queue = [goal]
        goal.h = 0
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
                costRow.append(self.maze[x][y].h)
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
            if t.isWall == [0] and t.h == '-':
                t.h = tile.h+random.randint(1, 3)
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
            if t.isWall == [0]:
                descendants.append(t)
        return descendants

    def getMinH(self, tiles):
        tileMinH = min(tiles, key=attrgetter('h'))
        return tileMinH.h+STEP_COST

    def getTileMinF(self, tiles):
        return min(tiles, key=attrgetter('f'))

    def getTileSecondMinF(self, tiles):
        tileMinF = self.getTileMinF(tiles)
        if len(tiles) > 1:
            return self.getTileMinF(list(set(tiles)-set([tileMinF])))
        else:
            return tileMinF

    def getScreenX(self, tile):
        return -len(self.maze[0])*50 + (tile.y * 100) + 300

    def getScreenY(self, tile):
        return len(self.maze)*50 - (tile.x * 100) - 50

    def RTAStar(self, x_start, y_start):
        actual = self.maze[x_start][y_start]
        self.markTile(actual, "green")
        self.node.draw(self.getScreenX(actual),
                       self.getScreenY(actual), actual.h, "green", -20)
        self.wall.speed(5)
        self.node.speed(5)

        listing = set()
        wykaz = []
        descendants = self.generateDescendants(actual)
        actual.f = self.getMinH(descendants)
        ancestor = None
        iter = 0
        while actual.isGoal != True:
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
                    descendant.f = STEP_COST
                elif descendants_prime:
                    # for dp in descendants_prime:
                    #     print("descendant_prime:", (dp.x, dp.y))
                    # print("minH_prime", (descendant.x, descendant.y),
                    #       self.getMinH(descendants_prime))
                    descendant.h = self.getMinH(descendants_prime)
                    descendant.h_prime = self.getMinH(descendants_prime)

                    # print("minF", (descendant.x, descendant.y),
                    #       self.getMinH(descendants_prime)+STEP_COST)
                    descendant.f = self.getMinH(descendants_prime)+STEP_COST
                else:
                    descendant.h_prime = actual.h+STEP_COST
                    descendant.f = descendant.h_prime+STEP_COST
            for descendant in descendants:
                descendant.h = descendant.h_prime
                self.node.draw(self.getScreenX(descendant),
                               self.getScreenY(descendant), descendant.h, "yellow", 10)
                listing.add(descendant)

            if ancestor and (actual.x, actual.y) not in wykaz:
                # print("ancestorH", (ancestor.x, ancestor.y), ancestor.h)
                ancestor.f = ancestor.h+STEP_COST
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
            actual.h = tileSecondMinF.f
            if (actual.x, actual.y) not in wykaz:
                wykaz.append((actual.x, actual.y))
            listing.add(actual)
            ancestor = actual
            print("actual (updated):", (actual.x, actual.y),
                  "h", actual.h, "f", actual.f)

            actual = new

            # for item in listing:
            #     print("listing:", (item.x, item.y))
            self.markTile(actual, "blue")
            self.node.draw(self.getScreenX(actual),
                           self.getScreenY(actual), actual.h, "blue", 10)
            print("cost so far:", STEP_COST*iter)
            print("actualized cost h:")
            self.printCost()

        print("\n****Found goal at", (actual.x, actual.y),  "****")
        self.markTile(actual, "red")
        self.node.draw(self.getScreenX(actual),
                       self.getScreenY(actual), actual.h, "red", 10)
        l = [(item.x, item.y) for item in listing]
        print("\n listing:", l)
        print("length(listing):", len(listing))

        wykaz.append((actual.x, actual.y))
        print("\n wykaz", wykaz)
        print("length(wykaz):", len(wykaz))

    def markTile(self, tile, color):
        screen_x = -len(self.maze[0])/2*25 + (tile.y * 25) - 500
        screen_y = len(self.maze)/2*25 - (tile.x * 25) - 50
        self.wall.goto(screen_x, screen_y)
        self.wall.color(color)
        self.wall.stamp()

    def displayMaze(self):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y].isWall == [True]:
                    self.markTile(self.maze[x][y], "white")
                if self.maze[x][y].isGoal == True:
                    self.markTile(self.maze[x][y], "red")

    def displayGraph(self):
        vertexDict = {}
        edgeList = []
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                tile = self.maze[x][y]
                if tile.isWall != [True]:
                    screen_x = self.getScreenX(tile)
                    screen_y = self.getScreenY(tile)
                    v = Vertex(tile.id, screen_x, screen_y, tile.h)
                    v.isGoal = tile.isGoal
                    vertexDict[tile.id] = v

                    adjacent = self.generateDescendants(tile)
                    for a in adjacent:
                        if a.id > tile.id:
                            edge = Edge(a.id, tile.id)
                            edgeList.append(edge)

        for vertexId in vertexDict:
            vertex = vertexDict[vertexId]
            if vertex.isGoal:
                color = "red"
            else:
                color = "white"
            self.node.draw(vertex.x, vertex.y, vertex.label, color, -20)

        for edge in edgeList:
            self.line.draw(vertexDict[edge.v1].x, vertexDict[edge.v1].y,
                           vertexDict[edge.v2].x, vertexDict[edge.v2].y)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-demo')
    args = parser.parse_args()

    if args.demo == "1":
        layout = LAYOUT1
        x_goal, y_goal = 1, 1
        x_start, y_start = 3, 3
    elif args.demo == "2":
        layout = LAYOUT2
        x_goal, y_goal = 1, 1
        x_start, y_start = 4, 5
    elif args.demo == "3":
        layout = LAYOUT3
        x_goal, y_goal = 9, 2
        x_start, y_start = 2, 9
    elif args.demo == "4":
        layout = LAYOUT4
        x_goal, y_goal = 9, 5
        x_start, y_start = 1, 9
    elif args.demo == "5":
        layout = LAYOUT5
        x_goal, y_goal = 1, 2
        x_start, y_start = 1, 9
    else:
        print("Przeszukiwanie RTA*. Problem przejscia przez labirynt.")
        raw_layout = input("""Podaj dwu wymiarowa liste m x n okreslajaca labirynt, gdzie:
        0 - wolne pole, 1 - sciana, a labirynt jest otoczony przez sciany. Pryklad:
        [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]\n""")
        x_goal, y_goal = [int(x) for x in input(
            "Podaj CEL jako wspolrzedne x i y gdzie x - rzad, y - kolumna, lewy gorny rog to 0,0. Przyklad: 1,1\n").split(",")]
        x_start, y_start = [int(x) for x in input(
            "Podaj START jako wspolrzedne x i y gdzie x - rzad, y - kolumna, lewy gorny rog to 0,0. Przyklad: 3,3\n").split(",")]

        layout = ast.literal_eval(raw_layout)

    windowSetup()
    wall = Wall()
    node = Node()
    line = Line()
    maze = App(layout, wall, node, line)
    maze.setCost(x_goal, y_goal)
    maze.displayMaze()
    maze.displayGraph()
    maze.RTAStar(x_start, y_start)
    turtle.done()


if __name__ == "__main__":
    main()
