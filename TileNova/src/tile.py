import pygame
import random
import os
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        self.tile_type = tile_type
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE + BOARD_OFFSET_X
        self.y = y * TILE_SIZE + BOARD_OFFSET_Y
        self.target_x = self.x
        self.target_y = self.y
        self.selected = False
        self.matched = False
        self.falling = False
        self.fall_speed = 0
        
        # Load fruit image
        self.fruit_image = self.load_fruit_image()
        
        # Create tile surface
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.update_appearance()
    
    def update_appearance(self):
        """Update the tile's visual appearance"""
        self.image.fill((0, 0, 0, 0))  # Clear surface
        
        # Draw fruit image (now with curved square design built-in)
        if self.fruit_image:
            img_rect = self.fruit_image.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
            self.image.blit(self.fruit_image, img_rect)
        else:
            # Fallback: Draw curved square background if no image
            bg_color = TILE_COLORS[self.tile_type % len(TILE_COLORS)]
            pygame.draw.rect(self.image, bg_color, self.image.get_rect(), border_radius=12)
            
        # Add selection glow effect
        if self.selected:
            glow_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            glow_color = (255, 255, 255, 100)
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=12)
            self.image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
            # Add pulsing border
            border_alpha = int(128 + 127 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            border_color = (*WHITE, border_alpha)
            border_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, border_surface.get_rect(), 3, border_radius=12)
            self.image.blit(border_surface, (0, 0))
    
    def update(self):
        """Update tile position and animation"""
        if self.falling:
            self.fall_speed += 0.5  # Gravity
            self.y += self.fall_speed
            self.rect.y = int(self.y)
            
            # Check if reached target position
            if self.y >= self.target_y:
                self.y = self.target_y
                self.rect.y = int(self.y)
                self.falling = False
                self.fall_speed = 0
        else:
            # Smooth movement to target position
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            if abs(dx) > 1:
                self.x += dx * 0.2
                self.rect.x = int(self.x)
            else:
                self.x = self.target_x
                self.rect.x = int(self.x)
                
            if abs(dy) > 1:
                self.y += dy * 0.2
                self.rect.y = int(self.y)
            else:
                self.y = self.target_y
                self.rect.y = int(self.y)
    
    def set_position(self, grid_x, grid_y):
        """Set the tile's grid position and update target coordinates"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.target_x = grid_x * TILE_SIZE + BOARD_OFFSET_X
        self.target_y = grid_y * TILE_SIZE + BOARD_OFFSET_Y
    
    def start_falling(self):
        """Start the falling animation"""
        self.falling = True
        self.fall_speed = 0
    
    def set_selected(self, selected):
        """Set the tile's selection state"""
        self.selected = selected
        self.update_appearance()
    
    def set_matched(self, matched):
        """Set the tile's matched state"""
        self.matched = matched
        if matched:
            # Make matched tiles semi-transparent
            self.image.set_alpha(128)
    
    def load_fruit_image(self):
        """Load the image for the tile's fruit type"""
        # Check if it's a special tile
        if self.tile_type >= 100:  # Special tiles start at 100
            from config import SPECIAL_TILES
            image_name = SPECIAL_TILES.get(self.tile_type)
        else:
            image_name = FRUIT_IMAGES.get(self.tile_type)
            
        if image_name:
            path = os.path.join(TILE_ASSETS, image_name)
            try:
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(image, (TILE_SIZE - 15, TILE_SIZE - 15))
            except pygame.error:
                return None
        return None

    def is_special_tile(self):
        """Check if this is a special tile"""
        return self.tile_type >= 100
    
    def get_special_type(self):
        """Get the special tile type"""
        if self.is_special_tile():
            return self.tile_type
        return None

    @staticmethod
    def generate_random_type():
        """Generate a random tile type"""
        return random.randint(0, len(FRUIT_IMAGES) - 1)

class TileGroup(pygame.sprite.Group):
    """Custom sprite group for tiles with additional functionality"""
    
    def __init__(self):
        super().__init__()
    
    def get_tile_at(self, grid_x, grid_y):
        """Get the tile at the specified grid position"""
        for tile in self.sprites():
            if tile.grid_x == grid_x and tile.grid_y == grid_y:
                return tile
        return None
    
    def remove_matched_tiles(self):
        """Remove all tiles marked as matched"""
        for tile in self.sprites():
            if tile.matched:
                self.remove(tile)
    
    def apply_gravity(self):
        """Apply gravity to make tiles fall down"""
        # Sort tiles by y position (bottom to top)
        tiles_by_column = {}
        for tile in self.sprites():
            if tile.grid_x not in tiles_by_column:
                tiles_by_column[tile.grid_x] = []
            tiles_by_column[tile.grid_x].append(tile)
        
        # Process each column
        for column in tiles_by_column.values():
            column.sort(key=lambda t: t.grid_y, reverse=True)  # Bottom to top
            
            # Find empty spaces and move tiles down
            new_positions = []
            for y in range(BOARD_HEIGHT - 1, -1, -1):  # Bottom to top
                tile_found = False
                for tile in column:
                    if tile.grid_y == y and not tile.matched:
                        new_positions.append(tile)
                        tile_found = True
                        break
                
            # Assign new positions
            for i, tile in enumerate(new_positions):
                new_y = BOARD_HEIGHT - 1 - i
                if new_y != tile.grid_y:
                    tile.set_position(tile.grid_x, new_y)
                    tile.start_falling()
