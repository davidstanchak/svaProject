import pygame
import random
import math

# -----------------------------------------------------------
# INITIAL SETUP
# Initializes the game window, screen, and clock.
# -----------------------------------------------------------
pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


# -----------------------------------------------------------
# FUNCTION: draw_rounded_rect
# Simple helper function to draw rectangles with rounded corners.
# -----------------------------------------------------------
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)


# -----------------------------------------------------------
# CLASS: Alien
# Represents one alien moving horizontally across a grid row.
# -----------------------------------------------------------
class alien:
    def __init__(self, row, cell_width, cell_height, grid_origin_x, grid_origin_y):
        self.row = row
        self.x = SCREEN_WIDTH
        self.y = grid_origin_y + row * cell_height + (cell_height // 4)
        self.width = cell_width // 2
        self.height = self.width
        self.speed = 0.5  # movement speed

    def update(self):
        self.x -= self.speed  # move left every frame

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0  # if alien is completely off screen


# -----------------------------------------------------------
# CLASS: FloatingBall
# Floating balls that wander around and give money when clicked.
# -----------------------------------------------------------
class FloatingBall:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(200, SCREEN_HEIGHT - 100)
        self.radius = 10
        self.dx = random.uniform(-0.5, 0.5)
        self.dy = random.uniform(-0.5, 0.5)

    def update(self):
        # Move the ball and bounce off edges
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.dx *= -1
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y)), self.radius)

    def is_near_mouse(self, mouse_pos):
        dist = math.hypot(self.x - mouse_pos[0], self.y - mouse_pos[1])
        return dist < 30


# -----------------------------------------------------------
# CLASS: PlaceableItem
# Represents a draggable item (like towers) that can be placed
# onto grid cells and optionally spawn objects over time.
# -----------------------------------------------------------
class PlaceableItem:
    def __init__(self, x, y, width, height, item_type="blue"):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dragging = False
        self.placed_items = []   # list of placed positions
        self.type = item_type
        self.spawn_timers = []   # timers for spawned objects

    def start_drag(self):
        self.dragging = True

    def stop_drag(self, grid_origin_x, grid_origin_y, cell_width, cell_height, num_columns, num_rows, player_money):
        self.dragging = False

        # Determine which grid cell the item was dropped into
        col = (self.x - grid_origin_x + self.width // 2) // cell_width
        row = (self.y - grid_origin_y + self.height // 2) // cell_height

        # Clamp to valid grid indices
        col = max(0, min(num_columns - 1, col))
        row = max(0, min(num_rows - 1, row))

        # Snap position to grid
        snap_x = grid_origin_x + col * cell_width + (cell_width - self.width) // 2
        snap_y = grid_origin_y + row * cell_height + (cell_height - self.height) // 2

        # Only place if the player has enough money
        if player_money >= 10:
            self.placed_items.append((snap_x, snap_y))
            self.spawn_timers.append(0)
            player_money -= 10

        # Return item back to original place
        self.x = self.original_x
        self.y = self.original_y

        return player_money

    def update_position(self, mouse_pos):
        if self.dragging:
            self.x = mouse_pos[0] - self.width // 2
            self.y = mouse_pos[1] - self.height // 2

    def draw(self, surface):
        color = (0, 0, 255) if self.type == "blue" else (0, 0, 0)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        for px, py in self.placed_items:
            pygame.draw.rect(surface, color, (px, py, self.width, self.height))

    def draw_preview(self, surface, grid_origin_x, grid_origin_y, cell_width, cell_height, num_columns, num_rows):
        if self.dragging:
            # Preview which cell the item would land in
            col = (self.x - grid_origin_x + self.width // 2) // cell_width
            row = (self.y - grid_origin_y + self.height // 2) // cell_height

            col = max(0, min(num_columns - 1, col))
            row = max(0, min(num_rows - 1, row))

            snap_x = grid_origin_x + col * cell_width + (cell_width - self.width) // 2
            snap_y = grid_origin_y + row * cell_height + (cell_height - self.height) // 2

            preview_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            preview_surface.fill((0, 0, 255, 100) if self.type == "blue" else (0, 0, 0, 100))
            surface.blit(preview_surface, (snap_x, snap_y))

    def spawn_ball_if_needed(self, dt, balls):
        # Only the "black" item type spawns currency balls
        if self.type != "black":
            return  

        for i in range(len(self.spawn_timers)):
            self.spawn_timers[i] += dt
            # Spawn ball every 2 seconds
            if self.spawn_timers[i] >= 2000:
                self.spawn_timers[i] = 0
                px, py = self.placed_items[i]
                ball = FloatingBall()
                ball.x = px + self.width // 2
                ball.y = py + self.height // 2
                balls.append(ball)


# -----------------------------------------------------------
# MAIN GAME LOOP
# Handles:
# - Game initialization
# - Drawing UI
# - Alien spawning cycles
# - Money collection
# - Player input and dragging
# -----------------------------------------------------------
def main():
    running = True

    # Grid parameters (9x5 play area)
    NUM_COLUMNS, NUM_ROWS = 9, 5
    GRID_ORIGIN_Y = 170
    GRID_HEIGHT = 530
    margin_bottom = SCREEN_HEIGHT - (GRID_ORIGIN_Y + GRID_HEIGHT)
    margin_sides = margin_bottom
    GRID_ORIGIN_X = margin_sides
    GRID_WIDTH = SCREEN_WIDTH - 2 * margin_sides

    CELL_WIDTH = GRID_WIDTH // NUM_COLUMNS
    CELL_HEIGHT = GRID_HEIGHT // NUM_ROWS

    # Each row stores a list of active aliens in that lane
    aliens_by_row = [[] for _ in range(NUM_ROWS)]

    spawn_timer = 0
    spawn_interval = 500
    spawn_cycle_timer = 0
    spawn_phase_duration = 2000
    break_phase_duration = 6000
    spawning_active = False
    alien_spawn_delay = 7000  # 7 seconds

    # Player starting money
    player_money = 0

    # Fonts
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 24)

    # Ball spawning system
    balls = []
    ball_spawn_timer = 0
    ball_spawn_interval = 3000

    game_started = True

    while running:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        spawn_timer += dt
        spawn_cycle_timer += dt
        ball_spawn_timer += dt

        if current_time >= alien_spawn_delay:
            if spawn_cycle_timer >= (spawn_phase_duration if spawning_active else break_phase_duration):
                spawn_cycle_timer = 0
                spawning_active = not spawning_active

        # -----------------------------------------------------------
        # EVENT HANDLING: mouse input and dragging logic
        # -----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()

        # -----------------------------------------------------------
        # DRAW BACKGROUND AND GRID
        # -----------------------------------------------------------
        screen.fill((0, 0, 0))##################
        draw_rounded_rect(screen, "#2C363F", (GRID_ORIGIN_X, GRID_ORIGIN_Y, GRID_WIDTH, GRID_HEIGHT), radius=5)

        # Draw grid cells
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                cell_color = "#333333" if (row + col) % 2 == 0 else "#535657"
                draw_rounded_rect(
                    screen,
                    cell_color,
                    (
                        GRID_ORIGIN_X + col * CELL_WIDTH,
                        GRID_ORIGIN_Y + row * CELL_HEIGHT,
                        CELL_WIDTH + 7,
                        CELL_HEIGHT
                    ),
                    radius=5
                )
#######################
        # -----------------------------------------------------------
        # TOP UI BAR (shop area + money display)
        # -----------------------------------------------------------
        draw_rounded_rect(screen, "#2F3061", (margin_sides, 12.5, 550, 145), radius=10) ############################
        money_box_width = 120
        money_box_x = margin_sides + 550 + 20
        draw_rounded_rect(screen, "#2F3061", (money_box_x, 12.5, money_box_width, 145), radius=10)

        money_text = font.render(f"{player_money}", True, (255, 255, 255))
        text_rect = money_text.get_rect(center=(money_box_x + money_box_width // 2, 12.5 + 145 // 2))
        screen.blit(money_text, text_rect)
########################

        # -----------------------------------------------------------
        # UPDATE AND DRAW ALIENS
        # -----------------------------------------------------------
        for row in range(NUM_ROWS):
            row_aliens = aliens_by_row[row]
            for a in row_aliens:
                a.update()
                a.draw(screen)

            # Remove aliens that have gone off screen
            aliens_by_row[row] = [a for a in row_aliens if not a.is_off_screen()]

        # Spawn a new alien periodically while active
        if spawning_active and spawn_timer >= spawn_interval:
            spawn_timer = 0
            random_row = random.randint(0, NUM_ROWS - 1)
            row_aliens = aliens_by_row[random_row]

            if not row_aliens or row_aliens[-1].x < SCREEN_WIDTH - random.randint(CELL_WIDTH, CELL_WIDTH * 3):
                aliens_by_row[random_row].append(
                    alien(random_row, CELL_WIDTH, CELL_HEIGHT, GRID_ORIGIN_X, GRID_ORIGIN_Y)
                )

        # -----------------------------------------------------------
        # FLOATING BALL SPAWNING AND COLLECTION
        # -----------------------------------------------------------
        if ball_spawn_timer >= ball_spawn_interval:     #######################
            ball_spawn_timer = 0
            balls.append(FloatingBall())

        # item_black.spawn_ball_if_needed(dt, balls)

        for ball in balls[:]: #######################
            ball.update()
            ball.draw(screen)

            # Collect if close to mouse cursor
            if ball.is_near_mouse(mouse_pos): #######################
                player_money += 5
                balls.remove(ball)

        pygame.display.update()

    pygame.quit()


main()