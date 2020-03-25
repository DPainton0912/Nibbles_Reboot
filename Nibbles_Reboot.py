#Python Nibbles Reboot
import time
import math
import random
import pygame
import Leaderboard
pygame.init()
size = 500
rows = 20
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
win = pygame.display.set_mode((size, size))
win.fill((157, 107, 72))
pygame.display.set_caption("Nibbles Reboot")

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(78, 41, 15)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (black), circleMiddle, radius)
            pygame.draw.circle(surface, (black), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dirnx != 1:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    if self.dirnx != -1:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    if self.dirny != 1:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    if self.dirny != -1: 
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (black), (x,0),(x,w))
        pygame.draw.line(surface, (black), (0,y),(w,y))

def redrawWindow(surface, s, snack):
    surface.fill((157, 107, 72))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(size, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    x = float(random.randint(1, rows-2))
    y = float(random.randint(1, rows-2))
    return(x, y)
    # positions = item.body
    # while True:
    #     x = random.randrange(rows)
    #     y = random.randrange(rows)
    #     if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
    #         continue
    #     else:
    #         break
    # return (x,y)

def main():
    s = snake((78, 41, 15), (10,10))
    s.reset((10,10))
    snack = cube(randomSnack(rows, s), color=(red))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(125)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(red))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                gameEnd(s)
                flag = False 
        snakeHeadX, snakeHeadY = s.body[0].pos
        if s.dirnx != 1 and snakeHeadX == 19:
            gameEnd(s)
            flag = False
        if s.dirnx != -1 and snakeHeadX == 0:
            gameEnd(s)
            flag = False
        if s.dirny != 1 and snakeHeadY == 19:
            gameEnd(s)
            flag = False
        if s.dirny != -1 and snakeHeadY == 0:
            gameEnd(s)
            flag = False
        redrawWindow(win, s, snack)

def gameStart():
    startGame = True
    clock = pygame.time.Clock()
    h = Leaderboard.Leaderboard("Bob")
    leaderboard = h.ReadFile()
    h.ShowLeaderboard(leaderboard)
    while startGame:
        pygame.time.delay(125)
        clock.tick(10)
        pygame.font.init()
        gameStartFont = pygame.font.Font('freesansbold.ttf', 50)
        nibblesRebootSurf = gameStartFont.render('Nibbles Reboot', True, white)
        playSurf = gameStartFont.render('Press space to play', True, white)
        win.blit(nibblesRebootSurf,
            (size // 8, size // 2.5))
        win.blit(playSurf,
            (size // 35, size // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startGame = False
    if startGame == False:
        main()

def gameEnd(s):
    endGame = True
    score = str(len(s.body)-1)
    playername = input("Enter your name: ").strip().lower().capitalize()
    h = Leaderboard.Leaderboard(playername)
    leaderboard = h.ReadFile()
    leaderboard = h.NewHighscore(s, leaderboard)
    h.ShowLeaderboard(leaderboard)
    h.WriteFile(leaderboard)
    while endGame:
        win.fill((157, 107, 72))
        pygame.font.init()
        gameEndFont = pygame.font.Font('freesansbold.ttf', 50)
        gameOverSurf = gameEndFont.render('Game Over!', True, white)
        scoreSurf = gameEndFont.render('Score: ' + score, True, white)
        restartSurf = gameEndFont.render('Press space to play', True, white)
        win.blit(gameOverSurf,
            (size // 5, size // 3.75))
        win.blit(scoreSurf,
            (size // 3.5, size // 2.75))
        win.blit(restartSurf,
            (size // 35, size // 2.25))
        pygame.display.update()
        clock = pygame.time.Clock()
        pygame.time.delay(125)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    endGame = False
                    
    if endGame == False:
        main()

gameStart()