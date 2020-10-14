import pygame
import sys
import random
import numpy as np

class Snake():
    def __init__(self):
        self.length = 1
        self.pos = [((screen_width/2), (screen_height/2))]
        self.dir = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0
        self.immunity = False
        self.suicide = False

    def get_head_position(self):
        return self.pos[0]

    def get_body_position(self):
        return self.pos

    def remove_immunity(self):

        self.immunity = False

    def add_immunity(self):

        self.immunity = True

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.dir:
            return
        else:
            self.dir = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.dir
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.pos) > 2 and new in self.pos[2:]:
            self.suicide = True
        else:
            self.pos.insert(0,new)
            if len(self.pos) > self.length:
                self.pos.pop()

    def reset(self):
        self.length = 1
        self.pos = [((screen_width/2), (screen_height/2))]
        self.dir = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.pos:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self, all_pos, snake_pos):
        self.pos = None #(0,0)
        self.color = (223, 163, 49)
        self.all_pos = all_pos 
        self.randomize_position(snake_pos)

        
    def randomize_position(self, snake_pos, posion_pos = None, immunity_pos= None ):
        

        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, posion_pos, immunity_pos] ]
        random.shuffle(available_pos)
        
        self.pos = available_pos.pop()
        
                  

    def draw(self, surface):
        r = pygame.Rect((self.pos[0], self.pos[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def get_position(self):
        return self.pos

class Poison():
    def __init__(self, all_pos, snake_pos , food_pos):
        self.pos = None
        self.color = (100, 100, 20)
        self.all_pos = all_pos
        self.randomize_position(snake_pos, food_pos)

    def randomize_position(self, snake_pos, food_pos, powerup_pos = None):
        
        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, food_pos, powerup_pos] ]
        random.shuffle(available_pos)
        self.pos = available_pos.pop()

    def draw(self, surface):
        if not(self.pos == None):
            r = pygame.Rect((self.pos[0], self.pos[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def get_position(self):
        return self.pos

class Immunity():
    def __init__(self, all_pos, snake_pos, food_pos = None, badfood_pos = None):
        self.pos = None
        self.color = (255, 192, 203)
        self.all_pos = all_pos
        self.randomize_position(snake_pos, food_pos, badfood_pos)
        
        
    def randomize_position(self, snake_pos, food_pos = None , poison_pos = None):
        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, food_pos, poison_pos] ]
        random.shuffle(available_pos)
        self.pos = available_pos.pop()
        
    def get_position(self):
        return self.pos

    def draw(self, surface):
        if not(self.pos == None):
            r = pygame.Rect((self.pos[0], self.pos[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

def run_game():

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    time = 0

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)
    
    #create list containing all coordinates
    all_pos = []
    for i in range(10):
        for j in range(10):
            all_pos.append((i*gridsize,j*gridsize))

    snake = Snake()
    food = Food(all_pos,snake.get_body_position())
    poison = Poison(all_pos, snake.get_body_position(), food.get_position())
    immunity = Immunity(all_pos,snake.get_body_position(), food.get_position(), poison.get_position())
    
    

    myfont = pygame.font.SysFont("monospace",16)
    
    terminal = False
    
    while (not terminal):
        time += 1
        clock.tick(5)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.get_position():
            snake.length += 1
            snake.score += 1
            food.randomize_position(snake.get_body_position(), poison.get_position(), immunity.get_position())
        
        if snake.suicide:
            terminal = True
            return snake.score
        
        if snake.get_head_position() == immunity.get_position():
            snake.add_immunity()
            immunity.randomize_position(snake.get_body_position(), food.get_position(), poison.get_position())
 
        
        if snake.get_head_position() == poison.get_position():
            if snake.immunity: 
                 snake.remove_immunity()
                 snake.length += 1
                 snake.score += 5
                 poison.randomize_position(snake.get_body_position(), food.get_position(), immunity.get_position())
            else:
                terminal = True
                return snake.score
        if time % 100 == 0:
            poison.randomize_position(snake.get_body_position(), food.get_position(), immunity.get_position())
        if time % 200 == 0:
            immunity.randomize_position(snake.get_body_position(), food.get_position(), poison.get_position())
        snake.draw(surface)
        food.draw(surface)

        poison.draw(surface)
        
        immunity.draw(surface)
        
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()
        


screen_width = 480
screen_height = 480

gridsize = 48
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

for i  in range(5):
    score = run_game()
    print(score)
