import pygame
import random

pygame.init()

# Дыбыстарды жүктеу
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/snake/eat.mp3")
crash_sound = pygame.mixer.Sound("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice10/snake/gameover.mp3")

# Экран өлшемдері
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Enhanced")

# Түстер
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
yellow = (255, 255, 0)

clock = pygame.time.Clock()

snake_block = 20
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

def show_score(score, level):
    """Ұпай мен деңгейді экранға шығару функциясы"""
    value = score_font.render("Score: " + str(score) + "  Level: " + str(level), True, yellow)
    screen.blit(value, [10, 10])

def message(msg, color):
    """Ойын аяқталғанда шығатын хабарлама"""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def game_loop():
    game_over = False
    game_close = False

    # Бастапқы позиция
    x = width // 2
    y = height // 2

    x_change = 0
    y_change = 0

    snake = []
    length = 1
    
    score = 0
    level = 1
    current_speed = 10 # Бастапқы жылдамдық

    # Тамақтың алғашқы орны
    foodx = random.randrange(0, width - snake_block, snake_block)
    foody = random.randrange(0, height - snake_block, snake_block)

    while not game_over:

        while game_close:
            screen.fill(black)
            message("Game Over! Q-Quit or C-Play Again", red)
            show_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        # Қабырғаға соғылуды тексеру
        if x >= width or x < 0 or y >= height or y < 0:
            crash_sound.play()
            game_close = True
            
        x += x_change
        y += y_change
        screen.fill(black)

        # Тамақты салу
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        # Жыланның басын есептеу
        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > length:
            del snake[0]

        # Өз-өзіне соғылуды тексеру
        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        # Жыланды салу
        for segment in snake:
            pygame.draw.rect(screen, white, [segment[0], segment[1], snake_block, snake_block])

        # Интерфейсті жаңарту
        show_score(score, level)
        pygame.display.update()

        # Тамақ жеген сәт
        if x == foodx and y == foody:
            eat_sound.play()
            score += 1
            length += 1
            
            # Деңгей мен жылдамдықты арттыру (әр 3 тамақ сайын)
            if score % 3 == 0:
                level += 1
                current_speed += 3 

            # Тамақтың жаңа орнын табу (жыланның үстіне түспеуін қадағалау)
            while True:
                foodx = random.randrange(0, width - snake_block, snake_block)
                foody = random.randrange(0, height - snake_block, snake_block)
                if [foodx, foody] not in snake:
                    break

        clock.tick(current_speed)

    pygame.quit()
    quit()

game_loop()