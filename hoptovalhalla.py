import pygame
from pygame import Vector2
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
FONT_SIZE = 30
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 100
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GRAVITY = Vector2(0, 0.5)
HORIZONTAL_SPEED = 5
JUMP_STRENGTH = -15

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
class Platform(pygame.sprite.Sprite):
    def __init__(self, color, image_path, width, height, pos):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            if color:
                self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        
class Menu(Drawable_objects):
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.buttons = {
            "Continue": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            "Settings": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            "Quit Game": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), (BUTTON_WIDTH, BUTTON_HEIGHT))
        }
        self.settings_menu = SettingsMenu(game)

    def draw(self, screen):
        screen.fill((0, 0, 0, 128))  # Semi-transparent background
        for text, rect in self.buttons.items():
            pygame.draw.rect(screen, (255, 255, 255), rect)
            label = self.font.render(text, True, (0, 0, 0))
            screen.blit(label, (rect.x + (BUTTON_WIDTH - label.get_width()) // 2, rect.y + (BUTTON_HEIGHT - label.get_height()) // 2))

    def update(self):
        keys = pygame.key.get_pressed()
    
        # If player presses escape, toggle menu
        if keys[pygame.K_ESCAPE]:
            self.game.menu_active = not self.game.menu_active
            pygame.time.wait(300)  # Debounce the key press

        if self.game.menu_active:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for text, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos) and mouse_click[0]:
                    if text == "Continue":
                        self.game.menu_active = False
                    elif text == "Settings":
                        self.game.settings_active = True
                    elif text == "Quit Game":
                        pygame.quit()
                        exit()

            if self.game.settings_active:
                self.settings_menu.update()
        
class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.buttons = {
            "Mute/Unmute Sound": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            "Change Keybindings": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            "Back": pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 150), (BUTTON_WIDTH, BUTTON_HEIGHT))
        }

    def draw(self, screen):
        screen.fill((0, 0, 0, 128))  # Semi-transparent background
        for text, rect in self.buttons.items():
            pygame.draw.rect(screen, (255, 255, 255), rect)
            label = self.font.render(text, True, (0, 0, 0))
            screen.blit(label, (rect.x + (BUTTON_WIDTH - label.get_width()) // 2, rect.y + (BUTTON_HEIGHT - label.get_height()) // 2))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for text, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos) and mouse_click[0]:
                if text == "Mute/Unmute Sound":
                    self.game.sound_muted = not self.game.sound_muted
                elif text == "Change Keybindings":
                    # Implement keybinding change logic here
                    pass
                elif text == "Back":
                    self.game.settings_active = False
                    
class HighscoreMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.active = False
        self.current_score = 0
        self.name = ""
        self.input_active = False
        self.buttons = {
            "restart": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50),
            "quit": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40, 200, 50)
        }

    def show(self, score):
        self.active = True
        self.current_score = score
        self.name = ""
        self.input_active = True

    def draw(self):
        self.game.screen.fill((0, 0, 0, 128))  # Semi-transparent background
        title = self.font.render("Highscores", True, (255, 255, 255))
        self.game.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        for i, (name, score) in enumerate(self.game.highscores):
            text = f"{i + 1}. {name} {score}"
            if score == self.current_score and self.input_active:
                text += f" {self.name}_"
            score_text = self.font.render(text, True, (255, 255, 255))
            self.game.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 100 + i * 40))

        # Draw buttons
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.buttons["restart"])
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.buttons["quit"])
        restart_text = self.font.render("Restart", True, (255, 255, 255))
        quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.game.screen.blit(restart_text, (self.buttons["restart"].x + 50, self.buttons["restart"].y + 10))
        self.game.screen.blit(quit_text, (self.buttons["quit"].x + 70, self.buttons["quit"].y + 10))

        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                        self.game.highscores.append((self.name, self.current_score))
                        self.game.highscores = sorted(self.game.highscores, key=lambda x: x[1], reverse=True)[:5]
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                        self.game.menu_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["restart"].collidepoint(event.pos):
                    self.active = False
                    self.game.restart_game()
                elif self.buttons["quit"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Game class. Responsible for the game loop, most of the collision detection and creating most of the objects apart from the missiles.
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = pygame.sprite.GroupSingle()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.highscores = []  # Initialize as an empty list
        self.collided_platforms = set()
        self.background_image = pygame.image.load('/home/magnus/dev/hoptovalhalla/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.highscore_menu = HighscoreMenu(self)

    def create_player(self):
        pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        player = Player(None, '/home/magnus/dev/hoptovalhalla/viking.png', PLAYER_WIDTH, PLAYER_HEIGHT, pos)
        self.player.add(player)
        self.all_sprites.add(player)
        
    def create_floor(self, pos):
        self.create_platform(pos, width=PLATFORM_WIDTH, image_path='/home/magnus/dev/hoptovalhalla/floor.png')

    def create_platform(self, pos, width=PLATFORM_WIDTH, image_path='/home/magnus/dev/hoptovalhalla/platform.png'):
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
            for hit in hits:
                if hit not in self.collided_platforms:
                    self.collided_platforms.add(hit)
                    self.score += 1
                player.rect.y = hit.rect.top - PLAYER_HEIGHT
                player.speed.y = 0
                player.on_ground = True

    def update_game(self):
        self.screen.blit(self.background_image, (0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        pygame.display.flip()

    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Platform Jumper')
        self.create_player()
        self.generate_floor()
        self.generate_platforms()
        
        # Load and play background music
        pygame.mixer.music.load('/home/magnus/dev/hoptovalhalla/hop_to_valhalla.mp3')
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.highscore_menu.active:
                self.highscore_menu.update()
                self.highscore_menu.draw()
            else:
                self.check_collisions()

                player = self.player.sprite
                if player.rect.top <= SCREEN_HEIGHT // 4:
                    self.scroll_screen(5)
                    self.generate_platforms()

                if player.rect.top > SCREEN_HEIGHT - 50:
                    # Scroll the screen down until the player reaches the floor
                    while player.rect.bottom < SCREEN_HEIGHT - 1:
                        self.scroll_screen(-5)
                        self.update_game()
                        self.clock.tick(60)
                    # Show highscore menu and enable name input
                    self.highscore_menu.show(self.score)
                    self.score = 0
                    self.collided_platforms.clear()

                self.update_game()
                self.clock.tick(60)

        pygame.quit()
        print("Quit game")

if __name__ == '__main__':
    game = Game()
    game.game_loop()