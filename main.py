import pygame

pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")
screen = pygame.display.set_mode((1280, 720))

grid_x, grid_y, grid_w, grid_h = 40, 170, 1200, 530
cols, rows = 9, 5
cell_w = grid_w // cols
cell_h = grid_h // rows

shop_x, shop_y, shop_w, shop_h = 40, 10, 500, 150

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_rounded_rect(screen, (213, 128, 75), (grid_x, grid_y, grid_w, grid_h), 5)

        for row in range(rows):
            for col in range(cols):
                x = grid_x + col * cell_w
                y = grid_y + row * cell_h
                if (row + col) % 2 == 0:
                    color = (183, 98, 45)
                else:
                    color = (213, 128, 75)
                draw_rounded_rect(screen, color, (x, y, cell_w+3, cell_h), 5)

        draw_rounded_rect(screen, (123, 64, 163), (shop_x, shop_y, shop_w, shop_h), 10)

        pygame.display.flip()
    pygame.quit()
    
main()