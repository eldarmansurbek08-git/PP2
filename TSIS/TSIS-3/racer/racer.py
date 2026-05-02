
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

fps = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
COINS_SCORE = 0  


font = pygame.font.SysFont("Verdana", 20)


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")


pygame.mixer.init()
coin_sound = pygame.mixer.Sound("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/racer/coin.mp3")
pygame.mixer.init()
gameover_sound = pygame.mixer.Sound("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/racer/gameover.mp3")


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/racer/coin.jpeg")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        while True:
            x = random.randint(40, SCREEN_WIDTH-40)

            if abs(x - E1.rect.centerx) > 60:
                break

        self.rect.center = (x, -100)
        self.weight = random.randint(1, 3)
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/racer/Enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-50, -50)
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/racer/Player.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(160, 520))
        self.rect.inflate_ip(-50, -50)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)



P1 = Player()
E1 = Enemy()
C1 = Coin()

start_time = pygame.time.get_ticks()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)


while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)

    # SCORE 
    scores = font.render(f"Coins: {COINS_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (SCREEN_WIDTH - 130, 10))

    # DRAW + MOVE
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # COIN COLLISION
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_SCORE += C1.weight
        coin_sound.play()   
        C1.reset()

    # ENEMY COLLISION
    if pygame.time.get_ticks() - start_time > 2000:
        if pygame.sprite.spritecollideany(P1, enemies):
            gameover_sound.play()
            big_font = pygame.font.SysFont("Verdana", 60, bold=True)
            DISPLAYSURF.fill(BLACK)

            game_over_text = big_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2 - 1, SCREEN_HEIGHT//2 - 1))
            DISPLAYSURF.blit(game_over_text, text_rect)

            pygame.display.update()
            time.sleep(3.3)

            pygame.quit()
            sys.exit()
            

    pygame.display.update()
    FramePerSec.tick(fps)