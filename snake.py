import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
color = (201, 242, 212)
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

def main():
    crashed = False
    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                
        gameDisplay.fill(color)
        pygame.display.update()
        # clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()