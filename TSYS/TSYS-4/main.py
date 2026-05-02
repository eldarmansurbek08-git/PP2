import pygame
import random
import json
import time
from db import DBManager

# Тұрақтылар
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
WHITE, BLACK, RED, GREEN, BLUE, YELLOW = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0)
POISON_COLOR = (150, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game TSIS4")
        self.clock = pygame.time.Clock()
        self.db = DBManager()
        self.load_settings()
        self.load_sounds()
        
        self.state = "MENU"
        self.username = ""
        self.reset_game()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {"snake_color": [0, 255, 0], "draw_grid": True, "sound_on": True}

    def load_sounds(self):
        try:
            self.snd_eat = pygame.mixer.Sound("assets/eat.mp3")
            self.snd_poison = pygame.mixer.Sound("assets/poison.mp3")
            self.snd_bonus = pygame.mixer.Sound("assets/bonus.mp3")
            self.snd_over = pygame.mixer.Sound("assets/gameover.mp3")
        except:
            print("Sound files not found in assets/")
            self.snd_eat = self.snd_poison = self.snd_bonus = self.snd_over = None

    def play_sound(self, sound):
        if self.settings.get("sound_on") and sound:
            sound.play()

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)
        self.score = 0
        self.level = 1
        self.speed = 10
        self.walls = []
        self.food = self.spawn_item()
        self.poison = self.spawn_item()
        self.bonus = None
        self.bonus_spawn_time = 0
        self.shield_active = False

    def spawn_item(self):
        while True:
            pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            if pos not in self.snake and pos not in self.walls:
                return pos

    def generate_walls(self):
        self.walls = []
        for _ in range(self.level * 3):
            w = self.spawn_item()
            if abs(w[0] - self.snake[0][0]) > 60:
                self.walls.append(w)

    def apply_bonus(self):
        b_type = random.choice(["SPEED", "SLOW", "SHIELD"])
        now = pygame.time.get_ticks()
        if b_type == "SPEED":
            self.speed = 20
        elif b_type == "SLOW":
            self.speed = 5
        elif b_type == "SHIELD":
            self.shield_active = True

    def update(self):
        now = pygame.time.get_ticks()
        if self.bonus and now - self.bonus_spawn_time > 8000:
            self.bonus = None

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= WIDTH or 
            new_head[1] < 0 or new_head[1] >= HEIGHT or 
            new_head in self.snake or new_head in self.walls):
            if self.shield_active:
                self.shield_active = False
            else:
                self.game_over()
                return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.play_sound(self.snd_eat)
            self.score += 10
            self.food = self.spawn_item()
            if self.score % 50 == 0:
                self.level += 1
                if self.level >= 3: self.generate_walls()
            if random.random() < 0.2: 
                self.bonus = self.spawn_item()
                self.bonus_spawn_time = now
        elif new_head == self.poison:
            self.play_sound(self.snd_poison)
            if len(self.snake) > 2:
                self.snake.pop(); self.snake.pop()
            else:
                self.game_over()
            self.poison = self.spawn_item()
        elif self.bonus and new_head == self.bonus:
            self.play_sound(self.snd_bonus)
            self.apply_bonus()
            self.bonus = None
        else:
            self.snake.pop()

    def game_over(self):
        self.play_sound(self.snd_over)
        p_id = self.db.get_player_id(self.username)
        self.db.save_game(p_id, self.score, self.level)
        self.personal_best = self.db.get_best_score(p_id)
        self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill(BLACK)
        if self.settings["draw_grid"]:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, (30, 30, 30), (0, y), (WIDTH, y))

        for seg in self.snake:
            pygame.draw.rect(self.screen, self.settings["snake_color"], (*seg, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(self.screen, GREEN, (*self.food, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, POISON_COLOR, (*self.poison, CELL_SIZE, CELL_SIZE))
        for w in self.walls:
            pygame.draw.rect(self.screen, WHITE, (*w, CELL_SIZE, CELL_SIZE))
        if self.bonus:
            pygame.draw.rect(self.screen, YELLOW, (*self.bonus, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont("Arial", 24)
        score_txt = font.render(f"Score: {self.score}  Level: {self.level}", True, WHITE)
        self.screen.blit(score_txt, (10, 10))
        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont("Arial", 40)
        title = font.render("SNAKE GAME", True, GREEN)
        input_txt = font.render(f"Name: {self.username}", True, WHITE)
        hint = font.render("Press ENTER to Start", True, BLUE)
        
        self.screen.blit(title, (WIDTH//2 - 100, 150))
        self.screen.blit(input_txt, (WIDTH//2 - 150, 250))
        self.screen.blit(hint, (WIDTH//2 - 150, 350))
        pygame.display.flip()

    def draw_game_over(self):
        self.screen.fill((50, 0, 0))
        font = pygame.font.SysFont("Arial", 40)
        self.screen.blit(font.render("GAME OVER", True, RED), (WIDTH//2-100, 150))
        self.screen.blit(font.render(f"Final Score: {self.score}", True, WHITE), (WIDTH//2-100, 220))
        self.screen.blit(font.render(f"Best: {self.personal_best}", True, YELLOW), (WIDTH//2-100, 280))
        self.screen.blit(font.render("Press M for Menu", True, WHITE), (WIDTH//2-100, 380))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.username:
                            self.state = "GAME"
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            if len(self.username) < 15:
                                self.username += event.unicode
                
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                            self.direction = (0, -CELL_SIZE)
                        if event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                            self.direction = (0, CELL_SIZE)
                        if event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                            self.direction = (-CELL_SIZE, 0)
                        if event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                            self.direction = (CELL_SIZE, 0)
                
                elif self.state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.reset_game()
                            self.state = "MENU"

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME":
                self.update()
                self.draw()
                self.clock.tick(self.speed)
            elif self.state == "GAME_OVER":
                self.draw_game_over()

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()