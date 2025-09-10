"""
Arianna Ford
Pygame Test
Version 1.1
Last Revised: 9/10/2025
"""

import os
import pygame
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

def asset_path(*path_parts):
    return os.path.join(base_dir, "assets", *path_parts)

class Player(pygame.sprite.Sprite):
    """
    Player class representing the main character in the game.
    
    Attributes:
        frames (list), images (dict), walk_direction (int), frame_index (int), image (Surface), rect (Rect), 
        animation_speed (float), frame_timer (float), moving (bool), speed (int), hitbox (Rect)

    Methods:
        __init__(self, x, y): Initializes the player at the given position.
        load_spritesheet(self, filename, frame_width, frame_height): Loads animation frames from a spritesheet.
        update(self): Updates the player's movement and animation based on user input.
        handle_camera(self): Adjusts the camera position to follow the player within a deadzone.
    """
    def __init__(self, x, y):
        """
        Initializes the player character with its starting position.
        
        Args:
            x (int): Initial x-coordinate of the player.
            y (int): Initial y-coordinate of the player.
        """
        super().__init__()
        self.frames = self.load_spritesheet(asset_path("images","walking-frames-1.png"), 16, 16) # A list of sprite frames for player animations
        self.images = {
            "up": pygame.image.load(asset_path("images", "player-up.png")).convert_alpha(),
            "down": pygame.image.load(asset_path("images", "player-down.png")).convert_alpha(),
            "left": pygame.image.load(asset_path("images", "player-left.png")).convert_alpha(),
            "right": pygame.image.load(asset_path("images", "player-right.png")).convert_alpha()
        } # A dictionary holding static images(up, down, left, right)
        self.walk_direction = 1 # current walking direction(0=up, 1=down, 2=left, 3=right)
        self.frame_index = 0 # index of current sprite frame
        self.image = self.frames[self.walk_direction][self.frame_index] # image displayed for player depending on direction facing
        self.rect = self.image.get_rect(center=(x, y)) # pygame.Rect object defining player's position
        self.animation_speed = 0.15 # Controls speed of walking animation
        self.frame_timer = 0 # Timer to control frame switching for the animation
        self.moving = False # boolean indicating if player is moving
        self.speed = 1 # Spped at which player moves
        self.hitbox = pygame.Rect(self.rect.centerx - 4, self.rect.centery - 4, 8, 8) # Smaller rectangle for collision detection, centered around player

    
    def load_spritesheet(self, filename, frame_width, frame_height):
        """
        Loads animation frames from a spritesheet.
        """
        sheet = pygame.image.load(filename).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()

        frames = []
        for y in range(0, sheet_height, frame_height):
            row = []
            for x in range(0, sheet_width, frame_width):
                frame = sheet.subsurface((x, y, frame_width, frame_height))
                row.append(frame)
            frames.append(row)
        return frames


    def update(self):
        """
        Updates the player's position and handles walking animation.
        Moves the player based on arrow key inputs, updates the frame index
        for animation, and ensures the player stays within the world bounds.
        """
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        self.moving = False
        if keys[pygame.K_UP]:
            dy = -player.speed
            self.walk_direction = 0
            self.moving = True
        if keys[pygame.K_DOWN]:
            dy = player.speed
            self.walk_direction = 1
            self.moving = True
        if keys[pygame.K_LEFT]:
            dx = -player.speed
            self.walk_direction = 2
            self.moving = True
        if keys[pygame.K_RIGHT]:
            dx = player.speed
            self.walk_direction = 3   
            self.moving = True     
        self.rect.x += dx
        self.rect.y += dy
        if self.moving:
            self.frame_timer += self.animation_speed
            if self.frame_timer >= 1:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.walk_direction])
        else:
            self.frame_index = 0 #idle frame
        
        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, world_height - self.rect.height))
        self.image = self.frames[self.walk_direction][self.frame_index]



    def handle_camera(self):
        """
        Adjusts the camera's position to keep the player in the center of the screen.
        The camera follows the player, ensuring they remain within a "deadzone" area.
        
        Returns:
            tuple: The camera's x and y offset (cam_x, cam_y).
        """
        cam_x, cam_y = 0, 0
        deadzone = pygame.Rect(
            game_width // 2 - 30, 
            game_height // 2 - 20, 
            60, 
            40
        )

        screen_x = self.rect.x - cam_x
        screen_y = self.rect.y - cam_y

        if screen_x < deadzone.left:
            cam_x -= deadzone.left - screen_x
        elif screen_x > deadzone.right:
            cam_x += screen_x - deadzone.right

        if screen_y < deadzone.top:
            cam_y -= deadzone.top - screen_y
        elif screen_y > deadzone.bottom:
            cam_y += screen_y - deadzone.bottom

        cam_x = max(0, min(cam_x, world_width - game_width))
        cam_y = max(0, min(cam_y, world_height - game_height))

        return cam_x, cam_y









if __name__ == '__main__':
    pygame.init()
    game_width, game_height = 160, 120
    window_width, window_height = 640, 480
    world_width = 1000
    world_height = 1000

    screen = pygame.display.set_mode((window_width, window_height))
    game_surface = pygame.Surface((game_width, game_height))

    player = Player(world_width//2, world_height//2)
    all_sprites = pygame.sprite.Group(player)

    pygame.display.set_caption("My Game")
    scenery = []
    for i in range(200):
        x = (i * 37) % world_width
        y = (i * 29) % world_height
        scenery.append(pygame.Rect(x, y, 6, 6))
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.update()

        cam_x, cam_y = player.handle_camera()
        room_bg = pygame.image.load(asset_path("images", "background-test.png")).convert()
        #game_surface.fill((20, 20, 10))
        game_surface.blit(room_bg, (-cam_x, -cam_y))
        game_surface.blit(player.image, (player.rect.x - cam_x, player.rect.y - cam_y))

        scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
        screen.blit(scaled_surface, (0,0))
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()
    





