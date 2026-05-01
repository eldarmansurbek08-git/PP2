
import pygame

# 1. Инициализация
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

# Музыка тізімі
playlist = [
    "/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/music_player/music/Sombr - 12 to 12.mp3",
    "/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/music_player/music/Sombr - Back to friends.mp3",
    "/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/music_player/music/Sombr-Homewrecker.mp3"
]

current_index = 0
pygame.mixer.music.load(playlist[current_index])

# Фон және қаріп
font = pygame.font.Font(None, 36)
bg = pygame.image.load("/Users/eldar.mansurbek21.06icloud.com/Desktop/KBTU/pp2/practices/practice9/music_player/sombr.jpg")
bg = pygame.transform.scale(bg, (600, 400))

running = True
is_playing = False

while running:
    screen.blit(bg, (0, 0))
    
    # Экранға ақпарат шығару
    song_name = playlist[current_index].split("/")[-1]
    text = font.render(f"Song: {song_name}", True, (255, 255, 255))
    screen.blit(text, (20, 300))
    
    hint = font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (0, 255, 0))
    screen.blit(hint, (20, 350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # P - Play 
            if event.key == pygame.K_p:
                pygame.mixer.music.play()
                is_playing = True
            
            # S - Stop 
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False
            
            # N - Next 
            if event.key == pygame.K_n:
                current_index = (current_index + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_index])
                pygame.mixer.music.play()
                is_playing = True
                
            # B - Back 
            if event.key == pygame.K_b:
                current_index = (current_index - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_index])
                pygame.mixer.music.play()
                is_playing = True
            
            # Q - Quit 
            if event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()