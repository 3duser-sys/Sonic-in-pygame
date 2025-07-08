import pygame
import sys

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load background image
background_img = pygame.image.load("/mnt/data/1600px-ManiaGHZ1.png").convert()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, level_rects):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += 1  # Gravity
        if self.vel_y > 10:
            self.vel_y = 10

        # Apply vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        for rect in level_rects:
            if self.rect.colliderect(rect):
                if self.vel_y > 0:
                    self.rect.bottom = rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = rect.bottom
                    self.vel_y = 0

        # Apply horizontal movement
        self.rect.x += dx
        for rect in level_rects:
            if self.rect.colliderect(rect):
                if dx > 0:
                    self.rect.right = rect.left
                elif dx < 0:
                    self.rect.left = rect.right

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# Manual collision rectangles (you can fine-tune these)
level_rects = [
    pygame.Rect(0, 500, 800, 100),       # Ground section
    pygame.Rect(900, 450, 200, 50),      # Platform 1
    pygame.Rect(1200, 400, 150, 50),     # Platform 2
    pygame.Rect(1450, 350, 100, 50),     # Platform 3
    # Add more as needed
]

# Initialize player
player = Player(100, 300)
camera_x = 0

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(level_rects)

    # Camera follows player
    camera_x = player.rect.centerx - screen_width // 2
    camera_x = max(0, min(camera_x, background_img.get_width() - screen_width))

    # Draw background
    screen.blit(background_img, (-camera_x, 0))

    # Draw collision rects (visual debug)
    for rect in level_rects:
        draw_rect = rect.move(-camera_x, 0)
        pygame.draw.rect(screen, (255, 0, 0), draw_rect, 2)

    # Draw player
    player.draw(screen, camera_x)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
