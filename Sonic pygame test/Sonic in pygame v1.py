import pygame
import sys
import math

# Init
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic Slope Physics")
clock = pygame.time.Clock()

# Colors
SKY = (135, 206, 235)
GREEN = (40, 200, 40)

# Load sprite sheet
sheet = pygame.image.load("sonic_mania_sprites_by_tazdrongo_dblf8qv.png").convert_alpha()

# Function to extract frames
def get_sprite(x, y, w, h):
    sprite = pygame.Surface((w, h), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, w, h))
    return sprite

def load_frames(start_x, start_y, count, w=48, h=48):
    return [get_sprite(start_x + i * w, start_y, w, h) for i in range(count)]

# Animation frame map
animations = {
    'idle': load_frames(0, 0, 3),
    'look_up': load_frames(144, 0, 2),
    'duck': load_frames(0, 48, 2),
    'run': load_frames(0, 144, 8),
    'skid': [get_sprite(384, 144, 48, 48)],
    'roll': load_frames(0, 192, 4),
    'jump': [get_sprite(0, 240, 48, 48)],
    'spin_dash': load_frames(48, 240, 5),
    'ball': load_frames(0, 96, 6),
    'super_idle': load_frames(624, 0, 4),
}

# Level with slope segments
level_slopes = [
    {'start': (0, 440), 'end': (100, 440)},
    {'start': (100, 440), 'end': (200, 420)},
    {'start': (200, 420), 'end': (300, 400)},
    {'start': (300, 400), 'end': (400, 400)},
    {'start': (400, 400), 'end': (600, 440)},
]

# Player class
class Player:
    def __init__(self):
        self.x = 50
        self.y = 100
        self.width = 48
        self.height = 48

        self.ground_speed = 0
        self.angle = 0
        self.on_ground = False
        self.gravity = 0.6
        self.y_velocity = 0

        self.anim_timer = 0
        self.anim_index = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.ground_speed -= 0.5
        if keys[pygame.K_RIGHT]:
            self.ground_speed += 0.5

        # Friction
        self.ground_speed *= 0.95

        # Position of foot for ground check
        foot_x = self.x + self.width // 2
        foot_y = self.y + self.height
        tile, slope_angle, corrected_y = self.get_current_slope(foot_x)

        if tile:
            angle_diff = (slope_angle - self.angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            self.angle += angle_diff * 0.2

            move_vec = pygame.Vector2(self.ground_speed, 0).rotate(-self.angle)
            self.x += move_vec.x
            self.y = corrected_y - self.height

            self.on_ground = True
            self.y_velocity = 0
        else:
            self.on_ground = False
            self.angle *= 0.9
            self.y_velocity += self.gravity
            self.y += self.y_velocity
            self.x += self.ground_speed

        # Animation timing
        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1)

    def get_current_slope(self, px):
        for slope in level_slopes:
            x1, y1 = slope['start']
            x2, y2 = slope['end']
            if x1 <= px <= x2:
                t = (px - x1) / (x2 - x1)
                py = y1 + t * (y2 - y1)
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                return slope, angle, py
        return None, 0, 0

    def get_current_animation(self):
        if not self.on_ground:
            return 'jump'
        elif abs(self.ground_speed) > 0.8:
            return 'run'
        else:
            return 'idle'

    def draw(self, surface):
        anim_name = self.get_current_animation()
        frames = animations[anim_name]
        frame = frames[self.anim_index % len(frames)]

        rotated = pygame.transform.rotate(frame, self.angle)
        rect = rotated.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(rotated, rect.topleft)

# Game setup
player = Player()

# Game loop
running = True
while running:
    screen.fill(SKY)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(keys)

    # Draw ground slopes
    for slope in level_slopes:
        pygame.draw.line(screen, GREEN, slope['start'], slope['end'], 6)

    # Draw player
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
