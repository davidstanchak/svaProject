import pygame
import random
import math

pygame.init()
pygame.display.set_caption("Scientists vs. Aliens")

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)

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

class FloatingBall:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(200, SCREEN_HEIGHT - 100)
        self.radius = 10
        self.dx = random.uniform(-0.5, 0.5)
        self.dy = random.uniform(-0.5, 0.5)

    def update(self):
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

class PlaceableItem:
    def __init__(self, x, y, width, height, item_type="blue"):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dragging = False
        self.placed_items = []
        self.type = item_type
        self.spawn_timers = []

    def start_drag(self):
        self.dragging = True

    def stop_drag(self, grid_left_x, grid_top_y, cell_width, cell_height, num_columns, num_rows, player_money):
        self.dragging = False
        col = (self.x - grid_left_x + self.width // 2) // cell_width
        row = (self.y - grid_top_y + self.height // 2) // cell_height
        col = max(0, min(num_columns - 1, col))
        row = max(0, min(num_rows - 1, row))
        snap_x = grid_left_x + col * cell_width + (cell_width - self.width) // 2
        snap_y = grid_top_y + row * cell_height + (cell_height - self.height) // 2

        if player_money >= 10:
            self.placed_items.append((snap_x, snap_y))
            self.spawn_timers.append(0)
            player_money -= 10

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

    def draw_preview(self, surface, grid_left_x, grid_top_y, cell_width, cell_height, num_columns, num_rows):
        if self.dragging:
            col = (self.x - grid_left_x + self.width // 2) // cell_width
            row = (self.y - grid_top_y + self.height // 2) // cell_height
            col = max(0, min(num_columns - 1, col))
            row = max(0, min(num_rows - 1, row))
            snap_x = grid_left_x + col * cell_width + (cell_width - self.width) // 2
            snap_y = grid_top_y + row * cell_height + (cell_height - self.height) // 2
            preview_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            preview_surface.fill((0, 0, 255, 100) if self.type == "blue" else (0, 0, 0, 100))
            surface.blit(preview_surface, (snap_x, snap_y))

    def spawn_ball_if_needed(self, dt, balls):
        if self.type != "black":
            return
        for i in range(len(self.spawn_timers)):
            self.spawn_timers[i] += dt
            if self.spawn_timers[i] >= 2000:
                self.spawn_timers[i] = 0
                px, py = self.placed_items[i]
                ball = FloatingBall()
                ball.x = px + self.width // 2
                ball.y = py + self.height // 2
                balls.append(ball)

def main():
    running = True
    NUM_COLUMNS, NUM_ROWS = 9, 5
    GRID_TOP_Y = 170
    GRID_HEIGHT = 530
    margin_bottom = SCREEN_HEIGHT - (GRID_TOP_Y + GRID_HEIGHT)
    margin_sides = margin_bottom
    GRID_LEFT_X = margin_sides
    GRID_WIDTH = SCREEN_WIDTH - 2 * margin_sides
    CELL_WIDTH = GRID_WIDTH // NUM_COLUMNS
    CELL_HEIGHT = GRID_HEIGHT // NUM_ROWS

    aliens_by_row = [[] for _ in range(NUM_ROWS)]
    spawn_timer = 0
    spawn_interval = 500
    spawn_cycle_timer = 0
    spawn_phase_duration = 2000
    break_phase_duration = 6000
    spawning_active = True

    item_blue = PlaceableItem(margin_sides + 20, 40, CELL_WIDTH // 2, CELL_HEIGHT // 2, "blue")
    item_black = PlaceableItem(margin_sides + 120, 40, CELL_WIDTH // 2, CELL_HEIGHT // 2, "black")

    player_money = 0
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 24)

    balls = []
    ball_spawn_timer = 0
    ball_spawn_interval = 2000

    countdown_start = pygame.time.get_ticks()
    countdown_duration = 3000
    game_started = False

    while running:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        if not game_started:
            elapsed = current_time - countdown_start
            screen.fill((0, 0, 0))
            if elapsed < countdown_duration:
                count = 3 - elapsed // 1000
                countdown_text = font.render(str(count), True, (255, 255, 255))
                countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(countdown_text, countdown_rect)
                pygame.display.update()
                continue
            else:
                game_started = True

        spawn_timer += dt
        spawn_cycle_timer += dt
        ball_spawn_timer += dt

        if spawning_active and spawn_cycle_timer >= spawn_phase_duration:
            spawn_cycle_timer = 0
            spawning_active = False
        elif not spawning_active and spawn_cycle_timer >= break_phase_duration:
            spawn_cycle_timer = 0
            spawning_active = True

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
                    player_money = item_blue.stop_drag(GRID_LEFT_X, GRID_TOP_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS, player_money)
                player_money = item_black.stop_drag(GRID_LEFT_X, GRID_TOP_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS, player_money)

        mouse_pos = pygame.mouse.get_pos()
        item_blue.update_position(mouse_pos)
        item_black.update_position(mouse_pos)

        screen.fill((0, 0, 0))
        draw_rounded_rect(screen, "#2C363F", (GRID_LEFT_X, GRID_TOP_Y, GRID_WIDTH, GRID_HEIGHT), radius=5)

        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                cell_color = "#333333" if (row + col) % 2 == 0 else "#535657"
                draw_rounded_rect(
                    screen,
                    cell_color,
                    (
                        GRID_LEFT_X + col * CELL_WIDTH,
                        GRID_TOP_Y + row * CELL_HEIGHT,
                        CELL_WIDTH + 7,
                        CELL_HEIGHT
                    ),
                    radius=5
                )

        draw_rounded_rect(screen, "#2F3061", (margin_sides, 12.5, 550, 145), radius=10)
        money_box_width = 120
        money_box_x = margin_sides + 550 + 20
        draw_rounded_rect(screen, "#2F3061", (money_box_x, 12.5, money_box_width, 145), radius=10)

        money_text = font.render(f"{player_money}", True, (255, 255, 255))
        text_rect = money_text.get_rect(center=(money_box_x + money_box_width // 2, 12.5 + 145 // 2))
        screen.blit(money_text, text_rect)

        item_blue.draw_preview(screen, GRID_LEFT_X, GRID_TOP_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS)
        item_black.draw_preview(screen, GRID_LEFT_X, GRID_TOP_Y, CELL_WIDTH, CELL_HEIGHT, NUM_COLUMNS, NUM_ROWS)
        item_blue.draw(screen)
        item_black.draw(screen)

        cost_text_blue = small_font.render("10", True, (255, 255, 255))
        cost_rect_blue = cost_text_blue.get_rect(center=(item_blue.x + item_blue.width // 2, item_blue.y + item_blue.height + 12))
        screen.blit(cost_text_blue, cost_rect_blue)

        cost_text_black = small_font.render("10", True, (255, 255, 255))
        cost_rect_black = cost_text_black.get_rect(center=(item_black.x + item_black.width // 2, item_black.y + item_black.height + 12))
        screen.blit(cost_text_black, cost_rect_black)

        for row in range(NUM_ROWS):
            row_aliens = aliens_by_row[row]
            for a in row_aliens:
                a.update()
                a.draw(screen)
            aliens_by_row[row] = [a for a in row_aliens if not a.is_off_screen()]

        if spawning_active and spawn_timer >= spawn_interval:
            spawn_timer = 0
            random_row = random.randint(0, NUM_ROWS - 1)
            row_aliens = aliens_by_row[random_row]
            if not row_aliens or row_aliens[-1].x < SCREEN_WIDTH - random.randint(CELL_WIDTH, CELL_WIDTH * 3):
                aliens_by_row[random_row].append(alien(random_row, CELL_WIDTH, CELL_HEIGHT, GRID_LEFT_X, GRID_TOP_Y))

        if ball_spawn_timer >= ball_spawn_interval:
            ball_spawn_timer = 0
            balls.append(FloatingBall())

        item_black.spawn_ball_if_needed(dt, balls)

        for ball in balls[:]:
            ball.update()
            ball.draw(screen)
            if ball.is_near_mouse(mouse_pos):
                player_money += 5
                balls.remove(ball)

        pygame.display.update()

    pygame.quit()

main()