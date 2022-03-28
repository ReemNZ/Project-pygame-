#The characteristics of this snake is that it moves only horizontal through the wall. When the snake eat a rat, the score increases by 1 point, while it increases by 2 points when the snake eats an apple.

import pygame, sys, random
from pygame import mixer
import pandas as pd

class SNAKE:
    def __init__(self):
        self.body = [pygame.math.Vector2(1,10),pygame.math.Vector2(2,10),pygame.math.Vector2(3,10)]
        self.direction = pygame.math.Vector2(0,0)

        #Head graphics
        self.head_up = pygame.image.load('snake/snake_headup.png').convert_alpha()
        self.headup = pygame.transform.scale(self.head_up, (cellsize,cellsize))
        self.head_down = pygame.image.load('snake/snake_headdown.png').convert_alpha()
        self.headdown = pygame.transform.scale(self.head_down, (cellsize,cellsize))
        self.head_right = pygame.image.load('snake/snake_headright.png').convert_alpha()
        self.headright = pygame.transform.scale(self.head_right, (cellsize,cellsize))
        self.head_left = pygame.image.load('snake/snake_headleft.png').convert_alpha()
        self.headleft = pygame.transform.scale(self.head_left, (cellsize,cellsize))

        #Tail graphics
        self.tail_up = pygame.image.load('snake/tailup.png').convert_alpha()
        self.tailup = pygame.transform.scale(self.tail_up, (cellsize,cellsize))
        self.tail_down = pygame.image.load('snake/taildown.png').convert_alpha()
        self.taildown = pygame.transform.scale(self.tail_down, (cellsize,cellsize))
        self.tail_right = pygame.image.load('snake/tailright.png').convert_alpha()
        self.tailright = pygame.transform.scale(self.tail_right, (cellsize,cellsize))
        self.tail_left = pygame.image.load('snake/tailleft.png').convert_alpha()
        self.tailleft = pygame.transform.scale(self.tail_left, (cellsize,cellsize))

        #Crunch sound
        self.crunch_sound = pygame.mixer.Sound('snake/crunch.wav')
        self.crunch_sound.set_volume(0.1) #Adjust sound from 0 to 1.0

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cellsize)
            y_pos = int(block.y * cellsize)
            snake_rect = pygame.Rect(x_pos, y_pos, cellsize, cellsize)
            if index == (len(self.body)-1):
                screen.blit(self.head, snake_rect)
            elif index == 0:
                screen.blit(self.tail, snake_rect)
            else:
                pygame.draw.ellipse(screen, (189,207,70), snake_rect)
    def move_snake(self): #Mechanism is to remove last block (smallest) and add new block at the beginning (direction)
        body_copy = self.body[1:] # body_copy include only index 0,1. Index 2 will be added.
        body_copy.insert(len(self.body)-1, body_copy[-1] + self.direction) # insert position: position is inserted only from left to right = 3-1 = index 2, value to be inserted
        self.body = body_copy[:]
    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] - self.direction) # insert position: position is inserted only from left to right = 3-1 = index 2, value to be inserted
        self.body = body_copy[:]
    def remove_block(self):
        body_copy = self.body[:]
        body_copy.remove(body_copy[0])
        self.body = body_copy[:]
    def update_head_graphics(self):
        head_relation = self.body[-1] - self.body[-2]
        if head_relation == pygame.math.Vector2(1,0): self.head = self.headright
        elif head_relation == pygame.math.Vector2(-1,0): self.head = self.headleft
        elif head_relation == pygame.math.Vector2(0,-1): self.head = self.headup
        elif head_relation == pygame.math.Vector2(0,1): self.head = self.headdown
    def update_tail_graphics(self):
        tail_relation = self.body[1] - self.body[0]
        if tail_relation == pygame.math.Vector2(1,0): self.tail = self.tailright
        elif tail_relation == pygame.math.Vector2(-1,0): self.tail = self.tailleft
        elif tail_relation == pygame.math.Vector2(0,-1): self.tail = self.tailup
        elif tail_relation == pygame.math.Vector2(0,1): self.tail = self.taildown
    def reset(self):
        self.body = [pygame.math.Vector2(1,10),pygame.math.Vector2(2,10),pygame.math.Vector2(3,10)]

class RAT:
    def __init__(self):  #Initiate the class. #Step 1: defining position
        self.randomize()
    def draw_rat(self): #Step 2: Creating fruit
        fruit_rect = pygame.Rect(int(self.position.x * cellsize), int(self.position.y * cellsize), cellsize, cellsize) #(x.pos, y.pos, w, h) #Draw
        screen.blit(new_rat, fruit_rect)  #Show rat on the random spots.
        #pygame.draw.ellipse(screen, (100,100,140), fruit_rect)
    def randomize(self):
        # Making a 2 dimentional vector
        self.x = random.randint(0, cellnumber - 1)  #position starts from topleft so we subtract 1.
        self.y = random.randint(1, cellnumber)
        self.position = pygame.math.Vector2(self.x, self.y)

class APPLE:
    def __init__(self):  #Initiate the class. #Step 1: defining position
        self.randomize()

    def draw_apple_in(self): #Step 2: Creating fruit
        fruit_rect = pygame.Rect(int(self.position.x * cellsize), int(self.position.y * cellsize), cellsize, cellsize) #(x.pos, y.pos, w, h) #Draw
        screen.blit(new_apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cellnumber - 1)  #position starts from topleft so we subtract 1.
        self.y = random.randint(1, cellnumber)
        self.position = pygame.math.Vector2(self.x, self.y)

class MAIN: # Join both snake and fruit
    def __init__(self):
        self.snake = SNAKE()
        self.rat = RAT()
        self.apple = APPLE()
    def draw_elements(self):
        self.draw_grass_fence()
        self.snake.draw_snake()
        self.score()
        self.rat.draw_rat()
        self.draw_apple_condition()
    def draw_grass_fence(self):
        for col in range(cellnumber):
            for row in range(cellnumber+2):
                grass = pygame.Rect(col*cellsize,row*cellsize,cellsize,cellsize)
                if (row % 2 == 0) and (col % 2 == 0):
                    pygame.draw.rect(screen, (70, 133, 12), grass)
                elif (row % 2 != 0) and (col % 2 != 0):
                    pygame.draw.rect(screen, (48, 107, 3), grass)
        for col in range(cellnumber):
            for row in [0,cellnumber+1]:
                fence1_rect = pygame.Rect(col*cellsize,row*cellsize, cellsize, cellsize) #(x.pos, y.pos, w, h) #Draw
                screen.blit(new_fence, fence1_rect)
    def collision(self):
        if self.rat.position == self.snake.body[-1]: #Rat collision
            self.snake.add_block()
            self.rat.randomize()
            self.snake.crunch_sound.play()
            snake_score.append(1)
        elif (self.apple.position == self.snake.body[-1]): #Apple collision
            self.snake.remove_block()
            self.apple.randomize()
            self.snake.crunch_sound.play()
            snake_score.append(2)

        for block in self.snake.body[:]: # Wall collision
            if (block.x == cellnumber):
                block.x = 0
            elif (block.x == -1):
                block.x = cellnumber

        for block in self.snake.body[1:]: #Randomize apple and rat
            if (block == self.rat.position):
                self.rat.randomize()
            elif (block == self.apple.position):
                self.apple.randomize()
    def death(self):
        if ((self.snake.body[-1] in self.snake.body[:-1]) or (not(1 <= self.snake.body[-1].y < cellnumber+1))) and (self.snake.direction != pygame.math.Vector2(0,0)):
            print(sum(snake_score))
            mixer.music.stop()
            self.game_over()
    def apple_showup_rate(self):
        applelist.append(len(self.snake.body)-3)
        if ((len(self.snake.body)-3) - applelist[-2]) != 0:
            var = random.randint(3,7)
            apple_var.append(var)
            del applelist[:-2]
    def draw_apple_condition(self):
        body = len(self.snake.body) - 3
        if ((body % (apple_var[-1])) == 0) and (body != 0):
            font = pygame.font.SysFont('arial', 40)
            #start_time = time.localtime(time.time()).tm_sec
            start_time = (pygame.time.get_ticks()%60000)/1000
            apple_time.append(start_time)
            counting_time = round(((pygame.time.get_ticks()%60000)/1000)-apple_time[0])
            counting_text = font.render(str(counting_time), 1, (255,220,220))
            counting_rect = counting_text.get_rect(center = ((cellsize*cellnumber) - 40, cellsize))
            if counting_time < 6:
                self.apple.draw_apple_in()
                screen.blit(counting_text, counting_rect)
            else:
                self.apple.randomize()
        else:
            apple_time.clear()
    def score(self):
        score_text = str(sum(snake_score))
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = (cellsize*cellnumber) - 45
        score_y = (cellsize*(cellnumber+2)) - 20
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        rat_rect = new_rat.get_rect(midright = (score_rect.left, score_rect.centery))
        backgroud_rect = pygame.Rect((rat_rect.left)-4, rat_rect.top, (rat_rect.width)+(9+score_rect.width), rat_rect.height)
        pygame.draw.rect(screen, (200,100,90), backgroud_rect)
        pygame.draw.rect(screen, (56,74,12), backgroud_rect, 4)
        screen.blit(score_surface, score_rect)
        screen.blit(new_rat, rat_rect)
    def game_over(self):
        #Maximum score
        score_text = sum(snake_score)
        df= pd.read_csv('snake/maxscore.csv')
        dict = {'score': score_text}
        df = df.append(dict, ignore_index = True)
        max_score = df['score'].max()
        df = df.drop(columns = df.columns[0])
        for ind, i in enumerate(df['score']):
            if i < df['score'].max():
                df = df.drop(df.index[ind])
        df.to_csv('snake/maxscore.csv')
        #Game over screen
        screen.fill((54, 110, 12))
        font1 = pygame.font.SysFont('arial', 40)
        font2 = pygame.font.SysFont('arial', 30)
        line1 = font1.render("Game Over", True, (255,255,255))
        line2 = font2.render("Your score is "+ str(score_text) , True, (255,250,250))
        line3 = font2.render("<Press Space to Restart> OR <Press X to Exit>", True, (255,150,150))
        line4 = font2.render("Maximum score is "+ str(max_score), True, (255,150,150))
        surface1 = line1.get_rect(center = ((cellsize*cellnumber)/2,((cellsize*cellnumber)/2)-105))
        surface2 = line2.get_rect(center = ((cellsize*cellnumber)/2,((cellsize*cellnumber)/2)-15))
        surface3 = line3.get_rect(center = ((cellsize*cellnumber)/2,((cellsize*cellnumber)/2)+65))
        surface4 = line4.get_rect(center = ((cellsize*cellnumber)/2,((cellsize*cellnumber)/2)+105))
        screen.blit(line1, surface1)
        screen.blit(line2, surface2)
        screen.blit(line3, surface3)
        screen.blit(line4, surface4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(1) #Pause screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.snake.reset()
                        self.snake.direction = pygame.math.Vector2(0,0)
                        snake_score.clear()
                        mixer.music.play()
                        waiting = False
                        break
    def action(self): #Call actions
        self.snake.move_snake()
        self.collision()
        self.death()
        self.apple_showup_rate()

##Initiate
pygame.mixer.pre_init(44100,-16,2,512) # prevent sound delay
pygame.init()  # Start screen
mixer.init()
##Screen
cellsize = 30
cellnumber = 20
screen = pygame.display.set_mode((cellsize*cellnumber, cellsize*(cellnumber+2)))
clock = pygame.time.Clock()
##Sounds
mixer.music.load('snake/CODEX Music-2016.mp3')
mixer.music.set_volume(0.1)
mixer.music.play()
##Images
rat = pygame.image.load('snake/rat_icon.png').convert_alpha()
new_rat = pygame.transform.scale(rat, (cellsize,cellsize))
apple = pygame.image.load('snake/apple.png').convert_alpha()
new_apple = pygame.transform.scale(apple, (cellsize,cellsize))
fence = pygame.image.load('snake/fence.png').convert_alpha()
new_fence = pygame.transform.scale(fence, (cellsize, cellsize))
##Font
game_font = pygame.font.Font(None, 25)
##Lists
snake_score = []
apple_time = []
apple_var = [4]
applelist = [0,0]

#Running system
main_game = MAIN() # start game
running = True
SCREEN_UPDATE = pygame.USEREVENT # Take input from user
pygame.time.set_timer(SCREEN_UPDATE,300) # this event is going to be triggered by user every 300 milliseconds.

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.action()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = pygame.math.Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = pygame.math.Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = pygame.math.Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = pygame.math.Vector2(-1,0)


    screen.fill((54, 110, 12)) #layer 1: screen backgroud
    main_game.draw_elements() #layer 2: fruit
    pygame.display.update() #display all above.
    clock.tick(60)

##Problems:
#random transparent apple
#Timer in negative
