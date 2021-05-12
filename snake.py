import pygame
from pygame.cursors import arrow
from pygame.display import update

# Configs and Veriables
pygame.init()
WIDTH, HEIGHT = 800, 800
HALFW, HALFH = WIDTH/2, HEIGHT/2
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
BG_COLOR = (201, 242, 212)
SPOTS = 20
snake = pygame.Rect((HALFW, HALFH), (WIDTH/SPOTS, HEIGHT/SPOTS))
SNAKE_COLOR = (37, 54, 44)

# Functions

def block(arrow):
    left = snake.left < 10
    right =  snake.left  >= WIDTH
    top = snake.bottom <= 0
    bottom =  snake.top >= HEIGHT
    arrows = [left, right, top, bottom]
    return arrows[arrow]

def controls(vel,turn):
    key = pygame.key.get_pressed()       

    if key[pygame.K_LEFT]:turn = [[-abs(vel),0],'left']
    if key[pygame.K_RIGHT] :turn = [[abs(vel),0], 'right']
    if key[pygame.K_UP]:turn = [[0, -abs(vel)], 'up']
    if key[pygame.K_DOWN]:turn = [[0,abs(vel)], 'down']

    return turn

def move_snake(vel, turn, still_out):
    out_of_screen = (block(0) or block(1) or block(2) or block(3))
    turn = controls(vel,turn) 

    if out_of_screen and still_out == 0:
        still_out =1; 
        if (turn[1] == 'right' or turn[1] == 'left'): 
            turn = [[-abs(vel), 0], 'left'] if turn[1] =='right' else [[abs(vel),0], 'right']
        else: 
            turn = [[0,abs(vel)], 'down'] if turn[1]== 'up' else [[0, -abs(vel)], 'up']
    elif not out_of_screen: still_out = 0

    return turn

def display_on_screen(turn):
    SCREEN.fill(BG_COLOR) 

    snake.move_ip(turn[0])

    pygame.draw.rect(SCREEN, SNAKE_COLOR, snake)

    pygame.display.update()

def main():
    CLOCK = pygame.time.Clock(); still_out = 0; vel =1; turn = [[vel,0],'right']; 

    crashed = False 
    while not crashed:
        CLOCK.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        
        turn = move_snake(vel,turn,still_out)
        display_on_screen(turn)

    pygame.quit()

if __name__ == '__main__':
    main()