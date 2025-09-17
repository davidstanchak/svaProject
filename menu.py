import pygame
from sys import exit
from subprocess import call
import os

def display_menu():
    pygame.init()
    pygame.display.set_caption("Scientists vs. Aliens")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill("Black")

    # Base path for assets
    base_path = os.path.join(os.path.dirname(__file__), "assets")

    # Load background image
    bg_path = os.path.join(base_path, "Backgrounds", "background.png")
    full_moon = pygame.image.load(bg_path)
    full_moon = pygame.transform.scale(full_moon, (1280, 720))

    # Title text
    font_path = os.path.join(base_path, "Font", "ka1.ttf")
    title_text_font = pygame.font.Font(font_path, 60)
    title_text_surface = title_text_font.render("Scientists vs. Aliens", True, "#5d2285")

    # Button setup
    button_rect = pygame.Rect(100, 160, 184, 64)
    button_color = "#5d2285"
    button_hover_color = "#7e3bbd"
    button_text_font = pygame.font.Font(font_path, 40)
    button_text_surface = button_text_font.render("Play", True, "White")

    running = True
    while running:
        screen.blit(full_moon, (0, 0))
        screen.blit(title_text_surface, (175, 10))

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    print("Button Pressed")
                    pygame.quit()
                    game_path = os.path.join(os.path.dirname(__file__),"main.py")
                    call(["python", game_path])
                    exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    print("hello")
    display_menu()