import pygame
import sys
import math

pygame.init()

# Fullscreen setup
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Sonic outdust")
pygame.display.set_icon(pygame.image.load("Sonic pygame test/amy.ico"))
clock = pygame.time.Clock()

SKY = (135, 206, 235)
GREEN = (40, 200, 40)

def load_frames(folder, prefix, count):
    return [pygame.image.load(f"{folder}/{prefix}_{i+1}.png").convert_alpha() for i in range(count)]

ANIM_FOLDER = "Sonic pygame test"

animations = {
    'idle': load_frames(ANIM_FOLDER, 'idle', 3),
    'look_up': load_frames(ANIM_FOLDER, 'look_up', 6),
    'crouch': load_frames(ANIM_FOLDER, 'crouch', 4),
    'walk': load_frames(ANIM_FOLDER, 'walk', 12),
    'run': load_frames(ANIM_FOLDER, 'run', 8),
    'topspeed_run': load_frames(ANIM_FOLDER, 'topspeed_run', 3),
    'skid': load_frames(ANIM_FOLDER, 'skid', 2),
    'jump': load_frames(ANIM_FOLDER, 'jump', 8),
    'dropdash_charge': [
        pygame.image.load(f"{ANIM_FOLDER}/jump_9.png").convert_alpha(),
        pygame.image.load(f"{ANIM_FOLDER}/jump_10.png").convert_alpha()
    ],
    'spindash': load_frames(ANIM_FOLDER, 'spindash', 4),
    'victory': load_frames(ANIM_FOLDER, 'victory', 3),
    'wall_cling': load_frames(ANIM_FOLDER, 'wall_cling', 3),
    'die': [pygame.image.load(f"{ANIM_FOLDER}/die.png").convert_alpha()],
    'hurt': [pygame.image.load(f"{ANIM_FOLDER}/hurt.png").convert_alpha()],
    'roll': load_frames(ANIM_FOLDER, 'jump', 8),
    'ground_enemy': load_frames(ANIM_FOLDER, 'ground_enemy', 7),
    'sky_enemy': load_frames(ANIM_FOLDER, 'sky_enemy', 4),
}

signpost_frames = [
    pygame.image.load(f"{ANIM_FOLDER}/signpost_1.png").convert_alpha(),
    pygame.image.load(f"{ANIM_FOLDER}/signpost_2.png").convert_alpha(),
    pygame.image.load(f"{ANIM_FOLDER}/signpost_3.png").convert_alpha(),
    pygame.image.load(f"{ANIM_FOLDER}/signpost_4.png").convert_alpha(),
    pygame.image.load(f"{ANIM_FOLDER}/signpost_5.png").convert_alpha(),
]

GROUND_Y = HEIGHT - 80
level_slopes = [
    {'start': (0, GROUND_Y), 'end': (WIDTH//2, GROUND_Y)},
    {'start': (WIDTH//2, GROUND_Y), 'end': (WIDTH*3//4, GROUND_Y-20)},
    {'start': (WIDTH*3//4, GROUND_Y-20), 'end': (WIDTH, GROUND_Y-40)},
    {'start': (WIDTH, GROUND_Y-40), 'end': (WIDTH+400, GROUND_Y-30)},
    {'start': (WIDTH+400, GROUND_Y-30), 'end': (WIDTH+800, GROUND_Y-60)},
    {'start': (WIDTH+800, GROUND_Y-60), 'end': (WIDTH+1200, GROUND_Y-20)},
    {'start': (WIDTH+1200, GROUND_Y-20), 'end': (WIDTH+1600, GROUND_Y-40)},
    {'start': (WIDTH+1600, GROUND_Y-40), 'end': (WIDTH+2000, GROUND_Y)},
]

pygame.mixer.init()

def play_music(path, loops=0):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

def show_menu_screen(screen):
    title_img = pygame.image.load(f"{ANIM_FOLDER}/title_screen.png").convert()
    title_img = pygame.transform.scale(title_img, (WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 48, bold=True)
    option_font = pygame.font.SysFont("arial", 32, bold=True)
    
    options = ["PLAY", "OPTIONS", "QUIT"]
    selected = 0
    play_music(f"{ANIM_FOLDER}/title_theme.mp3", loops=-1)
    blink = True
    blink_timer = 0
    BLINK_INTERVAL = 30

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % len(options)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    stop_music()
                    if options[selected] == "PLAY":
                        return "play"
                    elif options[selected] == "QUIT":
                        pygame.quit()
                        sys.exit()
                    elif options[selected] == "OPTIONS":
                        show_options_screen(screen)

        screen.blit(title_img, (0, 0))
        title_text = font.render("SONIC OUTDUST", True, (255, 255, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 70))

        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected and blink else (255, 255, 255)
            opt_txt = option_font.render(opt, True, color)
            screen.blit(opt_txt, (WIDTH // 2 - opt_txt.get_width() // 2, 200 + i * 60))
        
        blink_timer += 1
        if blink_timer >= BLINK_INTERVAL:
            blink = not blink
            blink_timer = 0

        pygame.display.flip()
        clock.tick(60)

def show_options_screen(screen):
    title_img = pygame.image.load(f"{ANIM_FOLDER}/title_screen.png").convert()
    title_img = pygame.transform.scale(title_img, (WIDTH, HEIGHT))
    option_font = pygame.font.SysFont("arial", 32, bold=True)
    back_font = pygame.font.SysFont("arial", 24, bold=True)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False

        screen.blit(title_img, (0, 0))
        opt_txt = option_font.render("OPTIONS (Not Implemented)", True, (255, 255, 255))
        screen.blit(opt_txt, (WIDTH // 2 - opt_txt.get_width() // 2, HEIGHT // 2 - 40))
        back_txt = back_font.render("Press ESC/ENTER to go back", True, (200, 200, 200))
        screen.blit(back_txt, (WIDTH // 2 - back_txt.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()
        clock.tick(60)

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 48
        self.height = 48

        self.ground_speed = 0
        self.angle = 0
        self.on_ground = False
        self.gravity = 0.21875
        self.jump_hold_gravity = 0.115
        self.jump_hold_frames_max = 15
        self.jump_hold_frames = 0
        self.y_velocity = 0
        self.air_x_speed = 0

        self.anim_timer = 0
        self.anim_index = 0
        self.state = "idle"
        self.facing_left = False

        self.idle_time = 0
        self.idle_special = False
        self.idle_special_timer = 0

        self.was_crouching = False
        self.crouch_hold = False
        self.was_lookup = False
        self.lookup_hold = False
        self.idle_stage = 0

        self.jump_pressed = False
        self.jump_anim_timer = 0
        self.jump_anim_speed = 4
        self.has_landed = False

        self.spindash_charging = False
        self.spindash_power = 0
        self.max_spindash = 16
        self.roll_threshold = 3.0
        self.rolling = False
        self.prev_crouching = False
        self.prev_z_pressed = False

        self.peelout_charging = False
        self.peelout_power = 0
        self.max_peelout = 16
        self.prev_lookup = False

        self.dropdash_charging = False
        self.dropdash_ready = False
        self.dropdash_charge_time = 0
        self.dropdash_charge_needed = 8
        self.dropdash_speed = 18
        self.jump_was_released = False

        self.jump_grace = 0
        self.JUMP_GRACE_TIME = 8

        self.respawn_x = 100
        self.respawn_y = 100

        # HURT STATE
        self.hurt_timer = 0
        self.HURT_TIME = 32
        self.hurt_dx = 0
        self.hurt_dy = 0
        self.invincible_timer = 0
        self.INVINCIBLE_TIME = 90

        self.dying = False
        self.die_timer = 0
        self.die_anim_length = 60

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def respawn(self):
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.ground_speed = 0
        self.air_x_speed = 0
        self.y_velocity = 0
        self.angle = 0
        self.state = "idle"
        self.rolling = False
        self.spindash_charging = False
        self.peelout_charging = False
        self.has_landed = False
        self.on_ground = False
        self.anim_index = 0
        self.anim_timer = 0
        self.dying = False
        self.die_timer = 0
        self.dropdash_charging = False
        self.dropdash_ready = False
        self.dropdash_charge_time = 0
        self.jump_grace = 0
        self.jump_was_released = False
        self.jump_hold_frames = 0
        self.hurt_timer = 0
        self.hurt_dx = 0
        self.hurt_dy = 0
        self.invincible_timer = 0

    def is_really_rolling(self):
        return (
            self.rolling
            and not self.spindash_charging
            and not self.peelout_charging
            and abs(self.ground_speed) >= self.roll_threshold
            and (not self.on_ground or (self.on_ground and (self.crouch_hold or abs(self.ground_speed) > self.roll_threshold)))
        )

    def hurt(self, enemy_x=None):
        if self.hurt_timer > 0 or self.invincible_timer > 0:
            return
        self.state = 'hurt'
        self.hurt_timer = self.HURT_TIME
        self.invincible_timer = self.INVINCIBLE_TIME
        if enemy_x is not None:
            direction = -1 if self.x + self.width // 2 < enemy_x else 1
        else:
            direction = -1 if self.facing_left else 1
        self.hurt_dx = direction * 5
        self.hurt_dy = -6
        self.ground_speed = 0
        self.air_x_speed = 0
        self.y_velocity = 0
        self.rolling = False
        self.spindash_charging = False
        self.peelout_charging = False
        self.anim_index = 0
        self.anim_timer = 0

    def update(self, keys):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            self.x += self.hurt_dx
            self.y += self.hurt_dy
            self.hurt_dy += self.gravity
            if self.hurt_timer <= 0:
                self.state = "idle"
                self.anim_index = 0
                self.anim_timer = 0
            return

        GROUND_ACCEL = 0.16
        GROUND_DECEL = 0.08
        FRICTION = 0.0625
        MAX_WALK_SPEED = 3.5
        MAX_RUN_SPEED = 7.0
        MAX_TOP_SPEED = 10.0
        MAX_ROLL_SPEED = 17.0

        if self.dying:
            self.die_timer += 1
            if self.die_timer >= self.die_anim_length:
                self.respawn()
            return

        if self.jump_grace > 0:
            self.jump_grace -= 1

        moved = False
        crouching = keys[pygame.K_DOWN] and self.on_ground
        looking_up = keys[pygame.K_UP] and self.on_ground
        z_pressed = keys[pygame.K_z]

        if looking_up and self.on_ground and abs(self.ground_speed) < 0.5 and not self.rolling and not self.spindash_charging:
            if not self.peelout_charging:
                if z_pressed and not self.prev_z_pressed:
                    self.peelout_charging = True
                    self.peelout_power = 8
                    self.state = 'topspeed_run'
                    self.anim_index = 0
            elif self.peelout_charging:
                if z_pressed and not self.prev_z_pressed:
                    if self.peelout_power < self.max_peelout:
                        self.peelout_power += 1.7
                self.state = 'topspeed_run'
        if self.peelout_charging and not looking_up and self.prev_lookup:
            self.ground_speed = (self.peelout_power * (-1 if self.facing_left else 1))
            self.rolling = False
            self.peelout_charging = False
            self.peelout_power = 0
            self.anim_index = 0
            self.anim_timer = 0

        self.prev_lookup = looking_up

        if crouching and self.on_ground and abs(self.ground_speed) < 0.5 and not self.rolling and not self.peelout_charging:
            if not self.spindash_charging:
                if z_pressed and not self.prev_z_pressed:
                    self.spindash_charging = True
                    self.spindash_power = 8
                    self.state = 'spindash'
                    self.anim_index = 0
            elif self.spindash_charging:
                if z_pressed and not self.prev_z_pressed:
                    if self.spindash_power < self.max_spindash:
                        self.spindash_power += 1.7
                self.state = 'spindash'
        if self.spindash_charging and not crouching and self.prev_crouching:
            self.ground_speed = (self.spindash_power * (-1 if self.facing_left else 1))
            self.air_x_speed = self.ground_speed
            self.rolling = True
            self.spindash_charging = False
            self.spindash_power = 0
            self.state = 'roll'
            self.anim_index = 0
            self.anim_timer = 0

        self.prev_crouching = crouching
        self.prev_z_pressed = z_pressed

        if (not self.rolling and not self.spindash_charging and not self.peelout_charging
            and self.on_ground and abs(self.ground_speed) > self.roll_threshold and crouching):
            self.rolling = True
            self.state = 'roll'
            self.anim_index = 0
            self.anim_timer = 0

        if self.rolling:
            if not self.on_ground or abs(self.ground_speed) < self.roll_threshold:
                self.rolling = False
                if not moved:
                    self.state = 'idle'
                elif abs(self.ground_speed) > 0.8:
                    self.state = 'walk'
                else:
                    self.state = 'idle'
                self.anim_index = 0

        can_move = not (self.rolling or self.spindash_charging or self.peelout_charging)

        if self.rolling:
            speed_cap = MAX_ROLL_SPEED
        else:
            speed_cap = MAX_TOP_SPEED

        if not crouching and not looking_up and can_move and self.on_ground:
            if keys[pygame.K_LEFT]:
                if self.ground_speed > 0:
                    self.ground_speed -= GROUND_DECEL
                else:
                    self.ground_speed -= GROUND_ACCEL
                self.facing_left = True
                moved = True
            elif keys[pygame.K_RIGHT]:
                if self.ground_speed < 0:
                    self.ground_speed += GROUND_DECEL
                else:
                    self.ground_speed += GROUND_ACCEL
                self.facing_left = False
                moved = True
            else:
                if abs(self.ground_speed) > FRICTION:
                    self.ground_speed -= FRICTION * (1 if self.ground_speed > 0 else -1)
                else:
                    self.ground_speed = 0

        if self.ground_speed > speed_cap:
            self.ground_speed = speed_cap
        elif self.ground_speed < -speed_cap:
            self.ground_speed = -speed_cap

        if (
            z_pressed and not self.jump_pressed and self.on_ground
            and not crouching
            and not looking_up
            and not self.spindash_charging
            and not self.peelout_charging
        ):
            jump_power = 6.5
            self.y_velocity = -jump_power
            self.air_x_speed = self.ground_speed
            self.on_ground = False
            self.state = 'jump'
            self.anim_index = 0
            self.jump_anim_timer = 0
            self.has_landed = False
            self.jump_grace = self.JUMP_GRACE_TIME
            self.jump_hold_frames = self.jump_hold_frames_max

        self.jump_pressed = z_pressed

        if not z_pressed and not self.on_ground:
            self.jump_was_released = True
        if self.on_ground:
            self.jump_was_released = False

        if not self.on_ground:
            if self.jump_was_released and z_pressed and not self.dropdash_charging and not self.spindash_charging and not self.peelout_charging:
                self.dropdash_charging = True
                self.dropdash_charge_time = 0
                self.dropdash_ready = False
            elif self.dropdash_charging and z_pressed:
                self.dropdash_charge_time += 1
                if self.dropdash_charge_time >= self.dropdash_charge_needed:
                    self.dropdash_ready = True
            elif not z_pressed:
                self.dropdash_charging = False
                self.dropdash_charge_time = 0
                self.dropdash_ready = False
        else:
            if self.dropdash_ready:
                self.ground_speed = self.dropdash_speed * (1 if not self.facing_left else -1)
                self.air_x_speed = self.ground_speed
                if self.on_ground and abs(self.ground_speed) > self.roll_threshold:
                    self.rolling = True
                    self.state = 'roll'
                    self.anim_index = 0
                    self.anim_timer = 0
            self.dropdash_charging = False
            self.dropdash_charge_time = 0
            self.dropdash_ready = False

        if not self.on_ground:
            if z_pressed and self.jump_hold_frames > 0 and self.y_velocity < 0:
                self.y_velocity += self.jump_hold_gravity
                self.jump_hold_frames -= 1
            else:
                self.y_velocity += self.gravity
                self.jump_hold_frames = 0

        if self.on_ground:
            tile, slope_angle, corrected_y = self.get_current_slope(self.x + self.width // 2)
            if self.rolling:
                self.ground_speed *= 0.985
                if tile and self.ground_speed != 0:
                    slope_rad = math.radians(slope_angle)
                    self.ground_speed += math.sin(slope_rad) * 0.36
            else:
                self.ground_speed *= 0.93 if abs(self.ground_speed) < 1 else 0.97
                if tile and self.ground_speed != 0:
                    slope_rad = math.radians(slope_angle)
                    self.ground_speed += math.sin(slope_rad) * 0.12
        else:
            self.air_x_speed *= 0.995
            self.ground_speed = self.air_x_speed

        if self.on_ground:
            self.x += self.ground_speed
        else:
            self.x += self.air_x_speed

        self.y += self.y_velocity

        foot_x = self.x + self.width // 2
        tile, slope_angle, corrected_y = self.get_current_slope(foot_x)
        landed_on_slope = False
        if tile and self.y + self.height >= corrected_y - 2 and self.y_velocity >= 0:
            self.y = corrected_y - self.height
            self.y_velocity = 0
            self.on_ground = True
            self.air_x_speed = self.ground_speed
            landed_on_slope = True
        elif self.y + self.height > HEIGHT - 10:
            self.y = HEIGHT - 10 - self.height
            self.y_velocity = 0
            self.on_ground = True
            self.air_x_speed = self.ground_speed
        else:
            self.on_ground = False

        speed = abs(self.ground_speed)
        prev_state = self.state

        if not self.on_ground:
            if self.state != 'jump' and not self.dying and abs(self.y_velocity) > 0.5:
                self.state = 'jump'
                self.anim_index = 0
                self.jump_anim_timer = 0

            self.jump_anim_timer += 1
            if self.jump_anim_timer >= self.jump_anim_speed:
                self.jump_anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(animations['jump'])

            self._reset_idle()
            self.crouch_hold = False
            self.was_crouching = False
            self.lookup_hold = False
            self.was_lookup = False
            self.idle_stage = 0

        elif self.state == 'jump':
            if self.on_ground and self.y_velocity >= 0 and not self.has_landed:
                self.has_landed = True
                if speed > 8:
                    self.state = 'topspeed_run'
                elif speed > 4:
                    self.state = 'run'
                elif speed > 0.8:
                    self.state = 'walk'
                else:
                    self.state = 'idle'
                self.anim_index = 0
                self.anim_timer = 0
        else:
            self.has_landed = False

        if self.on_ground and self.state not in ["jump", "spindash", "roll", "die"]:
            if crouching and 'crouch' in animations:
                self.state = 'crouch'
                if not self.was_crouching:
                    self.anim_index = 0
                    self.anim_timer = 0
                    self.crouch_hold = False
                self.was_crouching = True
                if self.anim_index == len(animations['crouch']) - 1:
                    self.crouch_hold = True
                self.lookup_hold = False
                self.was_lookup = False
                self.idle_stage = 0

            elif looking_up and 'look_up' in animations:
                self.state = 'look_up'
                if not self.was_lookup:
                    self.anim_index = 0
                    self.anim_timer = 0
                    self.lookup_hold = False
                self.was_lookup = True
                if self.anim_index == len(animations['look_up']) - 1:
                    self.lookup_hold = True
                self.crouch_hold = False
                self.was_crouching = False
                self.idle_stage = 0

            elif speed > 8:
                self.state = 'topspeed_run'
                self._reset_idle()
            elif speed > 4:
                self.state = 'run'
                self._reset_idle()
            elif speed > 0.8:
                self.state = 'walk'
                self._reset_idle()
            else:
                if moved:
                    self._reset_idle()
                else:
                    self.idle_time += clock.get_time() / 1000.0
                if self.idle_time < 5:
                    self.state = 'idle'
                    self.idle_stage = 0
                else:
                    self.idle_stage = 1
                    self.idle_special = True
                    self.idle_special_timer += clock.get_time() / 1000.0
                    if self.idle_special_timer <= 3:
                        self.state = 'idle_special'
                    else:
                        self._reset_idle()
                        self.state = 'idle'
                        self.idle_stage = 0

        if self.state != prev_state:
            if self.state == "jump":
                self.anim_index = 0
                self.jump_anim_timer = 0
            elif not ((prev_state == 'crouch' and self.crouch_hold) or (prev_state == 'look_up' and self.lookup_hold)):
                self.anim_timer = 0

        self.anim_timer += 1
        if self.state == 'idle_special':
            frame_speed = 10
        elif self.state == 'idle':
            frame_speed = 9999
        elif self.state in ['spindash', 'roll', 'topspeed_run']:
            frame_speed = 4
        else:
            frame_speed = max(1, int(12 - min(speed, 10)))

        if self.state != "jump":
            if self.anim_timer >= frame_speed:
                self.anim_timer = 0
                if self.state == 'idle_special':
                    self.anim_index = (self.anim_index + 1) % 2
                elif self.state == 'crouch' and not self.crouch_hold:
                    self.anim_index += 1
                    if self.anim_index >= len(animations['crouch']):
                        self.anim_index = len(animations['crouch']) - 1
                        self.crouch_hold = True
                elif self.state == 'look_up' and not self.lookup_hold:
                    self.anim_index += 1
                    if self.anim_index >= len(animations['look_up']):
                        self.anim_index = len(animations['look_up']) - 1
                        self.lookup_hold = True
                elif self.state == 'spindash':
                    self.anim_index = (self.anim_index + 1) % len(animations['spindash'])
                elif self.state == 'roll':
                    self.anim_index = (self.anim_index + 1) % len(animations['roll'])
                elif self.state == 'topspeed_run':
                    self.anim_index = (self.anim_index + 1) % len(animations['topspeed_run'])
                elif self.state in ('walk', 'run'):
                    self.anim_index = (self.anim_index + 1) % len(animations.get(self.state, [animations['idle'][0]]))
                elif self.state == 'idle':
                    self.anim_index = 0

        if self.was_crouching and not crouching:
            self.crouch_hold = False
            self.was_crouching = False
            self.anim_index = 0
            self.anim_timer = 0

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

    def draw(self, surface, camera_x):
        if self.hurt_timer > 0:
            frame = animations['hurt'][0]
        elif getattr(self, 'dropdash_charging', False) and not getattr(self, 'on_ground', True):
            frames = animations['dropdash_charge']
            frame = frames[(pygame.time.get_ticks() // 120) % len(frames)]
        else:
            anim_state = 'roll' if self.is_really_rolling() else self.state
            if anim_state == 'idle_special':
                frames = [animations['idle'][1], animations['idle'][2]]
            elif anim_state == 'spindash':
                frames = animations['spindash']
            elif anim_state == 'roll':
                frames = animations['roll']
            elif anim_state == 'topspeed_run':
                frames = animations['topspeed_run']
            elif anim_state == 'hurt':
                frames = animations['hurt']
            else:
                frames = animations.get(anim_state, animations['idle'])

            if anim_state == 'crouch' and self.crouch_hold:
                frame = frames[-1]
            elif anim_state == 'look_up' and self.lookup_hold:
                frame = frames[-1]
            elif anim_state == 'idle':
                frame = frames[0]
            else:
                frame = frames[self.anim_index % len(frames)]

        display_angle = -self.angle if self.facing_left else self.angle if self.state != 'jump' else 0
        frame = pygame.transform.flip(frame, self.facing_left, False)
        rotated = pygame.transform.rotate(frame, display_angle)
        rect = rotated.get_rect(midbottom=(self.x - camera_x + self.width // 2, self.y + self.height))
        surface.blit(rotated, rect.topleft)

class Enemy:
    def __init__(self, x, y, sky=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.alive = True
        self.sky = sky
        self.anim_timer = 0
        self.anim_index = 0
        self.direction = 1
        self.speed = 1.1 if not sky else 2
        self.patrol_left = x - 80
        self.patrol_right = x + 80
        self.facing_left = False
        self.vertical_offset = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, sonic_x, sonic_y):
        if not self.alive:
            return
        if self.sky:
            dx = (sonic_x - self.x)
            dy = (sonic_y - self.y)
            dist = math.hypot(dx, dy)
            if dist > 2:
                self.x += self.speed * dx / (dist + 1e-8)
                self.y += self.speed * dy / (dist + 1e-8)
            self.facing_left = dx > 0
        else:
            move_dir = 1 if sonic_x > self.x else -1
            self.facing_left = move_dir > 0
            self.x += move_dir * self.speed
            foot_x = self.x + self.width // 2
            slope, angle, corrected_y = self.get_current_slope(foot_x)
            if slope:
                self.y = corrected_y - self.height
            else:
                self.y += 2
        self.anim_timer += 1
        if self.sky:
            if self.anim_timer >= 6:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 4
        else:
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 7

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

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        if self.sky:
            frames = animations['sky_enemy']
        else:
            frames = animations['ground_enemy']
        frame = frames[self.anim_index % len(frames)]
        frame = pygame.transform.flip(frame, self.facing_left, False)
        rect = frame.get_rect(midbottom=(self.x - camera_x + self.width // 2, self.y + self.height))
        surface.blit(frame, rect.topleft)

    def handle_collision_with_sonic(self, player):
        if not self.alive or player.invincible_timer > 0:
            return
        prect = player.get_rect()
        erect = self.get_rect()
        if not prect.colliderect(erect):
            return

        is_rolling = player.is_really_rolling()
        is_spindash = player.spindash_charging
        is_dropdash = player.dropdash_charging or player.dropdash_ready
        is_jumping = player.state == "jump"
        jump_down = player.y_velocity > 0
        jump_up = player.y_velocity < 0
        jumping_on = (
            is_jumping and (player.y + player.height - 8 < self.y) and jump_down
        )
        jumping_any = is_jumping and (jump_up or jump_down)
        attacking = is_rolling or is_spindash or is_dropdash or jumping_any

        if attacking:
            self.alive = False
            # Bounce if hitting from above (jump or dropdash downwards)
            if jumping_on or (is_jumping and jump_down):
                player.y_velocity = -8
                player.on_ground = False
                player.state = "jump"
                player.jump_anim_timer = 0
        else:
            player.hurt(self.x)

player = Player()

def get_camera_x(player):
    min_x = 0
    if not level_slopes:
        return 0
    max_x = level_slopes[-1]['end'][0] - WIDTH
    target = player.x + player.width // 2 - WIDTH // 2
    return max(min_x, min(max_x, target))

enemies = [
    Enemy(WIDTH//2+200, GROUND_Y-45, sky=True),
    Enemy(WIDTH//2+600, GROUND_Y-10, sky=False),
    Enemy(WIDTH+800, GROUND_Y-60, sky=True),
    Enemy(WIDTH+1600, GROUND_Y-40, sky=False)
]

while True:
    menu_result = show_menu_screen(screen)
    if menu_result == "play":
        player.respawn()
        for e in enemies:
            e.alive = True
        running = True
        level_complete = False
        goal_x = level_slopes[-1]['end'][0] - 10 if level_slopes else WIDTH-10

        signpost_anim_timer = 0
        signpost_anim_index = 0
        signpost_anim_speed = 8

        while running:
            screen.fill(SKY)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not player.dying and (player.y > HEIGHT + 100):
                player.dying = True
                player.state = "die"
                player.die_timer = 0
            if keys[pygame.K_r]:
                player.respawn()

            player.update(keys)
            camera_x = get_camera_x(player)

            for slope in level_slopes:
                start = (slope['start'][0] - camera_x, slope['start'][1])
                end = (slope['end'][0] - camera_x, slope['end'][1])
                pygame.draw.line(screen, GREEN, start, end, 6)

            for e in enemies:
                e.update(player.x, player.y)
                e.handle_collision_with_sonic(player)
                e.draw(screen, camera_x)

            signpost_anim_timer += 1
            if signpost_anim_timer >= signpost_anim_speed:
                signpost_anim_timer = 0
                signpost_anim_index = (signpost_anim_index + 1) % len(signpost_frames)

            signpost_img = signpost_frames[signpost_anim_index]
            goal_rect = signpost_img.get_rect(midbottom=(goal_x - camera_x + 8, GROUND_Y+10))
            screen.blit(signpost_img, goal_rect.topleft)

            player.draw(screen, camera_x)

            if not level_complete and player.x + player.width // 2 >= goal_x:
                level_complete = True
                font = pygame.font.SysFont("arial", 64, bold=True)
                text = font.render("LEVEL COMPLETE!", True, (255, 255, 255))
                screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(3500)
                break

            pygame.display.flip()
            clock.tick(60)