import os
import sys
import pygame


class Board:
    # создание поля
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.board = [i.split() for i in open(name).readlines()]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = load_image('img_2.png').get_size()[0]
        self.x = 5
        self.y = 5

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def position(self, position, screen):
        x, y = int((position[0] - self.left) / self.cell_size), int((position[1] - self.top) / self.cell_size)
        if y >= self.height or x >= self.width:
            print(None)
        else:
            return (y, x)

    def render(self, screen):
        screen.fill((0, 0, 0))
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == '0':
                    image = load_image('img_2.png')
                else:
                    image = load_image('img_1.png')
                screen.blit(image, (self.left + x * self.cell_size, self.top + y * self.cell_size))
        screen.blit(load_image('img_3.png'), (10 + self.x * self.cell_size + 15, 10 + self.y * self.cell_size + 7))
        pygame.display.flip()



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def main_screen(screen):
    fon = load_image("img.png")
    pygame.display.set_mode((600, 349))
    intro_text = ["ИГРА", "",
                  "Для запуска игры нажми любую кнопку"]

    fon = pygame.transform.scale(fon, (600, 349))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black' if intro_text.index(line) != len(intro_text) - 1 else 'red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                return 2
        pygame.display.flip()


def game_screen(screen):
    name = input()
    try:
        map = open(name).readlines()
    except Exception:
        print('Такого файла не существует')
        return 0
    board = Board(len(map[0]) // 2, len(map), name)
    pygame.display.set_mode((board.width * board.cell_size + 50, board.height * board.cell_size + 50))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board.top += board.cell_size
                if event.key == pygame.K_DOWN:
                    board.top -= board.cell_size
                if event.key == pygame.K_LEFT:
                    board.left += board.cell_size
                if event.key == pygame.K_RIGHT:
                    board.left -= board.cell_size
        board.render(screen)
        pygame.display.flip()
    return 0

screen_type = {1: main_screen, 2: game_screen}

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    cur_screen = 1
    while cur_screen:
        cur_screen = screen_type[cur_screen](screen)
    pygame.quit()