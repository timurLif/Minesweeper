import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)

    fps = 60
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.flip()
        clock.tick(fps)