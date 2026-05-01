import pygame
import sys
import datetime

pygame.init()

SIZE = 800
screen = pygame.display.set_mode((SIZE, SIZE))
fps_clock = pygame.time.Clock()

def scale(surf):
    return pygame.transform.scale(surf, (SIZE, SIZE))


clock_face = scale(pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/mickeys_clock/images/clock.png"))


second_img = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/mickeys_clock/images/sec.png")
minute_img = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/mickeys_clock/images/min.png")
hour_img   = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/mickeys_clock/images/hour.png")

CENTER = (SIZE // 2, SIZE // 2)

HOUR_NATURAL = 270
MINUTE_NATURAL = 57
SECOND_NATURAL = 225



def rotate_hand(img, target_angle, natural_angle):
    rotation = -(target_angle - natural_angle)
    rotated = pygame.transform.rotate(img, rotation)
    rect = rotated.get_rect(center=CENTER)
    return rotated, rect

def get_time_angles():
    now = datetime.datetime.now()
    h = now.hour % 12
    m = now.minute
    s = now.second
    ms = now.microsecond / 1_000_000

    second_angle = (s + ms) * 6
    minute_angle = m * 6 + s * 0.1
    hour_angle = h * 30 + m * 0.5

    return hour_angle, minute_angle, second_angle

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    hour_angle, minute_angle, second_angle = get_time_angles()

    screen.blit(clock_face, (0, 0))

    h_surf, h_rect = rotate_hand(hour_img, hour_angle, HOUR_NATURAL)
    m_surf, m_rect = rotate_hand(minute_img, minute_angle, MINUTE_NATURAL)
    s_surf, s_rect = rotate_hand(second_img, second_angle, SECOND_NATURAL)

    screen.blit(h_surf, h_rect)
    screen.blit(m_surf, m_rect)
    screen.blit(s_surf, s_rect)

    pygame.display.flip()
    fps_clock.tick(60)