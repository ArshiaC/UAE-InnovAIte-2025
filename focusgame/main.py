import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('focusgame/tetris.mp3')
hit_sound = pygame.mixer.Sound('focusgame/hit.mp3')

pygame.mixer.music.play(-1, 0.0)

WIDTH, HEIGHT = 300, 500
FPS = 35

CELL = 20
ROWS = (HEIGHT - 120) // CELL
COLS = WIDTH // CELL

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Tetris")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (213, 229, 213)
GRID = (95, 192, 174)
WIN = (173, 178, 212)
LOSE = (235, 198, 195)
TEXT = (102, 108, 183)

ASSETS = {
    1: pygame.image.load("focusgame/Assets/1.png"),
    2: pygame.image.load("focusgame/Assets/2.png"),
    3: pygame.image.load("focusgame/Assets/3.png"),
    4: pygame.image.load("focusgame/Assets/4.png"),
}

font = pygame.font.SysFont("verdana", 50)
font2 = pygame.font.SysFont("verdana", 15)

class Shape:
    VERSION = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.SHAPES)
        self.shape = self.VERSION[self.type]
        self.color = random.randint(1, 4)
        self.orientation = 0

    def image(self):
        return self.shape[self.orientation]
    
    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)

class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.grid = [[0 for j in range(cols)] for i in range(rows)]
        self.next = None
        self.end = False
        self.new_shape()

    def make_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(SCREEN, GRID, (0, CELL*i), (WIDTH, CELL*i))
        for j in range(self.cols + 1):
            pygame.draw.line(SCREEN, GRID, (CELL*j, 0), (CELL*j, HEIGHT-120))
    
    def new_shape(self):
        if not self.next:
            self.next = Shape(5, 0)
        self.figure = self.next
        self.next = Shape(5, 0)
    
    def collision(self) -> bool:
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x
                    if (block_row >= self.rows or block_col >= self.cols or block_col < 0 or self.grid[block_row][block_col] > 0):
                        return True
        return False
    
    def remove_row(self):
        rerun = False
        for y in range(self.rows - 1, 0, -1):
            completed = True
            for x in range(0, self.cols):
                if self.grid[y][x] == 0:
                    completed = False

            if completed:
                del self.grid[y]
                self.grid.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
            
            if rerun:
                self.remove_row()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i * 4  + j) in self.figure.image():
                    self.grid[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_row()
        self.new_shape()
        if self.collision():
            self.end = True

    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -= 1
            self.freeze()
            hit_sound.play()

    def left(self):
        self.figure.x -= 1
        if self.collision():
            self.figure.x += 1
    
    def right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -= 1
    
    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
    
    def rotate(self):
        orientation = self.figure.orientation
        self.figure.rotate()
        if self.collision():
            self.figure.orientation = orientation

    def end_game(self):
        popup = pygame.Rect(50, 140, WIDTH - 100, HEIGHT - 350)
        pygame.draw.rect(SCREEN, BLACK, popup)
        pygame.draw.rect(SCREEN, LOSE, popup, 2)

        game_over = font2.render("GAME OVER!", True, WHITE)
        option1 = font2.render("Press r to restart", True, LOSE)
        option2 = font2.render("Press q to quit", True, LOSE)

        SCREEN.blit(game_over, (popup.centerx - game_over.get_width() / 2, popup.y + 20))
        SCREEN.blit(option1, (popup.centerx - option1.get_width() / 2, popup.y + 80))
        SCREEN.blit(option2, (popup.centerx - option2.get_width() / 2, popup.y + 110))

def main():
    tetris = Tetris(ROWS, COLS)
    counter = 0
    move = True
    run = True
    space_pressed = False
    while run:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            keys = pygame.key.get_pressed()
            if not tetris.end:
                if keys[pygame.K_LEFT]:
                    tetris.left()
                elif keys[pygame.K_RIGHT]:
                    tetris.right()
                elif keys[pygame.K_DOWN]:
                    tetris.move_down()
                elif keys[pygame.K_UP]:
                    tetris.rotate()
                elif keys[pygame.K_SPACE]:
                    space_pressed = True
            if keys[pygame.K_r]:
                tetris.__init__(ROWS, COLS)
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                run = False
            
        counter += 1
        if counter >= 15000:
            counter = 0
        
        if move:
            if counter % (FPS // (tetris.level * 2)) == 0:
                if not tetris.end:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False
                    else:
                        tetris.move_down()

        tetris.make_grid()

        for x in range(ROWS):
            for y in range(COLS):
                if tetris.grid[x][y] > 0:
                    value = tetris.grid[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y * CELL, x * CELL))
                    pygame.draw.rect(SCREEN, WHITE, (y * CELL, x * CELL, CELL, CELL), 1)

        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    if (i * 4 + j) in tetris.figure.image():
                        shape = ASSETS[tetris.figure.color]
                        x = CELL * (tetris.figure.x + j)
                        y = CELL * (tetris.figure.y + i)
                        SCREEN.blit(shape, (x, y))
                        pygame.draw.rect(SCREEN, WHITE, (x, y, CELL, CELL), 1)

        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if (i * 4 + j) in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELL * (tetris.next.x + j - 4)
                        y = HEIGHT - 100 + CELL * (tetris.next.y + i)
                        SCREEN.blit(image, (x, y))
        
        if tetris.end:
            tetris.end_game()

        score_text = font.render(f"{tetris.score}", True, TEXT)
        level_text = font2.render(f"level: {tetris.level}", True, TEXT)
        SCREEN.blit(score_text, (250 - score_text.get_width() // 2, HEIGHT - 110))
        SCREEN.blit(level_text, (250 - level_text.get_width() // 2, HEIGHT - 30))

        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
