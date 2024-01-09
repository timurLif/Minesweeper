import os
import sys


import pygame
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    
    image = pygame.image.load(fullname)
    return image


class Board:
    # создание поля
    def __init__(self, field_width, field_height):
        self.field_width = field_width
        self.field_height = field_height
        self.board = [['0'] * self.field_width for _ in range(self.field_height)]

        list_mines = []
        if field_width == field_height == 8:
            while len(list_mines) < 10:
                current_mine_coord = (random.randint(0, field_width - 1),
                                      random.randint(0, field_height - 1))
                
                if current_mine_coord not in list_mines:
                    list_mines.append(current_mine_coord)
        
        elif field_width == field_height == 16:
            while len(list_mines) < 40:
                current_mine_coord = (random.randint(0, field_width - 1),
                                      random.randint(0, field_height - 1))
                
                if current_mine_coord not in list_mines:
                    list_mines.append(current_mine_coord)
        
        for i in list_mines:
            self.board[i[0]][i[1]] = '*'

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
    
    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        print(cell_coords)

    # Вычисление координат клетки
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x <= self.field_width - 1 and 0 <= cell_y <= self.field_height - 1:
            return (cell_x, cell_y)

        return None
    
    def render(self, screen):
        for y in range(self.field_height):
            for x in range(self.field_width):
                pygame.draw.rect(screen, 'white', (x * self.cell_size + self.left,
                                                   y * self.cell_size + self.top,
                                                   self.cell_size, self.cell_size), 1)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)

    fps = 60
    clock = pygame.time.Clock()
    board = Board(8, 8)
    board.set_view(100, 50, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)