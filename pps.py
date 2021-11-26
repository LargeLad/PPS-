import numpy as np
import pygame
import math
import random
import matplotlib.pyplot as plt

pygame.init()

WIDTH = 1050
HEIGHT = 750
FPS = 30
CELLS = 700
CELLSIZE = 5
BASECOLOUR = (0, 0, 0)
RADIUS = 25
ELEMENTS = random.randint(3,7)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("poop fart")

font = pygame.font.Font('freesansbold.ttf', 17)
font2 = pygame.font.Font('freesansbold.ttf', 32)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.textsave = ''
        self.hasText = False
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    # checks whether a inputbox has been clicked
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.textsave = self.text
                    self.hasText = True
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)
                print(self.text)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    # draws textbox to screen
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class UserInterface:
    def __init__(self, rule_set):
        self.x = WIDTH-300
        self.color1 = (150, 150, 150)
        self.color2 = (100, 100, 100)

        self.elementX, self.elementY = WIDTH-285, 10
        self.statusX, self.statusY = WIDTH - 285, 40
        self.ruleX, self.ruleY = WIDTH - 285, 70
        self.pauseX, self.pauseY = 0, 0
        self.NewX, self.NewY = WIDTH-285, 440

        self.button_resetX, self.button_resetY = WIDTH - 285, 160
        self.button_pauseX, self.button_pauseY = WIDTH - 285, 200
        self.button_copyX, self.button_copyY = WIDTH - 285, 240
        self.Num_elementX, self.Num_elementY = WIDTH - 285, 310
        self.Num_ParticlesX, self.Num_ParticlesY = WIDTH - 285, 370

        self.ruleset = rule_set

        self.reset = False
        self.pause = False
        self.copy = False
        self.button_clear_hover = False
        self.new = False

    # draws all the buttons and stuff
    def draw(self, step, paused):
        pygame.draw.rect(WIN, self.color1, (self.x, 0, 300, HEIGHT))
        #pygame.draw.rect(WIN, self.color2, (self.x, 0, 5, HEIGHT))
        pygame.draw.rect(WIN, self.color2, (self.button_resetX-5, self.button_resetY-5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.button_pauseX - 5, self.button_pauseY - 5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.button_copyX - 5, self.button_copyY - 5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.NewX - 5, self.NewY - 5, 90, 30))

        elements = font.render("Number of Elements: " + str(ELEMENTS), True, (0, 0, 0))
        particles = font.render("Number of Particles: " + str(CELLS), True, (0, 0, 0))
        button_clear = font.render("Reset", True, (0, 0, 0))
        button_pause = font.render("Pause", True, (0, 0, 0))
        button_copy = font.render("Copy", True, (0, 0, 0))
        Num_element = font.render("Number of Elements: ", True, (0, 0, 0))
        Num_Particles = font.render("Number of Particles: ", True, (0, 0, 0))
        New = font.render("New", True, (0,0,0))

        if paused:
            pause = font2.render("Paused", True, (75, 75, 200))
        else:
            pause = font2.render("", True, (75, 75, 200))

        WIN.blit(elements, (self.elementX, self.elementY))
        WIN.blit(particles, (self.statusX, self.statusY))

        WIN.blit(pause, (self.pauseX, self.pauseY))
        WIN.blit(button_clear, (self.button_resetX, self.button_resetY))
        WIN.blit(button_pause, (self.button_pauseX, self.button_pauseY))
        WIN.blit(button_copy, (self.button_copyX, self.button_copyY))
        WIN.blit(Num_element, (self.Num_elementX, self.Num_elementY))
        WIN.blit(Num_Particles, (self.Num_ParticlesX, self.Num_ParticlesY))
        WIN.blit(New, (self.NewX, self.NewY))
        # [0, 0, 1, 1, 0, 0, 2, 0, 1]

    # checks to see if a button has been clicked
    def button_press(self, x, y):
        if (x > self.button_resetX-5) and (x < self.button_resetX+85):
            if (y > self.button_resetY-5) and (y < self.button_resetY+25):
                self.reset = True

        if (x > self.button_pauseX-5) and (x < self.button_pauseX+85):
            if (y > self.button_pauseY-5) and (y < self.button_pauseY+25):
                if self.pause == True:
                    self.pause = False
                else:
                    self.pause =  True

        if (x > self.button_copyX-5) and (x < self.button_copyX+85):
            if (y > self.button_copyY-5) and (y < self.button_copyY+25):
                self.copy = True

        if (x > self.NewX-5) and (x < self.NewX+85):
            if (y > self.NewY-5) and (y < self.NewY+25):
                self.new = True


class Element():
    def __init__(self, num, color,alpha,beta):
        self.num = num
        self.color = (0,0,0)
        self.alpha = 0
        self.beta = 0
        self.numInf = 0
        self.InfVal = []
        self.attraction_maps_x = []
        self.attraction_maps_y = []
        self.friction = random.randint(12,50)/10

    def colorSet(self):
        self.color = (random.randint(75,150),random.randint(75,150),random.randint(75,150))
        #self.color = (255,255,255)
        print(self.color)

    def alphaSet(self):
        #self.alpha = random.randint(170,180)
        self.alpha = 180

    def betaSet(self):
        #self.beta = random.randint(20,40)
        self.beta = 25

    def numInfSet(self):
        #self.numInf = float(random.randint(5,10)/10)
        self.numInf=random.randint(10,20)/10
        print(self.numInf)

    def InfSet(self):
        for i in range(0, ELEMENTS):
            self.InfVal.append(random.randint(-5,40)/20)

    def getInf(self, i):
        return self.InfVal[i]

    def attraction_maps_set(self, num,radius):
        for i in range(num):
            tempx,tempy = line_func(radius,5,2)
            self.attraction_maps_x.append(tempx)
            self.attraction_maps_y.append(tempy)

    def getFriction(self):
        return self.friction


class Cell():
    def __init__(self, x, y, velocity, num, element):
        # x is x position, y is y position, alpha is current angle, beta is change angle, velocity is change magnitude
        self.x = x
        self.y = y
        self.velocity = velocity
        self.num = num
        self.pic = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
        self.color = BASECOLOUR
        self.inf = 0
        self.leftRight = 0
        self.angle = 0
        self.colortype = random.randint(1,3)
        self.element = element
        self.yVec = 0
        self.xVec = 0

    def update(self,elements):

        if 0 < self.x + math.cos(self.angle) and self.x + math.cos(self.angle) < WIDTH-10:
            self.x += self.xVec
        else:
            self.loopx()
        if 0 < self.y + math.sin(self.angle) and self.y + math.sin(self.angle) < HEIGHT-10:
            self.y += self.yVec
        else:
            self.loopy()

        self.yVec = friction(self.yVec,elements,self.element)
        self.xVec = friction(self.xVec,elements,self.element)

        self.pic = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)

    def getNum(self):
        return self.num

    def colour(self):
        return self.color

    def changeColour(self, color):
        self.color = (colorval(self.inf) * color[0], colorval(self.inf) * color[1], colorval(self.inf) * color[2])

    def loopx(self):
        if self.x > 100:
            self.x = 12
        else:
            self.x = WIDTH -12

    def loopy(self):
        if self.y > 100:
            self.y = 12
        else:
            self.y = HEIGHT -12

    def addInfluence(self):
        self.inf+=1

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def friction(vector,elements,elementNum):
    frictionVal = elements[elementNum].friction
    #if abs(vector) >10:
    #    vector = 10
    return vector/frictionVal


#creates graphs which map out a particles attraction to other particles, every particle will have an attraction map to every other particle
def line_func(radius, amplitude, num=None):
    points = []
    lines = []
    x = []
    y = []
    if num is None:
            num = random.randint(5, 10)

    y.append(-10)
    x.append(0)
    y.append(0)
    x.append(CELLSIZE*2)
    temp_x = CELLSIZE*2
    points.append([x[len(x)-1], y[len(y)-1]])

    n = 1

    for i in range(0, n):
        y.append(random.randint(-amplitude, amplitude)*(1 - (i/num)))
        a = random.randint(temp_x,RADIUS)
        x.append(a)
        temp_x = a
        points.append([x[len(x)-1], y[len(y)-1]])

    points.append([radius,random.randint(-amplitude, amplitude)])
    y.append(0)
    x.append(radius)
    points.append([x[len(x)-1], y[len(y) - 1]])
    print(points)
    plt.plot(x, y)
    plt.plot([0, radius], [0, 0])
    #plt.show()

    return x,y


#radius = 100
#amplitude = 20
#num = 4

#for i in range(1):
    #x, y = line_func(radius, amplitude,num)
    #plt.plot(x,y)
    #plt.plot([0,radius], [0,0])
    #plt.show()


def leftright(cell,cell2,radius):
    x1 = (radius+1) * math.cos(180 + cell.angle)
    x2 = radius * math.cos(cell.angle)
    y1 = radius * math.sin(180 + cell.angle)
    y2 = radius * math.sin(cell.angle)

    xA = cell2.x
    yA = cell2.y

    v1 = (x2 - x1, y2 - y1)  # Vector 1
    v2 = (x2 - xA, y2 - yA)  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp > 0:
        return 1 #clockwise
    elif xp < 0:
        return -1 #counter clockwise
    else:
        return 0 #same


def colorval(poopey):
    '''print(poopey)
    if poopey >5:
        return 1
    return (poopey/6)+0.16
    '''
    return 1


def dir(left, right):
    if left-right <1:
        return -1
    else:
        return 1


def sign(num):
    if num > 0:
        return 1
    elif num <0:
        return -1
    else:
        return 0


def collide(bins, radius,bx,by, elements):
    for x in range(bx):
        for y in range(by):
            for cell in bins[x][y]:
                for dx in {-1, 0, 1}:
                    for dy in {-1, 0, 1}:
                        try:
                            for c in bins[x + dx][y + dy]:
                                if cell.num < c.num:
                                    d = math.hypot(cell.x - c.x, cell.y - c.y)
                                    if d < radius:
                                        try:
                                            c.inf+=1
                                            cell.inf+=1
                                            cell.yVec += math.sin(math.atan2((c.y - cell.y), (c.x - cell.x))) * np.interp(d, elements[cell.element].attraction_maps_x[c.element], elements[cell.element].attraction_maps_y[c.element])
                                            cell.xVec += math.cos(math.atan2((cell.y - c.y), (c.x - cell.x))) * np.interp(d, elements[cell.element].attraction_maps_x[c.element], elements[cell.element].attraction_maps_y[c.element])

                                            c.yVec += math.sin(math.atan2((cell.y - c.y), (cell.x - c.x))) * np.interp(d, elements[c.element].attraction_maps_x[cell.element], elements[c.element].attraction_maps_y[cell.element])
                                            c.xVec += math.cos(math.atan2((c.y - cell.y), (cell.x - c.x))) * np.interp(d, elements[c.element].attraction_maps_x[cell.element], elements[c.element].attraction_maps_y[cell.element])
                                            '''
                                            if abs(cell.yVec) >= 7:
                                                cell.yVec = 7*sign(cell.yVec)
                                            if abs(cell.xVec) >= 7:
                                                cell.xVec = 7*sign(cell.xVec)
                                            if abs(c.yVec) >= 7:
                                                c.yVec = 7*sign(c.yVec)
                                            if abs(c.xVec) >= 7:
                                                c.xVec = 7*sign(c.xVec)
                                            '''
                                        except ZeroDivisionError:
                                            continue
                        except IndexError:
                            continue


def updateBins(cells,bxnum,bynum):
    bins = [0] * bxnum
    for x in range(len(bins)):
        bins[x] = [0] * bynum
        for y in range(len(bins[x])):
            bins[x][y] = []
    for cell in cells:
        bx = math.floor(cell.x / 100)
        by = math.floor(cell.y / 100)
        try:
            bins[bx][by].append(cell)
        except IndexError:
            continue
    return bins


# moves and then places the cells on the screen
def update(cells, radius, elements, pause):
    if not pause:
        WIN.fill((0,0.,0))
        for cell in cells:
            cell.update(elements)
            cell.changeColour(elements[cell.element].color)
            cell.inf = 0
            pygame.draw.circle(WIN, cell.colour(), (cell.pic.x, cell.pic.y), CELLSIZE)
        bxnum = 40
        bynum = 20
        bins = updateBins(cells,bxnum,bynum)
        collide(bins, radius,bxnum,bynum, elements)

def setup(cellnum,elementnum):
    cells = []
    elements = []

    for i in range(elementnum):
        element = Element(i,0,random.randint(-180,180),random.randint(-40,40))
        element.colorSet()
        element.alphaSet()
        element.betaSet()
        element.numInfSet()
        element.InfSet()
        element.attraction_maps_set(ELEMENTS,RADIUS)
        elements.append(element)
    for i in range(cellnum):
        cell = Cell(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), 0.1, i, random.randint(0,ELEMENTS-1))
        cells.append(cell)

    return elements, cells

def main():
    clock = pygame.time.Clock()
    run = True
    cells = []
    elements = []
    cellnum = CELLS
    elementnum = ELEMENTS

    ui = UserInterface(11111)

    input_box1 = InputBox(WIDTH-285, 330, 140, 30)
    input_box2 = InputBox(WIDTH - 285, 390, 140, 30)
    input_boxes = [input_box1,input_box2]

    elements, cells = setup(cellnum, elementnum)

    while run:
        x, y = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ui.button_press(x, y)
            for box in input_boxes:
                box.handle_event(event)

        if ui.new:
            if input_box1.text == "":
                elementnum = random.randint(3,7)
            else:
                elementnum = int(input_box1.text)

            if input_box2.text == "":
                cellnum = random.randint(600,800)
            else:
                cellnum = int(input_box2.text)

            print(cellnum)
            print(elementnum)
            print("------------------------------------------")
            elements, cells = setup(cellnum, elementnum)
            ui.new = False

        if ui.reset:
            for cell in cells:
                cell.x = random.randint(10, WIDTH-10)
                cell.y = random.randint(10, HEIGHT-10)
            ui.reset = False

        for box in input_boxes:
            box.update()

        update(cells, RADIUS, elements, ui.pause)
        ui.draw(1,2)

        for box in input_boxes:
            box.draw(WIN)

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
