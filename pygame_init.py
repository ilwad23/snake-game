import pygame
from pygame.display import update

pygame.init()

WIDTH, HEIGHT = 100, 100
HALFW, HALFH = WIDTH / 2, HEIGHT / 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SET YOUR GAME TITLE")
BG_COLOR = (201, 242, 212)


def main():
    # Variables
    crashed = False
    clock = pygame.time.Clock()
    # gets the running untill it is quited or it crashed
    while not crashed:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

    # Background color
    SCREEN.fill(BG_COLOR)

    # updates the screen
    update()

    pygame.quit()


if __name__ == "__main__":
    main()
