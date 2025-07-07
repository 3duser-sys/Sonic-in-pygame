import pygame
import sys
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic Slope Physics")
clock = pygame.time.Clock()

# Colors
SKY = (135, 206, 235)
GREEN = (40, 200, 40)

# Helper to load sprite frames (make sure the files exist!)
def load_frames(folder, prefix, count):
    return [pygame.image.load(f"{folder}/{prefix}_{i+1}.png").convert_alpha() for i in range(count)]

# Animation frame map -- uses only files you actually have!
ANIM_FOLDER = "Sonic pygame test - Copy"

animations = {
    'idle': load_frames(ANIM_FOLDER, 'idle', 3),
    'look_up': load_frames(ANIM_FOLDER, 'look_up', 6),
    'crouch': load_frames(ANIM_FOLDER, 'crouch', 4),
    'walk': load_frames(ANIM_FOLDER, 'walk', 12),
    'run': load_frames(ANIM_FOLDER, 'run', 8),
    'topspeed_run': load_frames(ANIM_FOLDER, 'topspeed_run', 3),
    'skid': load_frames(ANIM_FOLDER, 'skid', 2),
    'jump': load_frames(ANIM_FOLDER, 'jump', 8),
    'spindash': load_frames(ANIM_FOLDER, 'spindash', 4),
    'victory': load_frames(ANIM_FOLDER, 'victory', 3),
    'wall_cling': load_frames(ANIM_FOLDER, 'wall_cling', 3),
    'die': [pygame.image.load(f"{ANIM_FOLDER}/die.png").convert_alpha()],
    'hurt': [pygame.image.load(f"{ANIM_FOLDER}/hurt.png").convert_alpha()],
}

level_slopes = [
    {'start': (0, 440), 'end': (100, 440)},
    {'start': (100, 440), 'end': (200, 420)},
    {'start': (200, 420), 'end': (300, 400)},
    {'start': (300, 400), 'end': (400, 400)},
    {'start': (400, 400), 'end': (600, 440)},
]

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
        self.state = "idle"
        self.facing_left = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        # Movement
        if keys[pygame.K_LEFT]:
            self.ground_speed -= 0.5
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.ground_speed += 0.5
            self.facing_left = False

        # Friction
        self.ground_speed *= 0.95

        # Crouch/look up
        crouching = keys[pygame.K_DOWN] and self.on_ground
        looking_up = keys[pygame.K_UP] and self.on_ground

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

        # Animation update
        self.anim_timer += 1
        speed = abs(self.ground_speed)
        prev_state = self.state
        if not self.on_ground:
            self.state = 'jump'
        elif crouching and 'crouch' in animations:
            self.state = 'crouch'
        elif looking_up and 'look_up' in animations:
            self.state = 'look_up'
        elif speed > 8 and 'topspeed_run' in animations:
            self.state = 'topspeed_run'
        elif speed > 4:
            self.state = 'run'
        elif speed > 0.8:
            self.state = 'walk'
        else:
            self.state = 'idle'

        # Reset animation index if state changed
        if self.state != prev_state:
            self.anim_index = 0
            self.anim_timer = 0

        # Frame timing
        frame_speed = max(1, int(12 - min(speed, 10)))
        if self.anim_timer >= frame_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(animations[self.state])

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

    def draw(self, surface):
        frames = animations[self.state]
        frame = frames[self.anim_index % len(frames)]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        rotated = pygame.transform.rotate(frame, self.angle)
        rect = rotated.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(rotated, rect.topleft)

player = Player()

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