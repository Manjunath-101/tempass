import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
LANE_COUNT = 3
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Shooter")
clock = pygame.time.Clock()

# Game objects

class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 60
        self.color = WHITE
        self.lane = LANE_COUNT // 2
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.update_position()

    def update_position(self):
        center_x = LANE_WIDTH // 2 + self.lane * LANE_WIDTH
        self.rect.centerx = center_x
        self.rect.bottom = SCREEN_HEIGHT - 10

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.update_position()

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
            self.update_position()

class Alien(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.width = 40
        self.height = 40
        self.color = RED
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        center_x = LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.centerx = center_x
        self.rect.top = -self.height
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.radius = 15
        self.color = YELLOW
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        center_x = LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.centerx = center_x
        self.rect.top = -self.radius * 2
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 5
        self.height = 15
        self.color = GREEN
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Sprite groups
rocket = Rocket()
rockets = pygame.sprite.GroupSingle(rocket)
aliens = pygame.sprite.Group()
coins = pygame.sprite.Group()
lasers = pygame.sprite.Group()

# Score
score = 0

# Timers
ADD_ALIEN = pygame.USEREVENT + 1
ADD_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_ALIEN, 800)  # every 0.8 seconds
pygame.time.set_timer(ADD_COIN, 1000)  # every 1 second

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rocket.move_left()
            elif event.key == pygame.K_RIGHT:
                rocket.move_right()
            elif event.key == pygame.K_SPACE:
                laser = Laser(rocket.rect.centerx, rocket.rect.top)
                lasers.add(laser)

        if event.type == ADD_ALIEN:
            lane = random.randrange(LANE_COUNT)
            aliens.add(Alien(lane))

        if event.type == ADD_COIN:
            lane = random.randrange(LANE_COUNT)
            coins.add(Coin(lane))

    # Update sprites
    aliens.update()
    coins.update()
    lasers.update()

    # Collisions
    # Rocket collects coins
    collected = pygame.sprite.spritecollide(rocket, coins, dokill=True)
    score += len(collected)

    # Lasers hit aliens
    for laser in lasers:
        hit_aliens = pygame.sprite.spritecollide(laser, aliens, dokill=True)
        if hit_aliens:
            score += len(hit_aliens) * 5
            laser.kill()

    # Alien hits rocket -> end game
    if pygame.sprite.spritecollideany(rocket, aliens):
        running = False

    # Drawing
    screen.fill(BLACK)
    aliens.draw(screen)
    coins.draw(screen)
    lasers.draw(screen)
    rockets.draw(screen)

    # display score
    font = pygame.font.Font(None, 36)
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()

# game over message
screen.fill(BLACK)
font = pygame.font.Font(None, 72)
text = font.render("Game Over", True, RED)
text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
screen.blit(text, text_rect)
pygame.display.flip()
pygame.time.wait(2000)

pygame.quit()
sys.exit()
