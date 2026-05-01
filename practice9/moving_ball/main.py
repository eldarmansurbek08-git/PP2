import pygame
pygame.init()
sc = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                running = False
    sc.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)