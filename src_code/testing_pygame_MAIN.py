"""
Arianna Ford




"""
#import time
import os
import pygame
import sys
from src.utils import asset_path


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_spritesheet(asset_path("images","walking-frames-1.png"), 16, 16)
        self.images = {
            "up": pygame.image.load("player-up.png").convert_alpha(),
            "down": pygame.image.load("player-down.png").convert_alpha(),
            "left": pygame.image.load("player-left.png").convert_alpha(),
            "right": pygame.image.load("player-right.png").convert_alpha()
        }
        self.walk_direction = 1 # 0=up, 1=down, 2=left, 3=right
        self.frame_index = 0
        self.image = self.frames[self.walk_direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        #self.image = self.images[self.walk_direction]
        #self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.moving = False
        self.speed = 1
        self.hitbox = pygame.Rect(self.rect.centerx - 4, self.rect.centery - 4, 8, 8)

    
    def load_spritesheet(self, filename, frame_width, frame_height):
        #Cut sprite into frames:returns [direction][frame]
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
    project_root = os.path.dirname(os.path.dirname(__file__))
    assets_dir = os.path.join(project_root, "assets")

    def asset_path(*path_parts):
        return os.path.join(assets_dir, *path_parts)
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
        room_bg = pygame.image.load("background-test.png")
        #game_surface.fill((20, 20, 10))
        game_surface.blit(room_bg, (-cam_x, -cam_y))

        """for rect in scenery:
            pygame.draw.rect(game_surface, (100, 200, 10), 
                            (rect.x - cam_x, rect.y - cam_y, rect.width, rect.height))"""
        


        
        game_surface.blit(player.image, (player.rect.x - cam_x, player.rect.y - cam_y))

        scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
        screen.blit(scaled_surface, (0,0))
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()
    





