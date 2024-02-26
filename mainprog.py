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
        self.board = [['-'] * self.field_width for _ in range(self.field_height)]
        self.start_time = pygame.time.get_ticks()
        self.restart_button = False
        self.lobby_button = False
        self.changes_on_the_board = True
        self.count_open_cells = 0

        list_mines = []
        if field_width == field_height == 8:
            while len(list_mines) < 10:
                current_mine_coord = (random.randint(0, field_width - 1),
                                      random.randint(0, field_height - 1))

                if current_mine_coord not in list_mines:
                    list_mines.append(current_mine_coord)

            self.max_cells = 8 * 8
            self.set_view(30, 30, 50)

        elif field_width == field_height == 16:
            while len(list_mines) < 40:
                current_mine_coord = (random.randint(0, field_width - 1),
                                      random.randint(0, field_height - 1))

                if current_mine_coord not in list_mines:
                    list_mines.append(current_mine_coord)

            self.max_cells = 16 * 16
            self.set_view(30, 30, 25)

        self.num_of_mines = len(list_mines)

        for i in list_mines:
            self.board[i[0]][i[1]] = '*'

        self.creation_of_numbers()

    def creation_of_numbers(self):
        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.board[y][x] != '*':
                    count = 0

                    if x != 0 and self.board[y][x - 1] == '*':
                        count += 1
                    if x != self.field_width - 1 and self.board[y][x + 1] == '*':
                        count += 1
                    if y != 0 and self.board[y - 1][x] == '*':
                        count += 1
                    if y != self.field_height - 1 and self.board[y + 1][x] == '*':
                        count += 1
                    if x != 0 and y != self.field_height - 1 and self.board[y + 1][x - 1] == '*':
                        count += 1
                    if x != self.field_width - 1 and y != self.field_height - 1 and self.board[y + 1][x + 1] == '*':
                        count += 1
                    if x != 0 and y != 0 and self.board[y - 1][x - 1] == '*':
                        count += 1
                    if x != self.field_width - 1 and y != 0 and self.board[y - 1][x + 1] == '*':
                        count += 1

                    if count != 0:
                        self.board[y][x] = f'-{count}'

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell != None and self.changes_on_the_board == True:
            self.open_cell(cell[0], cell[1])

        elif 445 < mouse_pos[0] < 582 and 200 < mouse_pos[1] < 290:
            self.restart_button = True

        elif 445 < mouse_pos[0] < 582 and 340 < mouse_pos[1] < 430:
            self.lobby_button = True

    def restart(self):
        return self.restart_button

    def lobby(self):
        return self.lobby_button

    def open_cell(self, x, y):
        if self.board[y][x] == '-':
            self.board[y][x] = '0'

            if x > 0:
                if self.board[y][x - 1] == '-':
                    self.open_cell(x - 1, y)
                elif len(self.board[y][x - 1]) == 2:
                    self.board[y][x - 1] = self.board[y][x - 1][1]

            if x < self.field_width - 1:
                if self.board[y][x + 1] == '-':
                    self.open_cell(x + 1, y)
                elif len(self.board[y][x + 1]) == 2:
                    self.board[y][x + 1] = self.board[y][x + 1][1]

            if y > 0:
                if self.board[y - 1][x] == '-':
                    self.open_cell(x, y - 1)
                elif len(self.board[y - 1][x]) == 2:
                    self.board[y - 1][x] = self.board[y - 1][x][1]

            if y < self.field_height - 1:
                if self.board[y + 1][x] == '-':
                    self.open_cell(x, y + 1)
                elif len(self.board[y + 1][x]) == 2:
                    self.board[y + 1][x] = self.board[y + 1][x][1]

            if x > 0 and y > 0:
                if self.board[y - 1][x - 1] == '-':
                    self.open_cell(x - 1, y - 1)
                elif len(self.board[y - 1][x - 1]) == 2:
                    self.board[y - 1][x - 1] = self.board[y - 1][x - 1][1]

            if x > 0 and y < self.field_height - 1:
                if self.board[y + 1][x - 1] == '-':
                    self.open_cell(x - 1, y + 1)
                elif len(self.board[y + 1][x - 1]) == 2:
                    self.board[y + 1][x - 1] = self.board[y + 1][x - 1][1]

            if x < self.field_width - 1 and y > 0:
                if self.board[y - 1][x + 1] == '-':
                    self.open_cell(x + 1, y - 1)
                elif len(self.board[y - 1][x + 1]) == 2:
                    self.board[y - 1][x + 1] = self.board[y - 1][x + 1][1]

            if x < self.field_width - 1 and y < self.field_height - 1:
                if self.board[y + 1][x + 1] == '-':
                    self.open_cell(x + 1, y + 1)
                elif len(self.board[y + 1][x + 1]) == 2:
                    self.board[y + 1][x + 1] = self.board[y + 1][x + 1][1]

        elif len(self.board[y][x]) == 2:
            self.board[y][x] = self.board[y][x][1]

        elif self.board[y][x] == '*':
            self.changes_on_the_board = False

        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.board[y][x] == '0':
                    self.count_open_cells += 1

                elif len(self.board[y][x]) == 1 and self.board[y][x].isdigit():
                    self.count_open_cells += 1

        if (self.max_cells - self.count_open_cells) == self.num_of_mines:
            self.changes_on_the_board = 'win'

        self.count_open_cells = 0

    # Вычисление координат клетки
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x <= self.field_width - 1 and 0 <= cell_y <= self.field_height - 1:
            return (cell_x, cell_y)

        return None

    def time(self):
        font_time = pygame.font.Font(None, 50)
        minutes = time_elapsed // 60000
        seconds = (time_elapsed % 60000) // 1000
        text_time = font_time.render(f'{minutes:02d}:{seconds:02d}', True, 'white')
        screen.blit(text_time, (475, 125))
        board_sprites.draw(screen)

        # restart и выход в меню
        pygame.draw.rect(screen, 'white', (445, 200, 137, 90), 2)
        pygame.draw.rect(screen, 'white', (445, 340, 137, 90), 2)

    def render(self, screen):
        for y in range(self.field_height):
            for x in range(self.field_width):
                pygame.draw.rect(screen, 'white', (x * self.cell_size + self.left,
                                                   y * self.cell_size + self.top,
                                                   self.cell_size, self.cell_size), 1)

                if self.board[y][x] == '0':
                    screen.fill(pygame.Color('gray'), pygame.Rect(x * self.cell_size + self.left + 1,
                                                                  y * self.cell_size + self.top + 1,
                                                                  self.cell_size - 2, self.cell_size - 2))

                elif len(self.board[y][x]) == 1 and self.board[y][x].isdigit():
                    screen.fill(pygame.Color('gray'), pygame.Rect(x * self.cell_size + self.left + 1,
                                                                  y * self.cell_size + self.top + 1,
                                                                  self.cell_size - 2, self.cell_size - 2))
                    font = pygame.font.Font(None, self.cell_size)
                    text = font.render(f'{self.board[y][x]}', True, 'red')
                    screen.blit(text, (x * self.cell_size + self.left + self.cell_size // 3,
                                       y * self.cell_size + self.top + self.cell_size // 5))
                    self.time()

                if self.changes_on_the_board == False and self.board[y][x] == '*':
                    screen.fill(pygame.Color('red'), pygame.Rect(x * self.cell_size + self.left + 1,
                                                                 y * self.cell_size + self.top + 1,
                                                                 self.cell_size - 2, self.cell_size - 2))
                    self.time()

                if self.changes_on_the_board == 'win' and self.board[y][x] == '*':
                    screen.fill(pygame.Color('green'), pygame.Rect(x * self.cell_size + self.left + 1,
                                                                   y * self.cell_size + self.top + 1,
                                                                   self.cell_size - 2, self.cell_size - 2))


# Пробный класс главного меню, который надо переделать и сделать красивым
class MainMenu:
    def __init__(self):
        self.game_mode = (0, 0)
        self.current_screen = 'start'
        self.count = None

    def get_click(self, mouse_pos):
        if self.current_screen == 'start':
            if 100 < mouse_pos[0] < 200 and 100 < mouse_pos[1] < 150:
                self.current_screen = 'select_screen'

        elif self.current_screen == 'select_screen':
            if 50 < mouse_pos[0] < 150 and 100 < mouse_pos[1] < 200:
                self.game_mode = (8, 8)

            elif 250 < mouse_pos[0] < 350 and 100 < mouse_pos[1] < 200:
                self.game_mode = (16, 16)
            self.count = 'New board'


    def open_game(self):
        if self.game_mode == (0, 0):
            return (True, self.game_mode)
        else:
            return (False, self.game_mode)

    def render(self, screen):
        font = pygame.font.Font(None, 35)
        if self.current_screen == 'select_screen':
            pygame.draw.rect(screen, 'black', (50, 45, 400, 35))
            text = font.render(f'Выбери режим: 8 * 8 или 16 * 16', True, 'white')
            screen.blit(text, (50, 50))

            pygame.draw.rect(screen, 'black', (50, 100, 100, 100))
            text_1 = font.render(f'8 * 8', True, 'white')
            screen.blit(text_1, (76, 135))

            pygame.draw.rect(screen, 'black', (250, 100, 100, 100))
            text_2 = font.render(f'16 * 16', True, 'white')
            screen.blit(text_2, (263, 135))


        elif self.current_screen == 'start':
            pygame.draw.rect(screen, 'black', (100, 100, 100, 50))
            text_0 = font.render(f'Играть', True, 'white')
            screen.blit(text_0, (112, 115))



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    size = width, height = 600, 470
    screen = pygame.display.set_mode(size)

    # Спрайты в классе Board
    board_sprites = pygame.sprite.Group()

    clock_sprite = pygame.sprite.Sprite(board_sprites)
    clock_sprite.image = load_image("clock.jpeg")
    clock_sprite.rect = clock_sprite.image.get_rect()
    clock_sprite.image = pygame.transform.scale(clock_sprite.image, (100, 100))
    clock_sprite.rect.x = 466
    clock_sprite.rect.y = 10

    restart_sprite = pygame.sprite.Sprite(board_sprites)
    restart_sprite.image = load_image("restart.jpeg")
    restart_sprite.rect = restart_sprite.image.get_rect()
    restart_sprite.image = pygame.transform.scale(restart_sprite.image, (150, 150))
    restart_sprite.rect.x = 438
    restart_sprite.rect.y = 170

    lobby_sprite = pygame.sprite.Sprite(board_sprites)
    lobby_sprite.image = load_image("home.jpeg")
    lobby_sprite.rect = lobby_sprite.image.get_rect()
    lobby_sprite.image = pygame.transform.scale(lobby_sprite.image, (100, 100))
    lobby_sprite.rect.x = 463
    lobby_sprite.rect.y = 333

    fps = 60
    clock = pygame.time.Clock()
    # board = Board(8, 8)
    main_menu = MainMenu()
    game_run = False
    # board.set_view(100, 50, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_run:
                    board.get_click(event.pos)
                else:
                    main_menu.get_click(event.pos)

        screen.fill((0, 0, 0))
        if not game_run:
            bg = load_image("minesweeper.jpeg")
            screen.blit(bg, (-20, -15))
        if main_menu.open_game()[0]:
            main_menu.render(screen)
        elif main_menu.open_game()[0] is False and main_menu.count == 'New board':
            board = Board(main_menu.open_game()[1][0], main_menu.open_game()[1][1])
            game_run = True
            main_menu.count = None
        elif board.restart():
            board = Board(main_menu.open_game()[1][0], main_menu.open_game()[1][1])
        elif board.lobby():
            game_run = False
            main_menu.game_mode = (0, 0)
            main_menu.current_screen = 'start'
        else:
            board.render(screen)
            time_elapsed = pygame.time.get_ticks() - board.start_time

        pygame.display.flip()
        clock.tick(fps)