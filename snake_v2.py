# Imports


import pygame
from pygame.display import update
from random import randint


# Configs and Veriables


pygame.init()
# SCREEN
WIDTH, HEIGHT = 800, 800
HALFW, HALFH = WIDTH / 2, HEIGHT / 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
BG_COLOR = (201, 242, 212)

# SNAKE
SPOTS_FOR_SNAKE = 20
size = (WIDTH / SPOTS_FOR_SNAKE, HEIGHT / SPOTS_FOR_SNAKE)
turn = 'right'
snake_head = pygame.Rect(
    (HALFW, HALFH), size
)
SNAKE_COLOR = (37, 54, 44)
body_arr = [snake_head]
last = len(body_arr) - 1
direction = {
    "left": [body_arr[last].w, 0],
    "right": [-body_arr[last].w, 0],
    "up": [0, body_arr[last].h],
    "down": [0, -body_arr[last].h],
}
snake_body = pygame.Rect((snake_head.x + direction[turn][0], snake_head.y + direction[turn][1]), size)


# FOOD
SPOTS_FOR_FOOD = 50
food = pygame.Rect((HALFW, HALFH), (WIDTH / SPOTS_FOR_FOOD, HEIGHT / SPOTS_FOR_FOOD))
FOOD_COLOR = (171, 22, 37)


# Functions


def add_body():
    # varibale
    global body_arr
    # adds a new square to the array (body_arr) to join the body
    new_part = pygame.Rect(
        (snake_head.w, snake_head.h),
        (WIDTH / SPOTS_FOR_SNAKE, HEIGHT / SPOTS_FOR_SNAKE),
    )
    body_arr.append(new_part)


def collision_detector():
    # detects if the snake eat the food then changes the placement of the food to a new location on the sceen.
    if body_arr[last].colliderect(food):
        # when the snke eats the food its body will grow, this function will add another part to the body.
        add_body()
        # this variable becomes true
        return [(randint(0, WIDTH - food.width), randint(0, HEIGHT - food.width))]
    return [(food.x, food.y)]


def block(side):
    # these boolens become true when the snke go through the sides of the screen.
    left = body_arr[last].right + 10 <= 0
    right = body_arr[last].left - 10 >= WIDTH
    top = body_arr[last].bottom + 10 <= 0
    bottom = body_arr[last].top + 10 >= HEIGHT
    sides = [left, right, top, bottom]
    return sides[side]


def controls(vel, move_snake):
    key = pygame.key.get_pressed()
    # the snake will move in different direction according the arrows pressed
    if key[pygame.K_LEFT] and move_snake[1] != "right":
        move_snake = [[-abs(vel), 0], "left"]
    if key[pygame.K_RIGHT] and move_snake[1] != "left":
        move_snake = [[abs(vel), 0], "right"]
    if key[pygame.K_UP] and move_snake[1] != "down":
        move_snake = [[0, -abs(vel)], "up"]
    if key[pygame.K_DOWN] and move_snake[1] != "up":
        move_snake = [[0, abs(vel)], "down"]

    return move_snake


def handle_move_for_snake(vel, move_snake, still_out):
    # Variables
    out_of_screen = block(0) or block(1) or block(2) or block(3)
    move_snake = controls(vel, move_snake)
    # makes the snake comes out from the side it went through
    if out_of_screen and still_out == 0:
        still_out = 1
        if move_snake[1] == "right":
            body_arr[last].x = 1
        if move_snake[1] == "left":
            body_arr[last].x = WIDTH - 1
        if move_snake[1] == "up":
            body_arr[last].y = HEIGHT - body_arr[last].height
        if move_snake[1] == "down":
            body_arr[last].y = 1
    elif not out_of_screen:
        still_out = 0

    return move_snake


def display_on_screen(move_snake):
    # Background color
    SCREEN.fill(BG_COLOR)
    # food that the snake eats. it will update its position each time the snake eats it.
    food.update(collision_detector()[0], food.size)
    pygame.draw.rect(SCREEN, FOOD_COLOR, food)
    # this will move and display the body part
    for i, p in enumerate(body_arr):
        if i != 0:
            p.update((body_arr[i-1].x + direction[turn][0], body_arr[i-1].y + direction[turn][1]), size)
        body_arr[i].move_ip(move_snake[0])
        pygame.draw.rect(SCREEN, SNAKE_COLOR, p)
    # updates the screen
    update()


def main():
    # Variables
    CLOCK = pygame.time.Clock()
    still_out = 0
    vel = 1
    move_snake = [[vel, 0], "right"]
    crashed = False
    # gets the running untill it is quited or it crashed
    while not crashed:
        CLOCK.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        # handles how the snake moves
        move_snake = handle_move_for_snake(vel, move_snake, still_out)

        display_on_screen(move_snake)

    pygame.quit()


if __name__ == "__main__":
    main()
