import pygame
from sys import exit

def menu():
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Menu')

    font = pygame.font.Font(None, 50)
    text_surf = font.render('Press ENTER to start the game', True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    running = True
    while running:
        display_surface.fill((0, 0, 0))  # Black background
        display_surface.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press ENTER to start the game
                    running = False  # This will exit the menu and continue to the game

        pygame.display.update()

if __name__ == "__main__":
    menu()
