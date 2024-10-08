### 1. **Imports and Initial Setup**

```python
import pygame 
from os.path import join
from random import randint, uniform
```

- **`pygame`**: A library used for creating games. It provides functionality for graphics, sound, and game logic.
- **`join`**: A method from `os.path` used to construct file paths in a way that is compatible with different operating systems.
- **`randint` and `uniform`**: Functions from the `random` module. `randint` generates an integer between two specified values, and `uniform` generates a floating-point number between two values. These are used to randomize meteor positions and movements.

### 2. **Player Class**

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('assets', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        # mask 
        self.mask = pygame.mask.from_surface(self.image)
```

- **`Player`**: Represents the player's spaceship.
  - **`__init__`**: Initializes the player sprite.
    - **`self.image`**: Loads the player's image and applies alpha transparency.
    - **`self.rect`**: Defines the player's rectangular area for positioning and collision detection, centered in the window.
    - **`self.direction`**: A `Vector2` object to store the direction of movement.
    - **`self.speed`**: Movement speed of the player.
    - **`self.can_shoot`**: Boolean to control if the player can shoot.
    - **`self.laser_shoot_time`**: Records the last time the player shot a laser.
    - **`self.cooldown_duration`**: Time required between shots.
    - **`self.mask`**: Creates a collision mask from the player's image to detect precise collisions.

```python
def laser_timer(self):
    if not self.can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - self.laser_shoot_time >= self.cooldown_duration:
            self.can_shoot = True
```

- **`laser_timer`**: Manages the cooldown period for shooting.
  - Checks if enough time has passed since the last shot to enable shooting again.

```python
def update(self, dt):
    keys = pygame.key.get_pressed()
    self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    self.direction = self.direction.normalize() if self.direction else self.direction
    self.rect.center += self.direction * self.speed * dt

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE] and self.can_shoot:
        Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
        self.can_shoot = False
        self.laser_shoot_time = pygame.time.get_ticks()
        laser_sound.play()
    
    self.laser_timer()
```

- **`update`**: Updates the player’s position and handles shooting.
  - **`keys`**: Checks which keys are currently pressed.
  - **`self.direction.x` and `self.direction.y`**: Sets movement direction based on arrow keys.
  - **`self.rect.center`**: Updates the player's position based on the direction and speed.
  - **`recent_keys`**: Checks for newly pressed keys.
  - **`Laser(...)`**: Creates a laser if the space key is pressed and the player can shoot.
  - **`self.laser_timer()`**: Updates the shooting cooldown status.

### 3. **Star Class**

```python
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
```

- **`Star`**: Represents stars in the background.
  - **`__init__`**: Initializes the star sprite.
    - **`self.image`**: Sets the star’s image.
    - **`self.rect`**: Randomly positions the star within the window.

### 4. **Laser Class**

```python
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
```

- **`Laser`**: Represents the lasers fired by the player.
  - **`__init__`**: Initializes the laser sprite.
    - **`self.image`**: Sets the laser’s image.
    - **`self.rect`**: Positions the laser at the specified location.
  - **`update`**: Moves the laser upwards and removes it if it goes off-screen.

### 5. **Meteor Class**

```python
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(300, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
```

- **`Meteor`**: Represents falling meteors.
  - **`__init__`**: Initializes the meteor sprite.
    - **`self.original_surf`**: Stores the original image to preserve it for rotation.
    - **`self.image`**: Sets the meteor’s image.
    - **`self.rect`**: Positions the meteor at the specified location.
    - **`self.start_time`**: Records the time when the meteor was created.
    - **`self.lifetime`**: Duration for which the meteor is active.
    - **`self.direction`**: Movement direction with some randomness.
    - **`self.speed`**: Random speed for the meteor.
    - **`self.rotation_speed`**: Random rotation speed for the meteor.
    - **`self.rotation`**: Current rotation angle.
  - **`update`**: Moves the meteor, applies rotation, and removes it after its lifetime.

### 6. **AnimatedExplosion Class**

```python
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        explosion_sound.play()
    
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
```

- **`AnimatedExplosion`**: Represents an explosion animation.
  - **`__init__`**: Initializes the explosion sprite.
    - **`self.frames`**: List of images for the explosion animation.
    - **`self.frame_index`**: Index to track the current frame.
    - **`self.image`**: Sets the initial image for the explosion.
    - **`self.rect`**: Positions the explosion.
    - **`explosion_sound.play()`**: Plays the explosion sound effect.
  - **`update`**: Advances the animation by updating the frame index and changing the image. Removes the explosion sprite when the animation is complete.

### 7. **Collision Detection and Scoring**

```python
def collisions():
    global running 

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
```

- **`collisions`**: Handles collisions between sprites.
  - **`pygame.sprite.spritecollide`**: Checks for collisions between the player and meteors. If a collision is detected, the game ends.
  - **`laser_sprites`**: Checks if lasers collide with meteors

. If a collision is detected, the laser is removed and an explosion animation is created.

```python
def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20,10).move(0,-8), 5, 10)
```

- **`display_score`**: Displays the score (time survived) on the screen.
  - **`current_time`**: Calculates the score based on elapsed time.
  - **`text_surf`**: Renders the score as text.
  - **`text_rect`**: Defines the position of the score on the screen.
  - **`display_surface.blit`**: Draws the score on the screen.
  - **`pygame.draw.rect`**: Draws a border around the score text.

### 8. **Game Initialization and Main Loop**

```python
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
running = True
clock = pygame.time.Clock()
```

- **`pygame.init()`**: Initializes all imported pygame modules.
- **`WINDOW_WIDTH` and `WINDOW_HEIGHT`**: Define the dimensions of the game window.
- **`display_surface`**: Creates the game window.
- **`pygame.display.set_caption`**: Sets the window title.
- **`running`**: Boolean flag to control the game loop.
- **`clock`**: Controls the frame rate.

```python
# import
star_surf = pygame.image.load(join('assets', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('assets', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('assets', 'images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('assets', 'images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('assets', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('assets', 'audio', 'laser.wav'))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join('assets', 'audio', 'explosion.wav'))
game_music = pygame.mixer.Sound(join('assets', 'audio', 'game_music.wav'))
game_music.set_volume(0.4)
```

- **`star_surf`, `meteor_surf`, `laser_surf`**: Load images for stars, meteors, and lasers.
- **`font`**: Loads a font for rendering text.
- **`explosion_frames`**: Loads images for the explosion animation.
- **`laser_sound`, `explosion_sound`, `game_music`**: Loads sound effects and background music.

```python
# sprites 
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf) 
player = Player(all_sprites)
```

- **`all_sprites`, `meteor_sprites`, `laser_sprites`**: Groups to manage different types of sprites.
- **`Star(...)`**: Creates background stars.
- **`player`**: Creates the player sprite.

```python
# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)
```

- **`meteor_event`**: Defines a custom event for creating meteors.
- **`pygame.time.set_timer`**: Triggers the custom event every 500 milliseconds to create new meteors.

```python
while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
    all_sprites.update(dt)
    collisions()

    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
```

- **`dt`**: Delta time, the time elapsed since the last frame, used to ensure smooth movement.
- **Event Loop**: Handles events like quitting the game and creating meteors.
- **`all_sprites.update(dt)`**: Updates all sprites.
- **`collisions()`**: Checks for collisions between sprites.
- **`display_surface.fill('#3a2e3f')`**: Fills the screen with a background color.
- **`display_score()`**: Displays the score.
- **`all_sprites.draw(display_surface)`**: Draws all sprites on the screen.
- **`pygame.display.update()`**: Updates the display with the drawn content.
- **`pygame.quit()`**: Quits pygame and cleans up resources when the game loop ends.