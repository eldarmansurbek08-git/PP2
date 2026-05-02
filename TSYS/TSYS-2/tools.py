import pygame
from collections import deque


def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        px, py = q.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)

        q.append((px + 1, py))
        q.append((px - 1, py))
        q.append((px, py + 1))
        q.append((px, py - 1))


def draw_square(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        side = -side

    rect = pygame.Rect(x1, y1, side, abs(side))
    pygame.draw.rect(surface, color, rect, size)


def draw_right_triangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    width = x2 - x1
    height = abs(width) * 0.866

    if y2 < y1:
        height = -height

    points = [
        (x1, y2),
        (x2, y2),
        ((x1 + x2) // 2, y2 - height)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    pygame.draw.polygon(surface, color, points, size)