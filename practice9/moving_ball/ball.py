import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

x = 300
y = 200

radius = 25
step = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if x - step >= radius:
                    x -= step

            if event.key == pygame.K_RIGHT:
                if x + step <= WIDTH - radius:
                    x += step

            if event.key == pygame.K_UP:
                if y - step >= radius:
                    y -= step

            if event.key == pygame.K_DOWN:
                if y + step <= HEIGHT - radius:
                    y += step

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.update()

pygame.quit()