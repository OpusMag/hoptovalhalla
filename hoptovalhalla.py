import pygame
from pygame import Vector2
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 20
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
GRAVITY = Vector2(0, 0.5)
JUMP_STRENGTH = -20

# Top parent class, responsible for variables needed to draw an object
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, image_path, width, height, pos):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

# Parent class. The child classes inherit from this which in turn inherits from Drawable_objects. Responsible for variables that move objects
class Moving_objects(Drawable_objects):
    def __init__(self, color, image, width, height, pos):
        super().__init__(color, image, width, height, pos)
        self.speed = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

# Player class. Holds the variables for the player object.
class Player(Moving_objects):
    def __init__(self, color, image, width, height, pos):
        super().__init__(color, image, width, height, pos)
        self.speed = Vector2(0, 0)
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Vertical movement (jumping)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.speed.y = JUMP_STRENGTH
            self.on_ground = False

        # Horizontal movement (left and right)
        if keys[pygame.K_LEFT]:
            self.speed.x = -5  # Move left
        elif keys[pygame.K_RIGHT]:
            self.speed.x = 5  # Move right
        else:
            self.speed.x = 0  # Stop horizontal movement if no key is pressed

        self.acceleration = GRAVITY
        self.speed += self.acceleration
        self.rect.y += self.speed.y
        self.rect.x += self.speed.x

# Platform class. Holds the variables for the platform object.
class Platform(Drawable_objects):
    def __init__(self, color, image, width, height, pos):
        super().__init__(color, image, width, height, pos)

# Game class. Responsible for the game loop, most of the collision detection and creating most of the objects apart from the missiles.
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = pygame.sprite.GroupSingle()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.background_image = pygame.image.load('/home/magnus/dev/hoptovalhalla/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_player(self):
        pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        player = Player(None, '/home/magnus/dev/hoptovalhalla/viking.png', PLAYER_WIDTH, PLAYER_HEIGHT, pos)
        self.player.add(player)
        self.all_sprites.add(player)
        
    def create_floor(self, pos):
        self.create_platform(pos, width=PLATFORM_WIDTH, image_path='/home/magnus/dev/hoptovalhalla/ground2')

    def create_platform(self, pos, width=PLATFORM_WIDTH, image_path='/home/magnus/dev/hoptovalhalla/platform2'):
        platform = Platform(None, image_path, width, PLATFORM_HEIGHT, pos)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

    def generate_floor(self):
        num_platforms = SCREEN_WIDTH // PLATFORM_WIDTH
        for i in range(num_platforms):
            x = i * PLATFORM_WIDTH
            y = SCREEN_HEIGHT - PLATFORM_HEIGHT
            self.create_floor(Vector2(x, y))

    def generate_platforms(self):
        if not hasattr(self, 'highest_platform_y'):
            self.highest_platform_y = SCREEN_HEIGHT - PLATFORM_HEIGHT
            while self.highest_platform_y > 0:
                x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                y = self.highest_platform_y
                self.create_platform(Vector2(x, y))
                self.highest_platform_y -= 120

        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = self.highest_platform_y - 120
        self.create_platform(Vector2(x, y))
        self.highest_platform_y = y

    def scroll_screen(self, dy):
        for sprite in self.all_sprites:
            sprite.rect.y += dy

    def check_collisions(self):
        player = self.player.sprite
        if player.speed.y > 0:
            hits = pygame.sprite.spritecollide(player, self.platforms, False)
            if hits:
                player.rect.y = hits[0].rect.top - PLAYER_HEIGHT
                player.speed.y = 0
                player.on_ground = True

    def update_game(self):
        self.screen.blit(self.background_image, (0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Platform Jumper')
        self.create_player()
        self.generate_floor()
        self.generate_platforms()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.check_collisions()

            player = self.player.sprite
            if player.rect.top <= SCREEN_HEIGHT // 4:
                self.scroll_screen(5)
                self.score += 1
                self.generate_platforms()

            if player.rect.top > SCREEN_HEIGHT:
                print("Player fell off the screen")
                running = False

            self.update_game()
            self.clock.tick(60)

        pygame.quit()
        print("Game loop ended")

if __name__ == '__main__':
    game = Game()
    game.game_loop()