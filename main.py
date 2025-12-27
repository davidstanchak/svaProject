import pygame
import random
import math

# -----------------------------------------------------------
# INITIAL SETUP
# Initializes the game window, screen, and clock.
# -----------------------------------------------------------
pygame.display.set_caption("Scientists vs. Aliens")

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

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
class Alien:
    def __init__(self, row, cell_width, cell_height, grid_origin_x, grid_origin_y):
        self.row = row
        self.x = SCREEN_WIDTH
        self.y = grid_origin_y + row * cell_height + (cell_height // 4)
        self.width = cell_width // 2
        self.height = self.width
        self.speed = 0.5  # movement speed
        self.health = 3  # takes 3 hits to die
        self.alpha = 255  # full opacity

    def update(self):
        self.x -= self.speed  # move left every frame

    def draw(self, surface):
        alien_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(alien_surface, (0, 255, 0, self.alpha), (0, 0, self.width, self.height))
        surface.blit(alien_surface, (self.x, self.y))

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
# CLASS: Laser
# Represents a laser shot from blue items towards aliens.
# -----------------------------------------------------------


class Laser:
    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.row = row
        self.width = 10
        self.height = 5
        self.speed = 5  # move right

    def update(self):
        self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x > SCREEN_WIDTH

    def collides_with(self, alien):
        return (self.x < alien.x + alien.width and
                self.x + self.width > alien.x and
                self.y < alien.y + alien.height and
                self.y + self.height > alien.y)


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
        self.shoot_timers = []   # timers for shooting lasers (blue only)

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
        cost = 10 if self.type == "blue" else 15
        if player_money >= cost:
            self.placed_items.append((snap_x, snap_y))
            self.spawn_timers.append(0)
            self.shoot_timers.append(0)
            player_money -= cost

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
            # Spawn ball every 3.25 seconds
            if self.spawn_timers[i] >= 3250:
                self.spawn_timers[i] = 0
                px, py = self.placed_items[i]
                ball = FloatingBall()
                ball.x = px + self.width // 2
                ball.y = py + self.height // 2
                balls.append(ball)

    def shoot_lasers_if_needed(self, dt, lasers, grid_origin_y, cell_height):
        # Only the "blue" item type shoots lasers
        if self.type != "blue":
            return

        for i in range(len(self.shoot_timers)):
            self.shoot_timers[i] += dt
            # Shoot laser every 1 second
            if self.shoot_timers[i] >= 1000:
                self.shoot_timers[i] = 0
                px, py = self.placed_items[i]
                # Calculate row from y position
                row = (py - grid_origin_y) // cell_height
                laser = Laser(px + self.width, py + self.height // 2 - 2.5, row)
                lasers.append(laser)


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
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
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
    alien_spawn_delay = 11000  # 11 seconds

    # Draggable item buttons
    item_blue = PlaceableItem(margin_sides + 20, 40, CELL_WIDTH // 2, CELL_HEIGHT // 2, "blue")
    item_black = PlaceableItem(margin_sides + 120, 40, CELL_WIDTH // 2, CELL_HEIGHT // 2, "black")

    # Player starting money
    player_money = 0

    # Fonts
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 24)

    # Ball spawning system
    balls = []
    ball_spawn_timer = 0
    ball_spawn_interval = 3000

    # Laser system
    lasers = []

    game_started = True
    game_over = False
    game_over_time = 0

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if item_blue.x <= mouse_x <= item_blue.x + item_blue.width and item_blue.y <= mouse_y <= item_blue.y + item_blue.height:
                    item_blue.start_drag()
                elif item_black.x <= mouse_x <= item_black.x + item_black.width and item_black.y <= mouse_y <= item_black.y + item_black.height:
                    item_black.start_drag()

            elif event.type == pygame.MOUSEBUTTONUP:
                if item_blue.dragging:
                    player_money = item_blue.stop_drag(GRID_ORIGIN_X, GRID_ORIGIN_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS, player_money)
                if item_black.dragging:
                    player_money = item_black.stop_drag(GRID_ORIGIN_X, GRID_ORIGIN_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS, player_money)

        mouse_pos = pygame.mouse.get_pos()
        item_blue.update_position(mouse_pos)
        item_black.update_position(mouse_pos)

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
        # TOP UI BAR (item buttons + money display)
        # -----------------------------------------------------------
        draw_rounded_rect(screen, "#2F3061", (margin_sides, 12.5, 550, 145), radius=10) ############################
        money_box_width = 120
        money_box_x = margin_sides + 550 + 20
        draw_rounded_rect(screen, "#2F3061", (money_box_x, 12.5, money_box_width, 145), radius=10)

        money_text = font.render(f"{player_money}", True, (255, 255, 255))
        text_rect = money_text.get_rect(center=(money_box_x + money_box_width // 2, 12.5 + 145 // 2))
        screen.blit(money_text, text_rect)
########################
        item_blue.draw_preview(screen, GRID_ORIGIN_X, GRID_ORIGIN_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS)
        item_black.draw_preview(screen, GRID_ORIGIN_X, GRID_ORIGIN_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS)
        item_blue.draw(screen)
        item_black.draw(screen)

        # Draw lasers
        for laser in lasers:
            laser.draw(screen)

        # Prices under each item
        cost_text_blue = small_font.render("10", True, (255, 255, 255))
        cost_rect_blue = cost_text_blue.get_rect(center=(item_blue.x + item_blue.width // 2, item_blue.y + item_blue.height + 12))
        screen.blit(cost_text_blue, cost_rect_blue)

        cost_text_black = small_font.render("15", True, (255, 255, 255))
        cost_rect_black = cost_text_black.get_rect(center=(item_black.x + item_black.width // 2, item_black.y + item_black.height + 12))
        screen.blit(cost_text_black, cost_rect_black)

        # -----------------------------------------------------------
        # UPDATE AND DRAW ALIENS
        # -----------------------------------------------------------
        for row in range(NUM_ROWS):
            row_aliens = aliens_by_row[row]
            for a in row_aliens:
                a.update()
                if a.x <= 0:
                    game_over = True
                    if game_over_time == 0:
                        game_over_time = pygame.time.get_ticks()
                if not game_over:
                    a.draw(screen)

            # Remove aliens that have gone off screen
            aliens_by_row[row] = [a for a in row_aliens if not a.is_off_screen()]

        # Spawn a new alien periodically while active
        if not game_over and spawning_active and spawn_timer >= spawn_interval:
            spawn_timer = 0
            random_row = random.randint(0, NUM_ROWS - 1)
            row_aliens = aliens_by_row[random_row]

            if not row_aliens or row_aliens[-1].x < SCREEN_WIDTH - random.randint(CELL_WIDTH, CELL_WIDTH * 3):
                aliens_by_row[random_row].append(
                    Alien(random_row, CELL_WIDTH, CELL_HEIGHT, GRID_ORIGIN_X, GRID_ORIGIN_Y)
                )

        # -----------------------------------------------------------
        # LASER SHOOTING AND COLLISIONS
        # -----------------------------------------------------------


        # Update lasers
        for laser in lasers[:]:
            laser.update()
            if laser.is_off_screen():
                lasers.remove(laser)

        # Check laser-alien collisions
        for laser in lasers[:]:
            for alien in aliens_by_row[laser.row][:]:
                if laser.collides_with(alien):
                    lasers.remove(laser)
                    aliens_by_row[laser.row].remove(alien)
                    break

        # Shoot lasers from blue items
        if not game_over:
            item_blue.shoot_lasers_if_needed(dt, lasers, GRID_ORIGIN_Y, CELL_HEIGHT)

        # -----------------------------------------------------------


        # -----------------------------------------------------------
        # FLOATING BALL SPAWNING AND COLLECTION
        # -----------------------------------------------------------
        if not game_over and ball_spawn_timer >= ball_spawn_interval:     #######################
            ball_spawn_timer = 0
            balls.append(FloatingBall())

        if not game_over:
            item_black.spawn_ball_if_needed(dt, balls)

        for ball in balls[:]: #######################
            ball.update()
            if not game_over:
                ball.draw(screen)

            # Collect if close to mouse cursor
            if ball.is_near_mouse(mouse_pos):
                player_money += 5
                balls.remove(ball)

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

        pygame.display.update()
        if game_over and current_time - game_over_time > 3000:
            running = False


if __name__ == "__main__":
    main()