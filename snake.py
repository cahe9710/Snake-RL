import pygame
import sys
import random
import numpy as np

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0
        self.powerup = False

    def get_head_position(self):
        return self.positions[0]

    def get_body_position(self):
        return self.positions

    def remove_powerup(self):

        self.powerup = False

    def add_powerup(self):

        self.powerup = True

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
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
        self.position = None #(0,0)
        self.color = (223, 163, 49)
        self.all_pos = all_pos 
        self.randomize_position(snake_pos)

        
    def randomize_position(self, snake_pos, posion_pos = None, powerup_pos= None ):
        

        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, posion_pos, powerup_pos] ]
        random.shuffle(available_pos)
        
        self.position = available_pos.pop()
        
                  

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def get_food_position(self):
        return self.position

class BadFood():
    def __init__(self, all_pos, snake_pos , food_pos):
        self.position = None
        self.color = (100, 100, 20)
        self.all_pos = all_pos
        self.randomize_position(snake_pos, food_pos)

    def randomize_position(self, snake_pos, food_pos, powerup_pos = None):
        
        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, food_pos, powerup_pos] ]
        random.shuffle(available_pos)
        self.position = available_pos.pop()

    def draw(self, surface):
        if not(self.position == None):
            r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def get_bad_food_position(self):
        return self.position

class PowerUp():
    def __init__(self, all_pos, snake_pos, food_pos = None, badfood_pos = None):
        self.position = None
        self.color = (255, 192, 203)
        self.all_pos = all_pos
        self.randomize_position(snake_pos, food_pos, badfood_pos)
        
        
    def randomize_position(self, snake_pos, food_pos = None , poison_pos = None):
        available_pos = [x for x in self.all_pos if x not in [ *snake_pos, food_pos, poison_pos] ]
        random.shuffle(available_pos)
        self.position = available_pos.pop()
        
    def get_powerup_position(self):
        return self.position

    def draw(self, surface):
        if not(self.position == None):
            r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
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

screen_width = 480
screen_height = 480

gridsize = 48
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():

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
    badfood = BadFood(all_pos, snake.get_body_position(), food.get_food_position())
    powerup = PowerUp(all_pos,snake.get_body_position(), food.get_food_position(), badfood.get_bad_food_position())
    
    

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        time += 1
        clock.tick(5)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position(snake.get_body_position())
        
        if snake.get_head_position() == powerup.position:
            snake.add_powerup()
            powerup.randomize_position(snake.get_body_position(), food.get_food_position(), badfood.get_bad_food_position())
 
        
        if snake.get_head_position() == badfood.position:
            if snake.powerup: 
                 snake.remove_powerup()
                 snake.length += 1
                 snake.score += 1
                 badfood.randomize_position(snake.get_body_position(), food.get_food_position(), powerup.get_powerup_position())
            else:
                snake.reset()

        if time % 100 == 0:
            badfood.randomize_position(snake.get_body_position(), food.get_food_position())
        if time % 200 == 0:
            powerup.randomize_position(snake.get_body_position(), food.get_food_position(), badfood.get_bad_food_position())
        snake.draw(surface)
        food.draw(surface)

        badfood.draw(surface)
        
        powerup.draw(surface)
        
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()

main()