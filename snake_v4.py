import pygame
from pygame.display import update
from random import randint
import time as x

# Configs and Veriables

pygame.init()
# GAME
WIDTH, HEIGHT = 800, 800
HALFW, HALFH = WIDTH / 2, HEIGHT / 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
crashed = False
BG_COLOR = (201, 242, 212)
CLOCK = pygame.time.Clock()
score = 0
font = pygame.font.Font("freesansbold.ttf", 45)
# SNAKE
SIZE_FOR_SNAKE = WIDTH / 20
snake = [pygame.Rect((HALFW, HALFH), (SIZE_FOR_SNAKE, SIZE_FOR_SNAKE))]
SNAKE_COLOR = (37, 54, 44)
SNAKE_HEAD = snake[0]
VEL = SIZE_FOR_SNAKE
TURN = {
    "right": [VEL, 0],
    "left": [-VEL, 0],
    "up": [0, -VEL],
    "down": [0, VEL],
    "p": [0, 0],
}
dir = "right"
# FOOD
SIZE_FOR_FOOD = WIDTH / 40
food = pygame.Rect((WIDTH - SIZE_FOR_FOOD, HALFH), (SIZE_FOR_FOOD, SIZE_FOR_FOOD))
FOOD_COLOR = (171, 22, 37)

# Functions
def add_body():
    # varibale
    global snake, score
    # adds a new square to the array (snake) to join the body
    new_part = pygame.Rect(
        (SNAKE_HEAD.x, SNAKE_HEAD.y),
        (SIZE_FOR_SNAKE, SIZE_FOR_SNAKE),
    )
    snake.append(new_part)
    score += 1


def collision_detector():
    # detects if the snake eat the food then changes the placement of the food to a new location on the sceen.
    if SNAKE_HEAD.colliderect(food):
        # when the snke eats the food its body will grow, this function will add another part to the body.
        add_body()
        # this variable becomes true
        return [(randint(0, WIDTH - food.width), randint(0, HEIGHT - food.width))]
    return [(food.x, food.y)]


def controls():
    global dir
    key = pygame.key.get_pressed()
    # the snake will move in different direction according the arrows pressed
    if key[pygame.K_LEFT] and dir != "right":
        dir = "left"
    if key[pygame.K_RIGHT] and dir != "left":
        dir = "right"
    if key[pygame.K_UP] and dir != "down":
        dir = "up"
    if key[pygame.K_DOWN] and dir != "up":
        dir = "down"
    if key[pygame.K_p]:
        dir = "p"


def handle_move_for_snake():
    # makes the snake move and comes out from the side it went through
    controls()
    if dir == "right" and SNAKE_HEAD.x >= WIDTH - SIZE_FOR_FOOD:
        SNAKE_HEAD.x = 0
    if dir == "left" and SNAKE_HEAD.x < 0:
        SNAKE_HEAD.x = WIDTH - SIZE_FOR_FOOD
    if dir == "up" and SNAKE_HEAD.y < 0:
        SNAKE_HEAD.y = HEIGHT - SNAKE_HEAD.height
    if dir == "down" and SNAKE_HEAD.y >= HEIGHT - SIZE_FOR_FOOD:
        SNAKE_HEAD.y = 0


def game_over():
    global crashed, dir
    for i in range(len(snake)):
        if i != 0:
            if SNAKE_HEAD.colliderect(snake[i]):
                dir = "p"
                # crashed = True
                print("hit")


def display_on_screen():
    # Background color
    SCREEN.fill(BG_COLOR)
    TEXT = font.render(f"Score: {score}", True, (0, 0, 0))
    SCREEN.blit(TEXT, (5, 5))
    game_over()
    # food that the snake eats. it will update its position each time the snake eats it.
    food.update(collision_detector()[0], food.size)
    pygame.draw.rect(SCREEN, FOOD_COLOR, food)
    # this will move and display the body part
    handle_move_for_snake()
    if dir != "p":
        for i in range(len(snake) - 1, -1, -1):
            if i != 0:
                p = snake[i - 1]
                snake[i].x = p.x
                snake[i].y = p.y

    SNAKE_HEAD.move_ip(TURN[dir])
    for i, p in enumerate(snake):
        pygame.draw.rect(SCREEN, (37, 54, 44), p)
    pygame.draw.rect(SCREEN, (0, 0, 0), SNAKE_HEAD)
    x.sleep(0.5)
    # updates the screen
    update()


def main():
    # Variables
    global crashed
    # gets the running untill it is quited or it crashed
    while not crashed:
        CLOCK.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        display_on_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
