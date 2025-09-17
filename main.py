import pygame

pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")

#setting up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#function to round any surfaces
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)

# def alien_spawn():

    

def main():
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the current even type is quit, loop stops
                running = False

        screen.fill((0, 0, 0)) #main screen is filled in a black color

        #grid layout settings
        NUM_COLUMNS, NUM_ROWS = 9, 5 #format of grid
        GRID_TOP_Y = 170 
        GRID_HEIGHT = 530

        margin_bottom = SCREEN_HEIGHT - (GRID_TOP_Y + GRID_HEIGHT)
        margin_sides = margin_bottom

        GRID_LEFT_X = margin_sides
        GRID_WIDTH = SCREEN_WIDTH - 2 * margin_sides

        CELL_WIDTH = GRID_WIDTH // NUM_COLUMNS
        CELL_HEIGHT = GRID_HEIGHT // NUM_ROWS

        #calling function to draw AND round a rectangle
        draw_rounded_rect(
            screen,
            (213, 128, 75), 
            (GRID_LEFT_X, GRID_TOP_Y, GRID_WIDTH, GRID_HEIGHT),
            radius=5
        )

        #
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS): 
                cell_color = (183, 98, 45) if (row + col) % 2 == 0 else (213, 128, 75)
                #calling function to draw AND round all individual grid squares.
                draw_rounded_rect(
                    screen,
                    cell_color,
                    (
                        GRID_LEFT_X + col * CELL_WIDTH, #each grid square is placed
                        GRID_TOP_Y + row * CELL_HEIGHT, 
                        CELL_WIDTH + 7,  #stationary width and height
                        CELL_HEIGHT
                    ),
                    radius=5
                )
        #calling function to draw AND round a shop rectangle
        draw_rounded_rect(
            screen,
            (153, 102, 204),
            (margin_sides, margin_bottom/2, 500, 150),
            radius=10
        )

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
