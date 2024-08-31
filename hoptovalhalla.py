import os
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
JUMP_STRENGTH = -10

# Top parent class, responsible for variables needed to draw an object
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, image, width, height, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

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
        if keys[pygame.K_SPACE] and self.on_ground:
            self.speed.y = JUMP_STRENGTH
            self.on_ground = False

        self.acceleration = GRAVITY
        self.speed += self.acceleration
        self.rect.y += self.speed.y

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

    def create_player(self):
        pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        player = Player((0, 0, 255), None, PLAYER_WIDTH, PLAYER_HEIGHT, pos)
        self.player.add(player)
        self.all_sprites.add(player)

    def create_platform(self, pos):
        platform = Platform((128, 128, 128), None, PLATFORM_WIDTH, PLATFORM_HEIGHT, pos)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

    def generate_platforms(self):
        for i in range(5):
            x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            y = SCREEN_HEIGHT - i * 120
            self.create_platform(Vector2(x, y))

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
        self.screen.fill((0, 0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Platform Jumper')
        self.create_player()
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
                if self.score % 100 == 0:
                    x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                    y = player.rect.top - 120
                    self.create_platform(Vector2(x, y))

            self.update_game()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.game_loop()