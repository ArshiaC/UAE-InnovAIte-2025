import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("relaxationgame\\ambient.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

sw = 800
sh = 800

win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Breakout")

brickHitSound = pygame.mixer.Sound("relaxationgame\hit.wav")
brickHitSound.set_volume(.1)
bounceSound = pygame.mixer.Sound("relaxationgame\hitGameSound.wav")
bounceSound.set_volume(.2)

clock = pygame.time.Clock()
gameover = False

class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

class Ball(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xv = random.choice([2, 3, 4, -2, -3, -4])
        self.yv = random.randint(3, 4)

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

    def move(self):
        self.x += self.xv
        self.y += self.yv

class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.pregnant = random.randint(0, 20) < 2  # Decreased chance

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

bricks = []
def init():
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            bricks.append(Brick(10 + j * 79, 100 + i * 35, 70, 25, (95, 192, 174)))  # Updated block color

def redrawGameWindow():
    win.fill((102, 108, 183))  # Updated background color (#666CB7)
    player.draw(win)
    for ball in balls:
        ball.draw(win)
    for b in bricks:
        b.draw(win)

    try:
        font_small = pygame.font.Font("relaxationgame\Roboto-VariableFont_wdth,wght.ttf", 22)  # Using Roboto font (adjust the path as needed)
    except:
        font_small = pygame.font.SysFont('comicsans', 22)  # Fallback to default if Roboto is not found
    
    infoText = font_small.render("Press R to Restart | Press Q to Quit", 1, (235, 220, 195))  # Updated text color (#EBDCC3)
    win.blit(infoText, (10, 10))  

    if gameover:
        try:
            font = pygame.font.Font("Roboto-Regular.ttf", 50)  # Using Roboto font (adjust the path as needed)
        except:
            font = pygame.font.SysFont('comicsans', 50)  # Fallback to default if Roboto is not found
        
        resText = font.render("Congrats!" if len(bricks) == 0 else "That's rough!", 1, (235, 220, 195))  # Updated text color (#EBDCC3)
        win.blit(resText, ((sw//2 - resText.get_width()//2), sh//2 - resText.get_height()//2))
    
    pygame.display.update()

player = Paddle(sw/2 - 50, sh -100, 140, 20, (0, 255, 100))
ball = Ball(sw/2 - 10, sh - 400, 20, 20, (255, 255, 255))
balls = [ball]
init()

run = True
while run:
    clock.tick(100)
    
    if not gameover:
        for ball in balls:
            ball.move()
        if pygame.mouse.get_pos()[0] - player.w//2 < 0:
            player.x = 0
        elif pygame.mouse.get_pos()[0] + player.w//2 > sw:
            player.x = sw - player.w
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w //2

        for ball in balls:
            if (ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                if ball.y + ball.h >= player.y:
                    ball.yv *= -1
                    ball.y = player.y - ball.h - 1
                    bounceSound.play()

            if ball.x + ball.w >= sw or ball.x < 0:
                bounceSound.play()
                ball.xv *= -1
            if ball.y <= 0:
                bounceSound.play()
                ball.yv *= -1
            if ball.y > sh:
                balls.remove(ball)

        for brick in bricks:
            for ball in balls:
                if (ball.x >= brick.x and ball.x <= brick.x + brick.w) or (ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w):
                    if (ball.y >= brick.y and ball.y <= brick.y + brick.h) or (ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y + brick.h):
                        brick.visible = False
                        if brick.pregnant:
                            balls.append(Ball(brick.x, brick.y, 20, 20, (255, 255, 255)))
                        ball.yv *= -1
                        brickHitSound.play()
                        break

        bricks = [brick for brick in bricks if brick.visible]

        if len(balls) == 0:
            gameover = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:  # Restart game
        gameover = False
        balls = [Ball(sw/2 - 10, sh - 400, 20, 20, (255, 255, 255))]  
        init()

    if keys[pygame.K_q]:  # Quit game
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()

pygame.quit()
