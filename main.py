import numpy as np
import pygame as pg

pg.init()

winWidth = 500
winHeight = 500

win = pg.display.set_mode((winWidth, winHeight))
pg.display.set_caption('A*')

run = True
step = 0
preparation = True
algRun = False
animation = False
clock = pg.time.Clock()
found = False

points = []

startPoint = []
endPoint = []
currentPoint = []
openPoints = []
closedPoints = []


class Field:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 0)
        self.fillColor = (255, 255, 255)
        self.isObstacle = False
        self.gCost = 0.0
        self.hCost = 0.0
        self.fCost = 0.0
        self.parentNode = []

    def draw(self, window):
        pg.draw.rect(window, self.color, (self.x, self.y, self.x + 10, self.y + 10), 1)
        pg.draw.rect(window, self.fillColor, (self.x + 1, self.y + 1, self.x + 9, self.y + 9))

    def set_color(self, color):
        self.fillColor = color

    def set_obstacle(self):
        self.set_color((0, 0, 0))
        self.isObstacle = True

    def reset_obstacle(self):
        self.isObstacle = False
        self.set_color((255, 255, 255))

    def calculate_cost(self, startPointF, endPointF):
        if self.x > startPointF.x:
            startDistX = self.x - startPointF.x
        else:
            startDistX = startPointF.x - self.x

        if self.y > startPointF.y:
            startDistY = self.y - startPointF.y
        else:
            startDistY = startPointF.y - self.y

        if self.x > endPointF.x:
            endDistX = self.x - endPointF.x
        else:
            endDistX = endPointF.x - self.x

        if self.y > endPointF.y:
            endDistY = self.y - endPointF.y
        else:
            endDistY = endPointF.y - self.y

        self.gCost = np.sqrt(startDistX ** 2 + startDistY ** 2)
        self.hCost = np.sqrt(endDistX ** 2 + endDistY ** 2)
        self.fCost = self.gCost + self.hCost

    def set_parent_node(self, parent):
        self.parentNode = parent


def update_window():
    for l in points:
        for point in l:
            point.draw(win)
    pg.display.update()


def add_open_points(currentPoint):
    # global openPoints
    # global closedPoints
    nearPoints = [
        # [currentPoint[0] - 1, currentPoint[1] - 1],
        [currentPoint[0], currentPoint[1] - 1],
        # [currentPoint[0] + 1, currentPoint[1] - 1],
        [currentPoint[0] - 1, currentPoint[1]],
        [currentPoint[0] + 1, currentPoint[1]],
        # [currentPoint[0] - 1, currentPoint[1] + 1],
        [currentPoint[0], currentPoint[1] + 1],
        # [currentPoint[0] + 1, currentPoint[1] + 1]
    ]

    for nearPoint in nearPoints:
        if 0 <= nearPoint[0] <= 49 and 0 <= nearPoint[1] <= 49:
            if not (nearPoint in openPoints) and not (nearPoint in closedPoints) and \
                    not points[nearPoint[0]][nearPoint[1]].isObstacle:
                openPoints.append(nearPoint)
                points[nearPoint[0]][nearPoint[1]].calculate_cost(points[startPoint[0]][startPoint[1]],
                                                                  points[endPoint[0]][endPoint[1]])
                points[nearPoint[0]][nearPoint[1]].set_parent_node(currentPoint)
                if nearPoint != startPoint and nearPoint != endPoint:
                    points[nearPoint[0]][nearPoint[1]].set_color((0, 255, 0))


# Create table of points

for i in range(0, winWidth, 10):
    line = []
    for j in range(0, winHeight, 10):
        line.append(Field(i, j))
    points.append(line)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            print('Window closed')

    # Mouse functions handling
    mouseButtons = pg.mouse.get_pressed()
    mousePos = pg.mouse.get_pos()
    mouseX = mousePos[0] // 10
    mouseY = mousePos[1] // 10

    # Prepare the map
    if preparation:

        # get start point
        if step == 0 and mouseButtons[0]:
            startPoint = [mouseX, mouseY]
            points[mouseX][mouseY].set_color((255, 102, 0))
        # get end point
        if len(startPoint) == 2:
            if step == 1 and mouseButtons[0] and not (startPoint[0] == mouseX and startPoint[1] == mouseY):
                endPoint = [mouseX, mouseY]
                points[mouseX][mouseY].set_color((0, 0, 255))
        # get obstacle points
        if len(startPoint) == 2 and len(endPoint) == 2:
            if step == 2 and mouseButtons[0] and not (
                    startPoint[0] == mouseX and startPoint[1] == mouseY) and not (
                    endPoint[0] == mouseX and endPoint[1] == mouseY):
                points[mouseX][mouseY].set_obstacle()
        # delete obstacle
        if mouseButtons[2] and points[mouseX][mouseY].isObstacle:
            points[mouseX][mouseY].reset_obstacle()

    # Run the algorithm
    if algRun:

        currentPoint = startPoint.copy()
        add_open_points(currentPoint)
        closedPoints.append(currentPoint)
        points[currentPoint[0]][currentPoint[1]].calculate_cost(points[startPoint[0]][startPoint[1]],
                                                                points[endPoint[0]][endPoint[1]])
        while currentPoint != endPoint and len(openPoints) > 0 and algRun:
            if animation:
                clock.tick(60)
                update_window()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    algRun = False
                    run = False
                    print('')

            # pick new current point
            currentPoint = openPoints[0]
            for point in openPoints:
                if points[point[0]][point[1]].fCost < points[currentPoint[0]][currentPoint[1]].fCost:
                    currentPoint = point.copy()

            # add new open points
            add_open_points(currentPoint)

            # move current point to closed points form open points
            if currentPoint != startPoint and currentPoint != endPoint:
                points[currentPoint[0]][currentPoint[1]].set_color((255, 0, 0))
            closedPoints.append(openPoints.pop(openPoints.index(currentPoint)))

            if len(openPoints) == 0:
                algRun = False
                found = False
                print("Path doesn't exist")

            if currentPoint == endPoint:
                algRun = False
                found = True

        if found:
            path = [closedPoints.pop(-1)]
            while path[-1] != startPoint:
                parentNode = points[path[-1][0]][path[-1][1]].parentNode
                if parentNode != startPoint:
                    points[parentNode[0]][parentNode[1]].set_color((127, 0, 127))
                path.append(parentNode)

    # control program phases
    keys = pg.key.get_pressed()
    if len(startPoint) == 2:
        step = 1
    if len(endPoint) == 2:
        step = 2
    if step == 2 and keys[pg.K_SPACE]:
        step = 3
        preparation = False
        algRun = True
        animation = False
    if step == 2 and keys[pg.K_RETURN]:
        step = 3
        preparation = False
        algRun = True
        animation = True
    update_window()

pg.quit()
