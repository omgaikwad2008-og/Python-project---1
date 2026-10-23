#alien_invasion.py
import sys
import pygame


# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
BG_COLOR = (15, 20, 40)

# Colors
WHITE = (255, 255, 255)
GREEN = (80, 220, 120)
RED = (240, 80, 80)
YELLOW = (255, 220, 70)


class Ship:
    def __init__(self):
        self.width = 60
        self.height = 35
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        # Draw a simple spaceship.
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
        ]
        pygame.draw.polygon(screen, GREEN, points)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y, 6, 15)
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)


class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 45, 35)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 12, self.rect.y + 12), 4)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 33, self.rect.y + 12), 4)


def create_aliens():
    aliens = []
    for row in range(3):
        for column in range(12):
            x = 60 + column * 75
            y = 60 + row * 60
            aliens.append(Alien(x, y))
    return aliens


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ship = Ship()
    bullets = []
    aliens = create_aliens()
    score = 0
    alien_direction = 1
    alien_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(ship.x + ship.width // 2, ship.y))

        keys = pygame.key.get_pressed()
        ship.move(keys)

        # Move bullets upward.
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # Move aliens sideways.
        change_direction = False
        for alien in aliens:
            alien.rect.x += alien_speed * alien_direction
            if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
                change_direction = True

        if change_direction:
            alien_direction *= -1
            for alien in aliens:
                alien.rect.y += 20

        # Detect bullet hits.
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 10
                    break

        # Create a new wave after all aliens are defeated.
        if not aliens:
            aliens = create_aliens()
            alien_speed += 1

        # Draw everything.
        screen.fill(BG_COLOR)

        ship.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for alien in aliens:
            alien.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        controls_text = font.render("Move: Left/Right   Fire: Space", True, WHITE)
        screen.blit(score_text, (15, 15))
        screen.blit(controls_text, (15, SCREEN_HEIGHT - 35))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()