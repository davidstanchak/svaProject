import pygame
import random

pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")

#setting up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#function to round any surfaces
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)

#alien class
class alien:
    def __init__(self, row, cell_width, cell_height, grid_left_x, grid_top_y):
        self.row = row
        self.x = SCREEN_WIDTH
        self.y = grid_top_y + row * cell_height + (cell_height // 4)
        self.width = cell_width // 2
        self.height = self.width
        self.speed = 0.5

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0

###############

def main():
    running = True 

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

    #initialize alien rows
    aliens_by_row = [[] for _ in range(NUM_ROWS)]
    spawn_timer = 0
    spawn_interval = 500 #milliseconds

    while running:
        dt = clock.tick(60)
        spawn_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the current even type is quit, loop stops
                running = False

        screen.fill((0, 0, 0)) #main screen is filled in a black color

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
            "#5d2285",
            (margin_sides, 12.5, 550, 145),
            radius=10
        )

        #update and draw aliens
        for row in range(NUM_ROWS):
            row_aliens = aliens_by_row[row]

            for a in row_aliens:
                a.update()
                a.draw(screen)

            #remove aliens that moved off screen
            aliens_by_row[row] = [a for a in row_aliens if not a.is_off_screen()]

        #randomized spawning logic
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            random_row = random.randint(0, NUM_ROWS - 1)
            row_aliens = aliens_by_row[random_row]

            if not row_aliens or row_aliens[-1].x < SCREEN_WIDTH - random.randint(CELL_WIDTH, CELL_WIDTH * 3):
                aliens_by_row[random_row].append(alien(random_row, CELL_WIDTH, CELL_HEIGHT, GRID_LEFT_X, GRID_TOP_Y))

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()