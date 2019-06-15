import turtle
import time
import random
import numpy
from operator import attrgetter


MAZE_HEIGHT = 8
MAZE_WIDTH = 8

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

    def setWall(self, wall):
        self.isWall = wall

    def getWall(self):
        return self.isWall

    def setH(self, h):
        self.h = h

    def getH(self):
        return self.h

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
                t.setH(tile.getH()+random.randint(1, 2))
                unvisited.append(t)
        return unvisited

    def minimin(self, tile):
        adjacent = []
        adjacent.append(self.maze[tile.x+1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y+1])
        adjacent.append(self.maze[tile.x-1][tile.y])
        adjacent.append(self.maze[tile.x][tile.y-1])

        successors = []
        for t in adjacent:
            if t.getWall() == [0]:
                successors.append(t)
        tileMinH = min(successors, key=attrgetter('h'))
        print(tileMinH.x, tileMinH.y)

    def RTAStar(self, x_start, y_start):
        listing = set()
        actual = self.maze[x_start][y_start]
        if actual.getGoal() == True:
            return actual
        else:
            self.minimin(actual)


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
maze.setCost(1, 1)
maze.printCost()
maze.RTAStar(3, 4)

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
