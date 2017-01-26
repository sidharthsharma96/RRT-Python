import math, sys, pygame, random
from math import *
from pygame import *

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 10.0
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 20000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,180,105
first = True
count = 3
rectObs = []

def dist(p1,p2):    #distance between two points
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def step_from_to(p1,p2):
    if dist(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def collides(p):    
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True
    return False


def get_random_clear():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        noCollision = collides(p)
        if noCollision == False:
            return p


def init_obstacles():  
    global rectObs
    rectObs = []
    rectObs.append(pygame.Rect((XDIM / 2.0 + 200, YDIM / 2.0 - 180),(100,370)))
    rectObs.append(pygame.Rect((370,100),(150,160)))
    rectObs.append(pygame.Rect((400,300),(100,80)))
    rectObs.append(pygame.Rect((250,180),(80,120)))
    rectObs.append(pygame.Rect((100,100),(80,80)))
    for rect in rectObs:
        pygame.draw.rect(screen, cyan, rect)


def reset():
    global count
    screen.fill(white)
    init_obstacles()
    count = 0

def main():
    global count
    
    initialPoint = Node(None, None)
    goalPoint = Node(None, None)
    currentState = 'init'
    first = True
    nodes = []
    reset()

    while True:

        #Initial point and Goal point specified
        initialPoint = Node((23,475), None)
        goalPoint = Node((694, 104),None)
        
        nodes.append(initialPoint) # Start in the center
        pygame.draw.circle(screen, red, initialPoint.point, GOAL_RADIUS)
        pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
        if(first == True):
            currentState = 'buildTree'
            first = False


        if currentState == 'goalFound':
            currNode = goalNode.parent
            pygame.display.set_caption('Goal Reached')
            while currNode.parent != None:
                pygame.draw.line(screen,red,currNode.point,currNode.parent.point)
                currNode = currNode.parent
        elif currentState == 'buildTree':
            count = count+1
            pygame.display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point,rand) <= dist(parentNode.point,rand):
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True

                newnode = step_from_to(parentNode.point,rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen,black,parentNode.point,newnode)

                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    currentState = 'goalFound'
                    goalNode = nodes[len(nodes)-1]

                
            else:
                print("Ran out of nodes... :(")
                return;
        pygame.display.update()
        fpsClock.tick(10000)



if __name__ == '__main__':
    main()