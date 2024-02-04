import pygame
import time
from pygame.locals import *
import random

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.image= pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [40]*length
        self.y = [40]*length


    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'

    def move_up(self):
         self.direction = 'up'
    def move_down(self):
         self.direction = 'down'


    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -=SIZE
        if self.direction == 'down':
            self.y[0] +=SIZE

        self.draw()

    def draw(self):
        for i in range (self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)



class Game :
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.play_bgm()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((255, 255, 255))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >=  x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1<y2+SIZE:
                return True
        return False


    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,0))
        self.surface.blit(score, (800, 10))

    def play_bgm(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg=pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake coliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        linel = font.render(f"You didn't protect Xukun's {self.snake.length} eggs", True, (255,255,0))
        self.surface.blit(linel,(200,300))
        line2 = font.render(f"Xukun invites you to press Enter to play again, Press Escape to exit", True, (255,255,0))
        self.surface.blit(line2, (200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer_music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()




                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()


            time.sleep(0.25)



if __name__ == '__main__':
    game = Game()
    game.run()


