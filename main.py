import asyncio
import random
import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Define vectors for position, velocity, acceleration
vec = pygame.math.Vector2

# Constants
HEIGHT = 450
WIDTH = 400
GRAVITY = 0.5
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

# Set up the display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror Wars")

# Define game states
PLAYING = 1
GAME_OVER = 0

# Initialize game state
game_state = PLAYING

# Load images (ensure these files exist in your project directory)
spritePic = pygame.transform.scale(pygame.image.load("spritepicFINAL.png").convert_alpha(), (40, 70))
shadowPic = pygame.transform.scale(pygame.image.load("shadowspriteFINAL.png").convert_alpha(), (40, 70))
spriteRunning = pygame.transform.scale(pygame.image.load("spriterunning.png").convert_alpha(), (40, 70))
shadowRunning = pygame.transform.scale(pygame.image.load("shadowrunning.png").convert_alpha(), (40, 70))

# Define sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()

# Add jump count variables
jump_count = 0
MAX_JUMPS = 1

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = spritePic
        except pygame.error as e:
            print(f"Unable to load player image: {e}")
            
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, GRAVITY)
        self.jump_count = 0
        self.MAX_JUMPS = 1
        self.spike_not_placed = True

    def move(self):
        self.acc = vec(0, GRAVITY)  # Apply gravity

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d]:
            self.acc.x = 0
            self.image = spritePic
        elif pressed_keys[pygame.K_a]:
            self.acc.x = -ACC
            self.image = pygame.transform.flip(spriteRunning, True, False)
        elif pressed_keys[pygame.K_d]:
            self.acc.x = ACC
            self.image = spriteRunning
        else:
            self.image = spritePic

        if pressed_keys[pygame.K_w]:
            self.jump()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Prevent moving beyond the left and right edges
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
            self.vel.x = 0
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
            self.vel.x = 0

        self.rect.midbottom = self.pos
        #print(self.rect.midbottom)

    def jump(self):
        if self.jump_count < self.MAX_JUMPS:
            self.jump_count += 1
            self.vel.y = -10

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Line thickness 2

    def update(self):
        self.move()
        collide = rect_collide(self.rect)
        if collide != False:
            if self.rect.centery < collide.rect.bottom:
                self.pos.y = collide.rect.top + 1
                self.vel.y = 0
                self.rect.midbottom = self.pos
                self.jump_count = 0
            else:
                self.vel.y = 0.1

def rect_collide(rect1):
    for platform in platforms:
        if rect1.colliderect(platform.rect):
            return platform
    return False

class Shadow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = shadowPic
        except pygame.error as e:
            print(f"Unable to load player image: {e}")
            
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, GRAVITY)
        self.jump_count = 0
        self.MAX_JUMPS = 1  # Allow double jumps
        self.mirrored_move = False
        self.isDead = False
        self.finished_current_level = False


    def move(self):
        self.acc = vec(0, GRAVITY)  # Apply gravity

        pressed_keys = pygame.key.get_pressed()
        if self.mirrored_move:
            if pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d]:
                self.acc.x = 0
                self.image = shadowPic
            elif pressed_keys[pygame.K_d]:
                self.acc.x = -ACC
                self.image = pygame.transform.flip(shadowRunning, True, False)
            elif pressed_keys[pygame.K_a]:
                self.acc.x = ACC
                self.image = shadowRunning
            else:
                self.image = shadowPic
        else:
            if pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d]:
                self.acc.x = 0
                self.image = shadowPic
            elif pressed_keys[pygame.K_a]:
                self.acc.x = -ACC
                self.image = pygame.transform.flip(shadowRunning, True, False)
            elif pressed_keys[pygame.K_d]:
                self.acc.x = ACC
                self.image = shadowRunning
            else:
                self.image = shadowPic

        if pressed_keys[pygame.K_w]:
            self.jump()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Prevent moving beyond the left and right edges
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0

        self.rect.midbottom = self.pos
        #print(self.rect.midbottom)

    def jump(self):
        if self.jump_count < self.MAX_JUMPS:
            self.jump_count += 1
            self.vel.y = -10

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Line thickness 2

    def update(self):
        self.move()
        collide = rect_collide(self.rect)
        if collide != False:
            if self.rect.centery < collide.rect.bottom:
                self.pos.y = collide.rect.top + 1
                self.vel.y = 0
                self.rect.midbottom = self.pos
                self.jump_count = 0
            else:
                self.vel.y = 0.1

# Define the Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((234, 208, 168))  # Platform color (Beige)
        self.rect = pygame.Rect(x, y, width, height)


    def draw(self, surface):
        pygame.draw.rect(surface, (234, 208, 168), self.rect)
    def move(self):
        pass  # Platforms are static in this example

# Define the Spike class
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("spike.png").convert_alpha(), (20, 20))  # Adjust size as needed
        except pygame.error as e:
            print(f"Unable to load spike image: {e}")
            
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x-40, y)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def update(self):
        # If spikes are stationary, no need to update position
        pass

class Mirror(pygame.sprite.Sprite):
    finished_current_level = False
    def __init__(self, x, y, M1, P1):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("mirror.png").convert_alpha(), (40, 40))  # Adjust size as needed
        except pygame.error as e:
            print(f"Unable to load mirror image: {e}")
            
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x-40, y)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.M1 = M1
        self.P1 = P1

    def update(self):
        if pygame.sprite.collide_rect(self, self.P1):
            #print("Collided with mirror")
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_f]:
                self.M1.mirrored_move = True
            elif pressed_keys[pygame.K_g]:
                self.M1.mirrored_move = False
            if self.M1.isDead:
                # Handle the case when M1 is dead, e.g., restart the level or end the game
                self.M1.finished_current_level = True
                #print("M1 is dead")
    def draw(self, surface):
        pass


# Define the kill_screen function with Restart button
def kill_screen():
    global game_state, level  # To modify the global game state variable

    # Define fonts
    game_over_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)

    # Render "Game Over" text
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))

    # Define "Restart" button
    restart_text = button_font.render('Restart', True, (255, 255, 255))
    restart_button = pygame.Rect(0, 0, 200, 50)
    restart_button.center = (WIDTH / 2, HEIGHT / 2 + 50)
    
    # Button colors
    button_color = (0, 255, 0)
    button_hover_color = (0, 200, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    level = 2            # Set level to 2
                    game_loop()    # Reset game objects
                    pygame.quit()
                    
                    game_state = PLAYING
                    return

        # Fill the screen with black
        displaysurface.fill((0, 0, 0))

        # Draw "Game Over" text
        displaysurface.blit(game_over_text, game_over_rect)

        # Check if mouse is over the restart button
        mouse_pos = pygame.mouse.get_pos()
        if restart_button.collidepoint(mouse_pos):
            current_button_color = button_hover_color
        else:
            current_button_color = button_color

        # Draw "Restart" button
        pygame.draw.rect(displaysurface, current_button_color, restart_button)
        displaysurface.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        # Update the display
        pygame.display.flip()
        FramePerSec.tick(FPS)

# Initialize or reset the game
def initialize_game():
    global all_sprites, platforms, spikes, P1, M1, mirror, top, floor
    global level
    level = 1
    # Create sprite instances
    P1 = Player(10, 410)
    M1 = Shadow(10, 200)
    mirror = Mirror(200, 430, M1, P1)
    floor = Platform(0, HEIGHT - 20, WIDTH, 20)
    platform = Platform(0, 320, 50, 20)

    top = Platform(0, -20, WIDTH, 20)
    # Clear existing sprite groups
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    
    # Add sprites to groups
    all_sprites.add(floor)
    all_sprites.add(P1)
    all_sprites.add(M1)
    all_sprites.add(platform)
    all_sprites.add(mirror)
    
    platforms.add(floor)
    platforms.add(platform)
    #platforms.add(top)

# Initialize the game for the first time

# Define the main game loop
def level_2():
    global all_sprites, platforms, spikes, P1, M1, mirror, floor, top
    global level
    mirror.finished_current_level = False
    level = 2
    
    # Clear existing platforms and spikes
    platforms.empty()
    spikes.empty()
    all_sprites.empty()
    
    # Reset player and shadow positions
    x = random.randint(10, WIDTH-10)
    P1 = Player(104, 410)
    #P1.pos = vec(50, HEIGHT - 70)
    P1.vel = vec(0, 0)
    P1.acc = vec(0, GRAVITY)
    P1.jump_count = 0
    P1.spike_not_placed = True
    i = random.randint(10, WIDTH-10)
    while abs(i-x) < 50:
        i = random.randint(10, WIDTH-10)
    M1 = Shadow(104, 0)
    #M1.pos = vec(100, HEIGHT - 70)
    M1.vel = vec(0, 0)
    M1.acc = vec(0, GRAVITY)
    M1.jump_count = 0
    M1.mirrored_move = False
    M1.isDead = False

    mirror = Mirror(317, 39, M1, P1)
    
    # Define new platforms for level 2
    floor = Platform(0, HEIGHT - 20, WIDTH, 20)
    platform1 = Platform(203, 236, 80, 20)
    platform2 = Platform(29, 327, 80, 20)
    platform3 = Platform(48, 103, 80, 20)
    platform4 = Platform(292, 100, 80, 20)
    platform5 = Platform(39, 220, 80, 20)
    platform6 = Platform(254, 359, 80, 20)
    # Add platforms to groups
    platforms.add(floor, platform1, platform2, platform3, platform4, platform5, platform6)
    all_sprites.add(floor, platform1, platform2, platform3, platform4, platform5, platform6)
    
    # Add player and shadow back to all_sprites
    all_sprites.add(P1, M1)
    
    # Add mirror or other sprites if needed
    #mirror = Mirror(300, 400, M1, P1)
    all_sprites.add(mirror)
    platforms.add(mirror)

def level3():
    global all_sprites, platforms, spikes, P1, M1, mirror, floor, top
    global level
    mirror.finished_current_level = False
    level = 2
    
    # Clear existing platforms and spikes
    platforms.empty()
    spikes.empty()
    all_sprites.empty()
    
    # Reset player and shadow positions
    x = random.randint(10, WIDTH-10)
    P1 = Player(104, 410)
    #P1.pos = vec(50, HEIGHT - 70)
    P1.vel = vec(0, 0)
    P1.acc = vec(0, GRAVITY)
    P1.jump_count = 0
    P1.spike_not_placed = True
    i = random.randint(10, WIDTH-10)
    while abs(i-x) < 50:
        i = random.randint(10, WIDTH-10)
    M1 = Shadow(104, 0)
    #M1.pos = vec(100, HEIGHT - 70)
    M1.vel = vec(0, 0)
    M1.acc = vec(0, GRAVITY)
    M1.jump_count = 0
    M1.mirrored_move = False
    M1.isDead = False

    mirror = Mirror(317, 39, M1, P1)
    
    # Define new platforms for level 2
    floor = Platform(0, HEIGHT - 20, WIDTH, 20)
    platform1 = Platform(80, 320, 80, 10)
    platform2 = Platform(160, 240, 80, 10)
    platform3 = Platform(240, 160, 80, 10)
    platform4 = Platform(320, 80, 80, 10)

    platforms.add(floor, platform1, platform2, platform3, platform4)
    all_sprites.add(floor, platform1, platform2, platform3, platform4)
    
    # Add player and shadow back to all_sprites
    all_sprites.add(P1, M1)
    
    # Add mirror or other sprites if needed
    #mirror = Mirror(300, 400, M1, P1)
    all_sprites.add(mirror)
    platforms.add(mirror)

'''def level4():
    global all_sprites, platforms, spikes, P1, M1, mirror, floor, top
    global level
    mirror.finished_current_level = False
    level = 2
    
    # Clear existing platforms and spikes
    platforms.empty()
    spikes.empty()
    all_sprites.empty()
    
    # Reset player and shadow positions
    x = random.randint(10, WIDTH-10)
    P1 = Player(104, 410)
    #P1.pos = vec(50, HEIGHT - 70)
    P1.vel = vec(0, 0)
    P1.acc = vec(0, GRAVITY)
    P1.jump_count = 0
    P1.spike_not_placed = True
    i = random.randint(10, WIDTH-10)
    while abs(i-x) < 50:
        i = random.randint(10, WIDTH-10)
    M1 = Shadow(104, 0)
    #M1.pos = vec(100, HEIGHT - 70)
    M1.vel = vec(0, 0)
    M1.acc = vec(0, GRAVITY)
    M1.jump_count = 0
    M1.mirrored_move = False
    M1.isDead = False

    mirror = Mirror(317, 39, M1, P1)
    
    # Define new platforms for level 2
    floor = Platform(0, HEIGHT - 20, WIDTH, 20)
    # Level 2 platforms
    platforms2 = [
        Platform(50, 450, 150, 20),
        Platform(250, 400, 120, 20),
        Platform(400, 350, 180, 20),
        Platform(600, 300, 100, 20),
        Platform(750, 250, 150, 20),
        Platform(900, 200, 120, 20),
        Platform(1050, 150, 180, 20),
        Platform(1200, 100, 100, 20)
    ]

    # Add platforms to sprite groups if necessary
    for platform in platforms2:
        all_sprites.add(platform)
        platforms.add(platform)

    #platforms.add(floor, platform1, platform2, platform3, top)
    #all_sprites.add(floor, platform1, platform2, platform3, top)
    
    # Add player and shadow back to all_sprites
    all_sprites.add(P1, M1)
    
    # Add mirror or other sprites if needed
    #mirror = Mirror(300, 400, M1, P1)
    all_sprites.add(mirror)
    platforms.add(mirror)'''

def run_level():
    global game_state
    PLAYING = 1
    GAME_OVER = 0
    game_state = PLAYING
    print("Running level")
    while M1.finished_current_level == False:
        if game_state == PLAYING:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    ()
                elif event.type == pygame.KEYDOWN:
                    #if event.key == pygame.K_w and jump_count < MAX_JUMPS:
                    #    P1.jump()
                    #    M1.jump()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        ()
                    elif event.key == pygame.K_s and P1.spike_not_placed:
                        # Place a spike at the player's current position
                        spike = Spike(P1.rect.centerx, P1.rect.bottom)
                        all_sprites.add(spike)
                        spikes.add(spike)
                        P1.spike_not_placed = False

            # Update and move sprites
            P1.move()
            M1.move()
            all_sprites.update()
            all_sprites.draw(displaysurface)
            pygame.display.flip()

            # Check for collisions between spikes and other sprites (e.g., Shadow)
            collisions = pygame.sprite.groupcollide(spikes, all_sprites, False, False)
            for spike, hit_sprites in collisions.items():
                for sprite in hit_sprites:
                    if sprite != P1 and isinstance(sprite, Shadow):
                        M1.isDead = True
                        sprite.kill()   # Remove the Shadow
                        spike.kill()    # Optionally remove the spike after collision
                    elif sprite == P1:
                        game_state = GAME_OVER
                        kill_screen()

            # Check for collision between Player and Shadow (or other game over conditions)
            if pygame.sprite.collide_rect(P1, M1):
                game_state = GAME_OVER
                kill_screen()

            # Render everything
            displaysurface.fill((0, 0, 0))  # Clear screen with black
            all_sprites.draw(displaysurface)
            for sprite in platforms:
                sprite.draw(displaysurface)
            #P1.draw(displaysurface)
            #M1.draw(displaysurface)
            pygame.display.flip()
            FramePerSec.tick(FPS)

        elif game_state == GAME_OVER:
            kill_screen()

def win_screen():
    font = pygame.font.Font(None, 74)
    text = font.render('You Win!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                game_loop()
                return

        displaysurface.fill((0, 0, 0))
        displaysurface.blit(text, text_rect)
        pygame.display.flip()
        FramePerSec.tick(FPS)

def intro_page():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                intro = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('Mirror Wars', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        instructions = font_small.render('Press space to start', True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        displaysurface.blit(instructions, instructions_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def about_page():
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                about = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('About', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 150))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        about_lines = [
    'You feel a split within your',
    'soul. An evil shadow', 
    'materializes before you.',  'Rid the world of',  'this corruption.',
    'Cleanse your soul.'
]

        y_offset = 100  # Updated starting y position
        for line in about_lines:
            line_surface = font_small.render(line, True, (255, 255, 255))
            displaysurface.blit(line_surface, (50, y_offset))
            y_offset += 30  # Adjust line height as needed

        continue_text = font_small.render('Press space to continue', True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))  # Move it near the bottom
        displaysurface.blit(continue_text, continue_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def controls_page():
    controls = True
    while controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                controls = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('Controls', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        # Render control instructions separately
        controls_text1 = font_small.render('Use A/D to move, W to jump.', True, (255, 255, 255))
        controls_text2 = font_small.render('F reverses your shadow when', True, (255, 255, 255))
        controls_text3 = font_small.render('you are in contact with a mirror,', True, (255, 255, 255))
        controls_text4 = font_small.render('and G sets it back to normal.', True, (255, 255, 255))

        # Set starting positions
        x_position = 25  # Adjust as needed
        y_position = 200  # Starting y position for controls

        # Blit the control texts to the display surface
        displaysurface.blit(controls_text1, (x_position, y_position))
        displaysurface.blit(controls_text2, (x_position, y_position + 30))
        displaysurface.blit(controls_text3, (x_position, y_position + 60))
        displaysurface.blit(controls_text4, (x_position, y_position + 90))

        # Render "Press space to continue" lower on the screen
        continue_text = font_small.render('Press space to continue', True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        displaysurface.blit(continue_text, continue_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def game_loop():
    initialize_game()
    run_level()
    level3()
    run_level()
    level_2()
    run_level()
    win_screen()

async def main():
    intro_page()
    about_page()
    controls_page()
    game_loop()
    await asyncio.sleep(0)

asyncio.run(main())