import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TEST WINDOW")

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))  # қара экран

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()