import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50, 128)  # Semi-transparent gray
GREEN = (0, 200, 0)  # Green for the play button
RED = (255, 0, 0)  # Red for health bar

# Load assets
background_img = pygame.image.load("ktQBX2.png")
ship3_img = pygame.image.load("ship3.png")  # Starter spaceship
ship5_img = pygame.image.load("ship5.png")  # Enemy spaceship
ship1_img = pygame.image.load("ship1.png")  # Boss spaceship
ship2_img = pygame.image.load("ship2.png")  # Upgraded spaceship
powerup_img = pygame.image.load("L5dZ5k.png")  # Power-up sprite
crown_img = pygame.image.load("fame.png")  # Crown for victory
enemy_bullet_img = pygame.image.load("AxHgLJ.gif")  # Enemy bullet
player_bullet_img = pygame.image.load("kzZ5B_.gif")  # Player bullet
laser_beam_img = pygame.image.load("lucia-robbins-laser-beam-1.gif")  # Boss laser beam
victory_background_img = pygame.image.load("elena-kaeva-564656.jpg")
victory_background_img = pygame.transform.scale(victory_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
defeated_screen_img = pygame.image.load("thumb-1920-336290.png")
defeated_screen_img = pygame.transform.scale(defeated_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load new background images
main_background_img = pygame.image.load("360_F_823167120_rxDpbnQVCtLQLedOsBx69IWtskvKyX0V.jpg")
game_background_img = pygame.image.load("b1bdc1ae539dcbd1a7c33cef3e5f2d9a.jpg")

# Scale images
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
main_background_img = pygame.transform.scale(main_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_background_img = pygame.transform.scale(game_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
ship3_img = pygame.transform.scale(ship3_img, (150, 150))
ship5_img = pygame.transform.scale(ship5_img, (100, 100))
ship1_img = pygame.transform.scale(ship1_img, (200, 200))
ship2_img = pygame.transform.scale(ship2_img, (150, 150))
powerup_img = pygame.transform.scale(powerup_img, (50, 50))
crown_img = pygame.transform.scale(crown_img, (100, 100))
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (30, 30))
player_bullet_img = pygame.transform.scale(player_bullet_img, (30, 30))
laser_beam_img = pygame.transform.scale(laser_beam_img, (150, 150))

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Fonts
font_title = pygame.font.Font(pygame.font.get_default_font(), 54)
font_button = pygame.font.Font(pygame.font.get_default_font(), 36)
font_level = pygame.font.Font(pygame.font.get_default_font(), 24)
font_gameover = pygame.font.Font(pygame.font.get_default_font(), 48)

# Text rendering
def render_text(text, font, color):
    return font.render(text, True, color)

# Button setup
def draw_button(surface, rect, text, font, color, bg_color):
    pygame.draw.rect(surface, WHITE, rect, border_radius=10)  # White border
    inner_rect = rect.inflate(-6, -6)
    pygame.draw.rect(surface, bg_color, inner_rect, border_radius=10)  # Button background
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Overlay background with lower opacity
def draw_translucent_background(surface, color):
    translucent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    translucent_surface.fill(color)
    surface.blit(translucent_surface, (0, 0))

# Main loading screen loop
def loading_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    running = False

        # Draw the main menu background
        screen.blit(main_background_img, (0, 0))

        # Add translucent overlay
        draw_translucent_background(screen, (0, 0, 0, 128))  # Semi-transparent black

        # Draw title box with border
        title_surface = render_text("Space Shooter", font_title, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        title_box = title_rect.inflate(30, 30)
        pygame.draw.rect(screen, WHITE, title_box, border_radius=10)  # White border
        inner_title_box = title_box.inflate(-6, -6)
        pygame.draw.rect(screen, GRAY, inner_title_box, border_radius=10)  # Inner box
        screen.blit(title_surface, title_rect)

        # Draw spaceship with larger box
        spaceship_rect = ship3_img.get_rect(center=(SCREEN_WIDTH // 2, 300))
        spaceship_box = spaceship_rect.inflate(40, 40)  # Larger box
        pygame.draw.rect(screen, WHITE, spaceship_box, border_radius=10)  # White border
        inner_spaceship_box = spaceship_box.inflate(-6, -6)
        pygame.draw.rect(screen, GRAY, inner_spaceship_box, border_radius=10)  # Inner box
        screen.blit(ship3_img, spaceship_rect)

        # Draw button
        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 60)
        draw_button(screen, play_button, "PLAY", font_button, WHITE, GREEN)

        pygame.display.flip()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = ship5_img
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.speed = 0  # Stationary

    def update(self):
        # Enemies shoot less frequently
        if random.random() < 0.01:  # 2% chance to shoot per frame
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.add(enemy_bullet)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# Player spaceship class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship3_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.health = 100
        self.speed = 10  # Faster movement
        self.upgraded = False
#KEYS
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def upgrade(self):
        self.image = ship2_img
        self.speed = 12
        self.upgraded = True

    def shoot(self):
        bullet = PlayerBullet(self.rect.centerx, self.rect.top)
        player_bullets.add(bullet)

# Player bullet class
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 5
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship1_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 200))  # Set boss at the top of the screen
        self.health = 250  # Increased health
        self.speed = 1  # Set speed to 0 to prevent moving
        self.laser_beam = None

    def update(self):
        if not self.laser_beam:
            self.laser_beam = LaserBeam(self.rect.centerx, self.rect.centery)
            lasers.add(self.laser_beam)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_beam_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Victory screen function
def victory_screen():
    screen.blit(victory_background_img, (0, 0))  # Set the background
    pygame.display.flip()
    pygame.time.wait(500000000000000) 

# Create sprite groups
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()

# Draw health bar
def draw_health_bar(surface, health):
    bar_width = 150
    bar_height = 20
    pygame.draw.rect(surface, RED, (SCREEN_WIDTH // 2 - bar_width // 2, 20, bar_width, bar_height))
    pygame.draw.rect(surface, GREEN, (SCREEN_WIDTH // 2 - bar_width // 2, 20, int(bar_width * (health / 100)), bar_height))

# Draw round indicator
def draw_round_indicator(surface, round_number):
    round_text = render_text(f"Round {round_number}/3", font_level, WHITE)
    surface.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 50))

# Defeat screen function
def defeat_screen():
    # Display defeat background image
    defeat_image = pygame.image.load("thumb-1920-336290.png")
    defeat_image = pygame.transform.scale(defeat_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(defeat_image, (0, 0))  # Set the background
    pygame.display.flip()
    pygame.time.wait(500000)  # Wait for 3 seconds before quitting or restarting
    pygame.quit()
    sys.exit()  # Quit the game after waiting

# Main game loop
def main_game():
    player = Player()
    round_number = 0
    clock = pygame.time.Clock()
    running = True
    boss = None  # Initialize boss as None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()

        # Player shooting
        if pygame.mouse.get_pressed()[0]:
            player.shoot()

        # Update all sprite groups
        player_bullets.update()
        enemy_bullets.update()
        powerups.update()
        enemies.update()
        lasers.update()

        # Check for collisions between bullets and enemies
        for bullet in player_bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                enemy.take_damage(2)  # Increased damage to enemies
                bullet.kill()

        # Check if the player has collided with any enemy bullets
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, player):
                player.take_damage(2)  # Increased damage from enemy bullets
                bullet.kill()

        # Rarely drop power-ups after defeating enemies
        if random.random() < 0.001 and len(enemies) == 0:
            powerup = PowerUp(random.randint(0, SCREEN_WIDTH), 0)
            powerups.add(powerup)

        # Spawn boss or enemies based on the round
        if not enemies:
            if round_number == 3 and not boss:  # Final boss round
                boss = Boss()
                enemies.add(boss)
            elif round_number < 3:
                round_number += 1
                for x in range(round_number * 5):
                    enemy = Enemy(random.randint(100, SCREEN_WIDTH - 100), 50, 5)  # Increased health for enemies
                    enemies.add(enemy)

        # Update power-ups
        for powerup in powerups:
            if pygame.sprite.collide_rect(powerup, player):
                player.upgrade()
                powerup.kill()

        # Draw everything
        screen.blit(game_background_img, (0, 0))
        player_bullets.draw(screen)
        enemy_bullets.draw(screen)
        powerups.draw(screen)
        enemies.draw(screen)
        lasers.draw(screen)
        screen.blit(player.image, player.rect)

        # Draw health bars and round indicator
        draw_health_bar(screen, player.health)
        draw_round_indicator(screen, round_number)

        # Boss health bar (if the boss exists)
        if boss:
            bar_width = 200  # Width of the health bar
            bar_height = 10  # Height of the health bar
            bar_x = SCREEN_WIDTH // 2 - bar_width // 2  # Centered horizontally
            bar_y = 350  # Position at the top of the screen
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))  # Background (red)
            current_health_width = int(bar_width * (boss.health / 250))  # Boss health is out of 250
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_health_width, bar_height))  # Foreground (green)

        pygame.display.flip()
        clock.tick(60)

        # Check if the boss is defeated
        if boss and boss.health <= 0:
            victory_screen()
            running = False

        # Check if the player is defeated
        if player.health <= 0:
            defeat_screen()  # Show the defeat screen and then quit or restart
            running = False  # Exit the game loop if the player is defeated

# Run the game
loading_screen()
main_game()
pygame.quit()
sys.exit()
