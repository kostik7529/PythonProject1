import copy

import pygame

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 60

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def position(self, position):
        x, y = int((position[0] - self.left) / self.cell_size), int((position[1] - self.top) / self.cell_size)
        if y >= self.height or x >= self.width:
            print(None)
        else:
            return (y, x)

    def render(self, screen):
        screen.fill((0, 0, 0))
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, 'white', (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size),1)
        pygame.display.flip()



class Lines(Board):
    # создание поля
    def __init__(self, width, height):
        super().__init__(width, height)
        self.x = None
        self.y = None
        self.cur = 1
        self.clock = pygame.time.Clock()

    def position(self, position):
        x, y = int((position[0] - self.left) / self.cell_size), int((position[1] - self.top) / self.cell_size)
        if y >= self.height or x >= self.width:
            print(None)
        else:
            if self.board[y][x] == -1 and self.x is None:
                self.board[y][x] = 0
                self.x = x
                self.y = y
            elif self.x == x and self.y == y:
                self.board[y][x] = -1
                self.x = None
                self.y = None
            elif self.board[y][x] != -1 and not self.x is None:
                lab = self.has_path(self.x, self.y, x, y)
                if lab:
                    for i in range(self.width):
                        for j in range(self.height):
                            self.board[j][i] = -1 if self.board[j][i] == -1 else 0
                    path = self.find_path(self.board.copy(), self.x, self.y, x, y)
                    self.go(path)
                    self.cur = 1
                    self.board[y][x] = -1
                    self.x = None
                    self.y = None
                    self.render(screen)
                else:
                    self.cur = 1
                    for x in range(self.width):
                        for y in range(self.height):
                            self.board[y][x] = -1 if self.board[y][x] == -1 else 0
            else:
                self.board[y][x] = -1

    def render(self, screen):
        screen.fill((0, 0, 0))
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, 'white', (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size),1)
                if x == self.x and y == self.y:
                    pygame.draw.circle(screen, 'red', (self.left + x * self.cell_size + self.cell_size * 0.5,
                                                        self.top + y * self.cell_size + self.cell_size * 0.5),
                                       self.cell_size * 0.5 - 2)
                if self.board[y][x] == -1:
                    pygame.draw.circle(screen, 'blue', (self.left + x * self.cell_size + self.cell_size * 0.5,
                                                       self.top + y * self.cell_size + self.cell_size * 0.5),
                                       self.cell_size * 0.5 - 2)
        pygame.display.flip()

    def has_path(self, x, y, x1, y1):
        return self.wave(x, y, x1, y1)[y1][x1] > 0

    def wave(self, x, y, x1, y1):
        self.board[y][x] = self.cur
        if y + 1 < self.height:
            if self.board[y + 1][x] == 0 or (self.board[y + 1][x] != -1 and self.board[y + 1][x] > self.cur):
                self.cur += 1
                self.wave(x, y + 1, x1, y1)
        if x + 1 < self.width:
            if self.board[y][x + 1] == 0 or (self.board[y][x + 1] != -1 and self.board[y][x + 1] > self.cur):
                self.cur += 1
                self.wave(x + 1, y, x1, y1)
        if x - 1 >= 0:
            if self.board[y][x - 1] == 0 or (self.board[y][x - 1] != -1 and self.board[y][x - 1] > self.cur):
                self.cur += 1
                self.wave(x - 1, y, x1, y1)
        if y - 1 >= 0:
            if self.board[y - 1][x] == 0 or (self.board[y - 1][x] != -1 and self.board[y - 1][x] > self.cur):
                self.cur += 1
                self.wave(x, y - 1, x1, y1)
        return self.board

    def find_path(self, map1, x1, y1, x2, y2):
        cur = 2
        if x1 - 1 >= 0 and map1[y1][x1 - 1] != -1:
            map1[y1][x1 - 1] += 1
        if x1 + 1 < self.width and map1[y1][x1 + 1] != -1:
            map1[y1][x1 + 1] += 1
        if y1 - 1 >= 0 and map1[y1 - 1][x1] != -1:
            map1[y1 - 1][x1] += 1
        if y1 + 1 < self.height and map1[y1 + 1][x1] != -1:
            map1[y1 + 1][x1] += 1
        while not map1[y2][x2]:
            for i in range(self.height):
                for j in range(self.width):
                    if map1[i][j] != -1 and map1[i][j] == 0 and not (y1 == i and x1 == j):
                        if j - 1 >= 0 and map1[i][j - 1] == cur - 1:
                            map1[i][j] = cur
                        if j + 1 < self.width and map1[i][j + 1] == cur - 1:
                            map1[i][j] = cur
                        if i - 1 >= 0 and map1[i - 1][j] == cur - 1:
                            map1[i][j] = cur
                        if i + 1 < self.height and map1[i + 1][j] == cur - 1:
                            map1[i][j] = cur
            if cur == 1000:
                break
            cur += 1
        points = [(y2, x2)]
        cur = map1[y2][x2] - 1
        while not (x2 == x1 and y1 == y2):
            points.append(list(filter(lambda x: x != (-1, -1) and map1[x[0]][x[1]] == cur, [(y2 - 1, x2) if y2 -1 >= 0 else (-1, -1), (y2, x2 - 1) if x2 - 1 >= 0 else (-1, -1),
                               (y2 + 1, x2) if y2 + 1 < self.height else (-1, -1), (y2, x2 + 1) if x2 + 1 < self.width
                               else (-1, -1)]))[0])
            y2, x2 = points[-1]
            cur -= 1
        return points[-1::-1]

    def go(self, path):
        for i in path:
            self.y, self.x = i
            self.render(screen)
            self.clock.tick(10)


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 800, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    board = Lines(5, 7)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.position(event.pos)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()