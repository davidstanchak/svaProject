import pygame

pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Fixed vertical placement for the grid
grid_y, grid_h = 170, 530
cols, rows = 9, 5

# Compute margin so side gaps == bottom gap
bottom_margin = screen_height - (grid_y + grid_h)
side_margin = bottom_margin

# Apply that margin to left/right
grid_x = side_margin
grid_w = screen_width - 2 * side_margin

cell_w = grid_w // cols
cell_h = grid_h // rows

# Shop panel aligned to the same left margin
shop_x, shop_y, shop_w, shop_h = side_margin, 10, 500, 150

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw the main grid background
        draw_rounded_rect(
            screen,
            (213, 128, 75),
            (grid_x, grid_y, grid_w, grid_h),
            radius=5
        )

        # Draw grid cells
        for row in range(rows):
            for col in range(cols):
                x = grid_x + col * cell_w
                y = grid_y + row * cell_h
                color = (183, 98, 45) if (row + col) % 2 == 0 else (213, 128, 75)
                draw_rounded_rect(
                    screen,
                    color,
                    (x, y, cell_w + 7, cell_h),
                    radius=5
                )
                
        # Draw the shop panel
        draw_rounded_rect(
            screen,
            (123, 64, 163),
            (shop_x, shop_y, shop_w, shop_h),
            radius=10
        )

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()