import pygame
from pygame.display import update
from random import randint
import time

pygame.init()


class Food:
    def __init__(self, screen, snake, size=20):
        self.screen = screen
        self.snake = snake
        self.x = self.snake.starting + 200
        self.y = self.snake.starting
        self.size = size
        self.color = (250, 0, 10)
        self.rectangle = pygame.Rect(self.x, self.y, self.size, self.size)

    def update_position(self):
        # self.rectangle.update(randint(0,800),randint(0,800),self.size,self.size)
        foodcopy = pygame.Rect(
            (randint(0, 800), randint(0, 800)), (self.size, self.size)
        )
        for i in self.snake.rectangles:
            while i.colliderect(foodcopy):
                print("caught", foodcopy)
                foodcopy = pygame.Rect(
                    (randint(0, 800), randint(0, 800)), (self.size, self.size)
                )
                print("changed", foodcopy)
        self.rectangle = foodcopy

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rectangle)


class Snake:
    def __init__(self, screen, screen_size, size=40):
        self.screen = screen
        self.screen_size = screen_size
        self.size = (size, size)
        self.starting = self.screen_size / 2 - self.size[0]
        self.end = self.screen_size - self.size[0]
        self.head = pygame.Rect((self.starting, self.starting), self.size)
        self.rectangles = [self.head]
        self.color = (37, 54, 44)
        self.velocity = self.size[0]
        self.turns = {
            "right": [self.velocity, 0],
            "left": [-self.velocity, 0],
            "up": [0, -self.velocity],
            "down": [0, self.velocity],
            "p": [0, 0],
        }
        self.direction = "right"
        self.score = 0

    def game_over(self):
        for i in range(len(self.rectangles)):
            if i != 0:
                if self.head.colliderect(self.rectangles[i]):
                    print('gameover')
                    self.__init__(self.screen, self.screen_size)
                    break

    def add(self):
        self.score += self.score // 10 + 1
        self.rectangles.append(
            pygame.Rect((self.rectangles[-1].x, self.rectangles[-1].y), self.size)
        )
        
    def controls(self):
        key = pygame.key.get_pressed()
        # the snake will move in different direction according the arrows pressed
        if key[pygame.K_LEFT] and self.direction != "right":
            self.direction = "left"
        if key[pygame.K_RIGHT] and self.direction != "left":
            self.direction = "right"
        if key[pygame.K_UP] and self.direction != "down":
            self.direction = "up"
        if key[pygame.K_DOWN] and self.direction != "up":
            self.direction = "down"
        if key[pygame.K_p]:
            self.direction = "p"

    def walls(self):
        # when the snake goes through the wall it will return through the opposite wall
        if self.head.x > self.end:
            self.head.x = 0
        if self.head.x < 0:
            self.head.x = self.end
        if self.head.y > self.end:
            self.head.y = 0
        if self.head.y < 0:
            self.head.y = self.end

    def update_position(self):
        self.controls()
        self.walls()
        for i in range(len(self.rectangles) - 1, -1, -1):
            if i != 0:
                position = (self.rectangles[i - 1].x, self.rectangles[i - 1].y)
                self.rectangles[i].update(position, self.size)
        self.head.move_ip(self.turns[self.direction])

    def draw(self):
        for rect in self.rectangles:
            pygame.draw.rect(self.screen, self.color, rect)


class Game:
    def __init__(self, screen_size=800, color=(201, 242, 212)):
        self.screen_size = screen_size
        self.title = "Snake Game"
        self.color = color
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption(self.title)
        self.font = pygame.font.Font("freesansbold.ttf", 45)
        self.crashed = False
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.screen, self.screen_size)
        self.food = Food(self.screen, self.snake)
        pass

    def collision_with_food(self):
        if self.snake.head.colliderect(self.food.rectangle):
            self.food.update_position()
            self.snake.add()
        pass

    def main(self):
        # gets the running untill it is quited or it crashed
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

            # background
            self.screen.fill(self.color)
            # score
            text = self.font.render(f"Score: {self.snake.score}", True, (0, 0, 0))
            self.screen.blit(text, (5, 5))
            # checking
            self.snake.game_over()
            self.collision_with_food()
            # updating
            # print(self.snake.rectangles)
            self.snake.update_position()
            # drawing
            self.food.draw()
            self.snake.draw()
            # updating the screen
            time.sleep(0.5)
            self.clock.tick(120)
            update()

        pygame.quit()


if __name__ == "__main__":
    Game().main()
