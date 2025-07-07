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

def load_frames(folder, prefix, count):
    return [pygame.image.load(f"{folder}/{prefix}_{i+1}.png").convert_alpha() for i in range(count)]

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

        self.idle_time = 0
        self.idle_special = False
        self.idle_special_timer = 0

        self.was_crouching = False
        self.crouch_hold = False  # For crouch: True = hold last frame, False = animate

        self.was_lookup = False
        self.lookup_hold = False  # For look_up: True = hold last frame, False = animate

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        moved = False
        if keys[pygame.K_LEFT]:
            self.ground_speed -= 0.5
            self.facing_left = True
            moved = True
        if keys[pygame.K_RIGHT]:
            self.ground_speed += 0.5
            self.facing_left = False
            moved = True

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

        speed = abs(self.ground_speed)
        prev_state = self.state

        # --- Idle Animation Smart Logic and Hold Logic ---
        if not self.on_ground:
            self.state = 'jump'
            self._reset_idle()
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False
        elif crouching and 'crouch' in animations:
            self.state = 'crouch'
            # Start crouch animation if just pressed down
            if not self.was_crouching:
                self.anim_index = 0
                self.anim_timer = 0
                self.crouch_hold = False
            self.was_crouching = True
            # If animation finished, hold last frame until released
            if self.anim_index == len(animations['crouch']) - 1:
                self.crouch_hold = True
            self.lookup_hold = False
            self.was_lookup = False
        elif looking_up and 'look_up' in animations:
            self.state = 'look_up'
            # Start look up animation if just pressed up
            if not self.was_lookup:
                self.anim_index = 0
                self.anim_timer = 0
                self.lookup_hold = False
            self.was_lookup = True
            # If animation finished, hold last frame until released
            if self.anim_index == len(animations['look_up']) - 1:
                self.lookup_hold = True
            self.crouch_hold = False
            self.was_crouching = False
        elif speed > 8 and 'topspeed_run' in animations:
            self.state = 'topspeed_run'
            self._reset_idle()
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False
        elif speed > 4:
            self.state = 'run'
            self._reset_idle()
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False
        elif speed > 0.8:
            self.state = 'walk'
            self._reset_idle()
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False
        else:
            # IDLE LOGIC
            if moved or not self.on_ground:
                self._reset_idle()
                self.crouch_hold = False
                self.was_crouching = False
                self.lookup_hold = False
                self.was_lookup = False
            else:
                self.idle_time += clock.get_time() / 1000.0  # seconds

            # After 5 seconds, play idle_2 and idle_3 repeatedly for 3 seconds, then return to idle_1
            if self.idle_time >= 5:
                self.idle_special = True
                self.idle_special_timer += clock.get_time() / 1000.0

                # Play idle_2 and idle_3 repeatedly for 3 seconds
                if self.idle_special_timer <= 3:
                    self.state = 'idle_special'
                else:
                    self._reset_idle()
            else:
                self.state = 'idle'
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False

        # Reset animation index if state changed
        if self.state != prev_state:
            # Only reset anim_index/timer if NOT holding crouch/lookup last frame
            if not ((prev_state == 'crouch' and self.crouch_hold) or (prev_state == 'look_up' and self.lookup_hold)):
                self.anim_index = 0
                self.anim_timer = 0

        # Frame timing
        self.anim_timer += 1
        if self.state == 'idle_special':
            frame_speed = 10  # slower loop for idle_2/3
        else:
            frame_speed = max(1, int(12 - min(speed, 10)))
        if self.anim_timer >= frame_speed:
            self.anim_timer = 0
            if self.state == 'idle_special':
                self.anim_index = (self.anim_index + 1) % 2
            elif self.state == 'crouch':
                if not self.crouch_hold:
                    self.anim_index += 1
                    if self.anim_index >= len(animations['crouch']):
                        self.anim_index = len(animations['crouch']) - 1
                        self.crouch_hold = True
            elif self.state == 'look_up':
                if not self.lookup_hold:
                    self.anim_index += 1
                    if self.anim_index >= len(animations['look_up']):
                        self.anim_index = len(animations['look_up']) - 1
                        self.lookup_hold = True
            else:
                self.anim_index = (self.anim_index + 1) % len(animations.get(self.state, [animations['idle'][0]]))

        # If released crouch, reset crouch state
        if self.was_crouching and not crouching:
            self.crouch_hold = False
            self.was_crouching = False
            self.anim_index = 0
            self.anim_timer = 0

        # If released lookup, reset lookup state
        if self.was_lookup and not looking_up:
            self.lookup_hold = False
            self.was_lookup = False
            self.anim_index = 0
            self.anim_timer = 0

    def _reset_idle(self):
        self.idle_time = 0
        self.idle_special = False
        self.idle_special_timer = 0

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
        if self.state == 'idle_special':
            frames = [animations['idle'][1], animations['idle'][2]]
        else:
            frames = animations[self.state]
        # For crouch or look_up, if holding last frame, always show last
        if self.state == 'crouch' and self.crouch_hold:
            frame = frames[-1]
        elif self.state == 'look_up' and self.lookup_hold:
            frame = frames[-1]
        else:
            frame = frames[self.anim_index % len(frames)]
        angle = -self.angle if self.facing_left else self.angle
        frame = pygame.transform.flip(frame, self.facing_left, False)
        rotated = pygame.transform.rotate(frame, angle)
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