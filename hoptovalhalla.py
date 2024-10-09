import pygame
from pygame import Vector2
import random
from enum import Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
FONT_SIZE = 30
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 40
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GRAVITY = Vector2(0, 0.5)
HORIZONTAL_SPEED = 5
JUMP_STRENGTH = -15
MIN_V_JUMP_DISTANCE = 100
MIN_H_JUMP_DISTANCE = 320

# Game States
class GameState(Enum):
    RUNNING = 1
    MENU = 2
    SETTINGS = 3
    HIGHSCORE = 4

# Top parent class, responsible for variables needed to draw an object
class DrawableObjects(pygame.sprite.Sprite):
    def __init__(self, color, image_path, width, height, pos):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

# Parent class. The child classes inherit from this which in turn inherits from DrawableObjects. Responsible for variables that move objects
class MovingObjects(DrawableObjects):
    def __init__(self, color, image, width, height, pos):
        super().__init__(color, image, width, height, pos)
        self.speed = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

# Player class. Holds the variables for the player object.
class Player(MovingObjects):
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
            self.speed.x = -HORIZONTAL_SPEED  # Move left
        elif keys[pygame.K_RIGHT]:
            self.speed.x = HORIZONTAL_SPEED  # Move right
        else:
            self.speed.x = 0  # Stop horizontal movement if no key is pressed

        self.acceleration = GRAVITY
        self.speed += self.acceleration
        self.rect.y += self.speed.y
        self.rect.x += self.speed.x
        
class Ravens(MovingObjects):
    def __init__(self, color, image, width, height, pos):
        super().__init__(color, image, width, height, pos)
        self.speed = Vector2(HORIZONTAL_SPEED, 0)  # Move right with a speed of 5 units per frame

    def update(self):
        # Move the raven
        self.rect.x += self.speed.x

        # Wrap around if it goes off the right side of the screen
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

# Platform class. Holds the variables for the platform object.
class Platform(DrawableObjects):
    def __init__(self, color, image_path, width, height, pos):
        super().__init__(color, image_path, width, height, pos)

class Floor(DrawableObjects):
    def __init__(self, color, image_path, width, height, pos):
        super().__init__(color, image_path, width, height, pos)
        
class Menu(DrawableObjects):
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

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                        self.save_score()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["restart"].collidepoint(event.pos):
                    self.restart_game()
                elif self.buttons["quit"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

    def save_score(self):
        self.game.highscores.append((self.name, self.current_score))
        self.game.highscores.sort(key=lambda x: x[1], reverse=True)
        self.game.highscores = self.game.highscores[:10]  # Keep only top 10 scores

    def restart_game(self):
        self.active = False
        self.game.reset_game()

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

# Game class. Responsible for the game loop, most of the collision detection and creating most of the objects apart from the missiles.
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = pygame.sprite.GroupSingle()
        self.ravens = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.highscores = []
        self.highscore_menu = HighscoreMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.settings_active = False
        self.collided_platforms = set()
        self.background_image = pygame.image.load('/home/magnus/dev/hoptovalhalla/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.highscore_menu = HighscoreMenu(self)
        self.state = GameState.RUNNING

    def create_player(self):
        pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
        player = Player(None, '/home/magnus/dev/hoptovalhalla/viking.png', PLAYER_WIDTH, PLAYER_HEIGHT, pos)
        self.player.add(player)
        self.all_sprites.add(player)
        
    def create_ravens(self, pos):
        width = 50  # Example width for the raven
        height = 30  # Example height for the raven
        ravens = Ravens(None, '/home/magnus/dev/hoptovalhalla/raven.png', width, height, pos)
        self.ravens.add(ravens)
        self.all_sprites.add(ravens)
        
    def create_floor(self, pos, width=1800, image_path='/home/magnus/dev/hoptovalhalla/platform.png'):
        floor = Floor(None, image_path, width, 1, pos)
        self.floors.add(floor) 
        self.all_sprites.add(floor)
        
    def create_platform(self, pos, width=PLATFORM_WIDTH, image_path='/home/magnus/dev/hoptovalhalla/platform1.png'):
        platform = Platform(None, image_path, width, PLATFORM_HEIGHT, pos)
        self.platforms.add(platform)
        self.all_sprites.add(platform)
        
    def generate_ravens(self):
        num_ravens = self.score // 25

        for _ in range(num_ravens):
            x = 0  # Start from the left side of the screen
            y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
            self.create_ravens(Vector2(x, y))

        for _ in range(num_ravens):
            x = 0  # Start from the left side of the screen
            y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
            self.create_ravens(Vector2(x, y))

    def generate_floor(self):
        # Position the floor at the bottom of the screen
        pos = (0, SCREEN_HEIGHT - 1)  # Assuming the floor height is 20 pixels
        self.create_floor(pos)

    def generate_platforms(self):
        if not hasattr(self, 'highest_platform_y'):
            # Set the initial highest platform position to be the minimum jump distance from the floor
            self.highest_platform_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - MIN_V_JUMP_DISTANCE
            self.previous_platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            while self.highest_platform_y > 0:
                x = random.randint(max(0, self.previous_platform_x - MIN_H_JUMP_DISTANCE), 
                                min(SCREEN_WIDTH - PLATFORM_WIDTH, self.previous_platform_x + MIN_H_JUMP_DISTANCE))
                y = self.highest_platform_y
                self.create_platform(Vector2(x, y))
                self.highest_platform_y -= MIN_V_JUMP_DISTANCE  # Use the minimum jump distance for spacing
                self.previous_platform_x = x

        x = random.randint(max(0, self.previous_platform_x - MIN_H_JUMP_DISTANCE), 
                        min(SCREEN_WIDTH - PLATFORM_WIDTH, self.previous_platform_x + MIN_H_JUMP_DISTANCE))
        y = self.highest_platform_y - MIN_V_JUMP_DISTANCE  # Use the minimum jump distance for spacing
        self.create_platform(Vector2(x, y))
        self.highest_platform_y = y
        self.previous_platform_x = x

    def scroll_screen(self, dy):
        for sprite in self.all_sprites:
            sprite.rect.y += dy

    def check_collisions(self):
        player = self.player.sprite

        if player.speed.y >= 0:
            # Check collisions with the floor
            floor_hits = pygame.sprite.spritecollide(player, self.floors, False)
            for hit in floor_hits:
                if player.rect.bottom <= hit.rect.top + player.speed.y:
                    player.rect.bottom = hit.rect.top
                    player.speed.y = 0
                    player.on_ground = True

            # Check collisions with platforms
            platform_hits = pygame.sprite.spritecollide(player, self.platforms, False)
            for hit in platform_hits:
                if player.rect.bottom <= hit.rect.top + player.speed.y:
                    if hit not in self.collided_platforms:
                        self.collided_platforms.add(hit)
                        self.score += 1
                    player.rect.bottom = hit.rect.top
                    player.speed.y = 0
                    player.on_ground = True

        # Check collisions with ravens
        raven_hits = pygame.sprite.spritecollide(player, self.ravens, False)
        for hit in raven_hits:
            if player.rect.left <= hit.rect.right:
                self.highscore_menu.active = True 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.settings_active = not self.settings_active

    def update_game(self):
        self.screen.blit(self.background_image, (0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        pygame.display.flip()
        
    def reset_game(self):
        # Reset game state
        self.player.empty()  # Clear player
        self.platforms.empty()  # Clear platforms
        self.all_sprites.empty()  # Clear all sprites
        self.generate_floor()  # Generate floor
        self.generate_platforms()  # Generate initial platforms
        self.score = 0  # Reset score
        self.highscore_menu.active = False  # Deactivate highscore menu
        self.create_player()  # Create a new player

    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Hop to Valhalla')
        self.generate_floor()
        self.generate_platforms()
        self.create_player()
        global GRAVITY
        
        # Load and play background music
        pygame.mixer.music.load('/home/magnus/dev/hoptovalhalla/hop_to_valhalla.mp3')
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.settings_active = not self.settings_active
            
            player = self.player.sprite  # Access the player object from the group

            if player.on_ground:
                GRAVITY = Vector2(0, 0)
            else:
                GRAVITY = Vector2(0, 0.5)
                
            if self.settings_active:
                self.settings_menu.update()
                self.settings_menu.draw(self.screen)
            elif self.highscore_menu.active:
                self.highscore_menu.update()
                self.highscore_menu.draw()
            else:
                self.check_collisions()

                player = self.player.sprite
                if player.rect.top <= SCREEN_HEIGHT // 4:
                    self.scroll_screen(5)
                    self.generate_platforms()

                if player.rect.bottom > SCREEN_HEIGHT - 1 and not player.on_ground:
                    self.scroll_screen(-5)
                    self.generate_platforms()

                self.update_game()
                self.clock.tick(60)

        pygame.quit()
        print("Quit game")

if __name__ == '__main__':
    game = Game()
    game.game_loop()
