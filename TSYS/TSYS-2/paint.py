import pygame
from datetime import datetime
from tools import flood_fill, draw_square, draw_right_triangle, draw_equilateral_triangle, draw_rhombus


pygame.init()

WIDTH = 1000
HEIGHT = 700
TOOLBAR = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("arial", 22)
small_font = pygame.font.SysFont("arial", 18)

tool = "pencil"
color = (0, 0, 0)
brush_size = 5

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (255, 255, 255)
]

drawing = False
start_pos = None
last_pos = None
text_mode = False
text_pos = None
text_value = ""

clock = pygame.time.Clock()
running = True


def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR))

    x = 10
    for c in colors:
        pygame.draw.rect(screen, c, (x, 10, 35, 35))
        pygame.draw.rect(screen, (0, 0, 0), (x, 10, 35, 35), 2)
        x += 45

    info = f"Tool: {tool} | Size: {brush_size}"
    text = small_font.render(info, True, (0, 0, 0))
    screen.blit(text, (10, 60))

def draw_controls():
    controls = [
        "P pencil  L line  R rect  C circle  E eraser",
        "F fill    T text  S square  H triangle",
        "G eq-triangle  D rhombus",
        "1 small  2 medium  3 large",
        "Ctrl+S save  Enter OK  Esc cancel"
    ]

    y = 5
    for line in controls:
        text = small_font.render(line, True, (0, 0, 0))
        screen.blit(text, (400, y))
        y += 18

def pick_color(pos):
    global color

    x, y = pos

    if y > 45:
        return

    start_x = 10

    for i in range(len(colors)):
        rect = pygame.Rect(start_x + i * 45, 10, 35, 35)
        if rect.collidepoint(pos):
            color = colors[i]


def save_canvas():
    name = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, name)
    print("Saved:", name)


def draw_preview(temp, start, end):
    if tool == "line":
        pygame.draw.line(temp, color, start, end, brush_size)

    elif tool == "rectangle":
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        pygame.draw.rect(temp, color, rect, brush_size)

    elif tool == "circle":
        radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
        pygame.draw.circle(temp, color, start, radius, brush_size)

    elif tool == "square":
        draw_square(temp, color, start, end, brush_size)

    elif tool == "right_triangle":
        draw_right_triangle(temp, color, start, end, brush_size)

    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(temp, color, start, end, brush_size)

    elif tool == "rhombus":
        draw_rhombus(temp, color, start, end, brush_size)


while running:
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] and event.key == pygame.K_s:
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_value, True, color)
                    canvas.blit(text_surface, text_pos)
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_h:
                    tool = "right_triangle"
                elif event.key == pygame.K_g:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_d:
                    tool = "rhombus"
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < TOOLBAR:
                pick_color(event.pos)
            else:
                pos = canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], color)

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    text_value = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = canvas_pos(event.pos)

                if tool == "line":
                    pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

                elif tool == "rectangle":
                    rect = pygame.Rect(start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, rect, brush_size)

                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

                elif tool == "square":
                    draw_square(canvas, color, start_pos, end_pos, brush_size)

                elif tool == "right_triangle":
                    draw_right_triangle(canvas, color, start_pos, end_pos, brush_size)

                elif tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, color, start_pos, end_pos, brush_size)

                elif tool == "rhombus":
                    draw_rhombus(canvas, color, start_pos, end_pos, brush_size)

                drawing = False

    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, TOOLBAR))

    if drawing and tool in ["line", "rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
        temp = canvas.copy()
        draw_preview(temp, start_pos, canvas_pos(mouse_pos))
        screen.blit(temp, (0, TOOLBAR))

    if text_mode:
        temp_text = font.render(text_value, True, color)
        screen.blit(temp_text, (text_pos[0], text_pos[1] + TOOLBAR))

    draw_toolbar()
    draw_controls()
    pygame.display.flip()

pygame.quit()