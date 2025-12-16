import pygame
from sys import exit
from subprocess import call
import os
import main

def display_menu():
    pygame.init()
    pygame.display.set_caption("Scientists vs. Aliens")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill("Black")

    #base path for assets
    base_path = os.path.join(os.path.dirname(__file__), "assets")

    #load background image
    bg_path = os.path.join(base_path, "Backgrounds", "background.png")
    full_moon = pygame.image.load(bg_path)
    full_moon = pygame.transform.scale(full_moon, (1280, 720))

    #title text
    font_path =os.path.join(base_path, "Font", "ka1.ttf")
    title_text_font = pygame.font.Font(font_path, 60)
    title_text_surface = title_text_font.render("Scientists vs. Aliens", False, "#5d2285")

    #button setup
    button_rect = pygame.Rect(550, 290, 180, 70)
    button_color = "#5d2285"
    button_hover_color = "#7e3bbd"

    #play button text using Arial
    play_font = pygame.font.SysFont("Arial", 30)
    play_text_surface = play_font.render("PLAY", True, "White")
    play_text_rect = play_text_surface.get_rect(center=button_rect.center)

    running = True
    while running:
        screen.blit(full_moon, (0, 0))
        screen.blit(title_text_surface, (175, 10))

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        #drawing "PLAY" on button
        screen.blit(play_text_surface, play_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    print("Button Pressed")
                    main.main()
                    screen.fill("Black")

        pygame.display.update()
        clock.tick(60)


display_menu()