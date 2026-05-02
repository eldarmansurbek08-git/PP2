import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1000, 650
TOOLBAR_WIDTH = 140
PALETTE_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
DARK_GRAY = (40, 40, 40)
BLUE = (70, 130, 255)

palette_colors = [
   (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),
   (255,255,0),(255,0,255),(0,255,255),(128,0,0),(0,128,0),
   (0,0,128),(128,128,0),(128,0,128),(0,128,128)
]

font = pygame.font.SysFont("Segoe UI", 14, bold=True)

current_color = (0, 0, 0)
tool = "brush"
brush_size = 5

drawing = False
start_pos = None
preview_surface = None

canvas = pygame.Surface((WIDTH - TOOLBAR_WIDTH, HEIGHT - PALETTE_HEIGHT))
canvas.fill(WHITE)

tools = ["brush", "rectangle", "circle", "eraser"]

# UI
def draw_toolbar():
   pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_WIDTH, HEIGHT))
   for i, t in enumerate(tools):
      y = 50 + i * 70
      rect = pygame.Rect(20, y, 100, 50)

      color = BLUE if t == tool else DARK_GRAY
      pygame.draw.rect(screen, color, rect, border_radius=10)

      txt = font.render(t.upper(), True, WHITE)
      screen.blit(txt, (rect.x + 10, rect.y + 15))

def draw_palette():
   pygame.draw.rect(screen, GRAY, (TOOLBAR_WIDTH, HEIGHT - PALETTE_HEIGHT, WIDTH, PALETTE_HEIGHT))

   for i, color in enumerate(palette_colors):
      x = TOOLBAR_WIDTH + 10 + i * 60
      y = HEIGHT - 60
      rect = pygame.Rect(x, y, 40, 40)

      pygame.draw.rect(screen, color, rect, border_radius=8)

      if color == current_color:
         pygame.draw.rect(screen, BLUE, rect, 3, border_radius=8)

def draw_info():
   txt = font.render(f"{tool} | size: {brush_size}", True, DARK_GRAY)
   screen.blit(txt, (TOOLBAR_WIDTH + 10, 10))

# LOOP
while True:
   screen.fill((200, 200, 200))

   # отображение холста
   if preview_surface:
      screen.blit(preview_surface, (TOOLBAR_WIDTH, 0))
   else:
      screen.blit(canvas, (TOOLBAR_WIDTH, 0))

   draw_toolbar()
   draw_palette()
   draw_info()

   for event in pygame.event.get():

      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

      # МЫШЬ НАЖАТА
      if event.type == pygame.MOUSEBUTTONDOWN:
         x, y = event.pos

         # тулбар
         if x < TOOLBAR_WIDTH:
            for i, t in enumerate(tools):
               if 50 + i*70 <= y <= 100 + i*70:
                  tool = t

         # палитра
         elif y > HEIGHT - PALETTE_HEIGHT:
            for i, color in enumerate(palette_colors):
               px = TOOLBAR_WIDTH + 10 + i*60
               if px <= x <= px + 40:
                  current_color = color

         else:
            drawing = True
            start_pos = (x - TOOLBAR_WIDTH, y)

      # ОТПУСТИЛ МЫШЬ
      if event.type == pygame.MOUSEBUTTONUP:
         if drawing:
               x, y = event.pos
               x -= TOOLBAR_WIDTH

               if tool == "rectangle":
                  rect = pygame.Rect(start_pos, (x - start_pos[0], y - start_pos[1]))
                  pygame.draw.rect(canvas, current_color, rect, 2)

               elif tool == "circle":
                  dx = x - start_pos[0]
                  dy = y - start_pos[1]
                  radius = int((dx**2 + dy**2)**0.5)
                  pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

         drawing = False
         preview_surface = None

      # ДВИЖЕНИЕ МЫШИ
      if event.type == pygame.MOUSEMOTION and drawing:
         x, y = event.pos
         x -= TOOLBAR_WIDTH

         if tool == "brush":
            pygame.draw.circle(canvas, current_color, (x, y), brush_size)

         elif tool == "eraser":
            pygame.draw.circle(canvas, WHITE, (x, y), brush_size + 5)

         elif tool in ["rectangle", "circle"]:
            preview_surface = canvas.copy()

            if tool == "rectangle":
               rect = pygame.Rect(start_pos, (x - start_pos[0], y - start_pos[1]))
               pygame.draw.rect(preview_surface, current_color, rect, 2)

            elif tool == "circle":
               dx = x - start_pos[0]
               dy = y - start_pos[1]
               radius = int((dx**2 + dy**2)**0.5)
               pygame.draw.circle(preview_surface, current_color, start_pos, radius, 2)

      # КОЛЁСИКО
      if event.type == pygame.MOUSEWHEEL:
         brush_size += event.y
         brush_size = max(1, min(50, brush_size))

   pygame.display.flip()
   clock.tick()