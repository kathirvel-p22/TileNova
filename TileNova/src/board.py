import pygame
import random
from config import *
from tile import Tile, TileGroup

class Board:
    def __init__(self):
        self.tiles = TileGroup()
        self.grid = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.selected_tile = None
        self.matches_found = []
        self.combo_count = 0
        self.animation_in_progress = False
        
    def initialize(self):
        """Initialize the board with random tiles"""
        self.tiles.empty()
        self.grid = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                # Generate tile type ensuring no initial matches
                tile_type = self.generate_safe_tile_type(x, y)
                tile = Tile(x, y, tile_type)
                self.tiles.add(tile)
                self.grid[y][x] = tile
    
    def generate_safe_tile_type(self, x, y):
        """Generate a tile type that won't create initial matches"""
        forbidden_types = set()
        
        # Check horizontal matches
        if x >= 2:
            if (self.grid[y][x-1] and self.grid[y][x-2] and 
                self.grid[y][x-1].tile_type == self.grid[y][x-2].tile_type):
                forbidden_types.add(self.grid[y][x-1].tile_type)
        
        # Check vertical matches
        if y >= 2:
            if (self.grid[y-1][x] and self.grid[y-2][x] and 
                self.grid[y-1][x].tile_type == self.grid[y-2][x].tile_type):
                forbidden_types.add(self.grid[y-1][x].tile_type)
        
        # Generate a safe tile type
        available_types = [i for i in range(len(FRUIT_IMAGES)) if i not in forbidden_types]
        if not available_types:
            available_types = list(range(len(FRUIT_IMAGES)))
        
        return random.choice(available_types)
    
    def get_tile_at(self, x, y):
        """Get tile at grid position"""
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            return self.grid[y][x]
        return None
    
    def swap_tiles(self, pos1, pos2):
        """Swap two tiles"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        tile1 = self.get_tile_at(x1, y1)
        tile2 = self.get_tile_at(x2, y2)
        
        if tile1 and tile2:
            # Swap in grid
            self.grid[y1][x1] = tile2
            self.grid[y2][x2] = tile1
            
            # Update tile positions
            tile1.set_position(x2, y2)
            tile2.set_position(x1, y1)
            
            return True
        return False
    
    def check_matches(self):
        """Check for matches on the board and return match info"""
        matches = set()
        match_groups = []  # Store groups with their lengths for special tile creation
        
        # Check horizontal matches
        for y in range(BOARD_HEIGHT):
            count = 1
            current_type = None
            start_x = 0
            
            for x in range(BOARD_WIDTH):
                tile = self.get_tile_at(x, y)
                tile_type = tile.tile_type if tile and not tile.is_special_tile() else None
                
                if tile and tile_type == current_type and current_type is not None:
                    count += 1
                else:
                    if count >= 3 and current_type is not None:
                        group_matches = [(i, y) for i in range(start_x, x)]
                        matches.update(group_matches)
                        match_groups.append({
                            'matches': group_matches,
                            'count': count,
                            'type': current_type,
                            'direction': 'horizontal',
                            'center': (start_x + count // 2, y)
                        })
                    
                    if tile and tile_type is not None:
                        current_type = tile_type
                        start_x = x
                        count = 1
                    else:
                        current_type = None
                        count = 0
            
            # Check end of row
            if count >= 3 and current_type is not None:
                group_matches = [(i, y) for i in range(start_x, BOARD_WIDTH)]
                matches.update(group_matches)
                match_groups.append({
                    'matches': group_matches,
                    'count': count,
                    'type': current_type,
                    'direction': 'horizontal',
                    'center': (start_x + count // 2, y)
                })
        
        # Check vertical matches
        for x in range(BOARD_WIDTH):
            count = 1
            current_type = None
            start_y = 0
            
            for y in range(BOARD_HEIGHT):
                tile = self.get_tile_at(x, y)
                tile_type = tile.tile_type if tile and not tile.is_special_tile() else None
                
                if tile and tile_type == current_type and current_type is not None:
                    count += 1
                else:
                    if count >= 3 and current_type is not None:
                        group_matches = [(x, i) for i in range(start_y, y)]
                        matches.update(group_matches)
                        match_groups.append({
                            'matches': group_matches,
                            'count': count,
                            'type': current_type,
                            'direction': 'vertical',
                            'center': (x, start_y + count // 2)
                        })
                    
                    if tile and tile_type is not None:
                        current_type = tile_type
                        start_y = y
                        count = 1
                    else:
                        current_type = None
                        count = 0
            
            # Check end of column
            if count >= 3 and current_type is not None:
                group_matches = [(x, i) for i in range(start_y, BOARD_HEIGHT)]
                matches.update(group_matches)
                match_groups.append({
                    'matches': group_matches,
                    'count': count,
                    'type': current_type,
                    'direction': 'vertical',
                    'center': (x, start_y + count // 2)
                })
        
        return list(matches), match_groups
    
    def create_special_tiles(self, match_groups):
        """Create special tiles based on match patterns"""
        special_tiles_created = []
        
        for group in match_groups:
            count = group['count']
            center_x, center_y = group['center']
            tile_type = group['type']
            
            # Create special tiles based on match size
            if count == 4:
                # Create rocket bomb
                special_tile = Tile(center_x, center_y, SPECIAL_TILE_ROCKET)
                special_tiles_created.append((center_x, center_y, special_tile))
            elif count >= 5:
                # Create lightning tile
                special_tile = Tile(center_x, center_y, SPECIAL_TILE_LIGHTNING)
                special_tiles_created.append((center_x, center_y, special_tile))
        
        return special_tiles_created
    
    def activate_special_tile(self, x, y):
        """Activate a special tile and return affected positions"""
        tile = self.get_tile_at(x, y)
        if not tile or not tile.is_special_tile():
            return []
        
        affected_positions = []
        special_type = tile.get_special_type()
        
        if special_type == SPECIAL_TILE_ROCKET:
            # Clear entire row and column
            for i in range(BOARD_WIDTH):
                affected_positions.append((i, y))
            for i in range(BOARD_HEIGHT):
                affected_positions.append((x, i))
                
        elif special_type == SPECIAL_TILE_LIGHTNING:
            # Clear all tiles of the same color as the tile that was swapped with it
            # For now, we'll clear all tiles of a random color
            target_color = random.randint(0, len(FRUIT_IMAGES) - 1)
            for board_y in range(BOARD_HEIGHT):
                for board_x in range(BOARD_WIDTH):
                    board_tile = self.get_tile_at(board_x, board_y)
                    if board_tile and board_tile.tile_type == target_color:
                        affected_positions.append((board_x, board_y))
                        
        elif special_type == SPECIAL_TILE_BOMB:
            # Clear 3x3 area around the bomb
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT:
                        affected_positions.append((new_x, new_y))
        
        return affected_positions
    
    def place_special_tile(self, x, y, special_tile):
        """Place a special tile on the board"""
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            # Remove existing tile if any
            existing_tile = self.get_tile_at(x, y)
            if existing_tile:
                self.tiles.remove(existing_tile)
            
            # Place the special tile
            special_tile.set_position(x, y)
            self.tiles.add(special_tile)
            self.grid[y][x] = special_tile
    
    def remove_matches(self, matches):
        """Remove matched tiles from the board"""
        for x, y in matches:
            tile = self.get_tile_at(x, y)
            if tile:
                tile.set_matched(True)
                self.tiles.remove(tile)
                self.grid[y][x] = None
        
        self.matches_found = matches
        return len(matches)
    
    def apply_gravity(self):
        """Apply gravity to make tiles fall"""
        moved = False
        
        for x in range(BOARD_WIDTH):
            # Collect non-None tiles in this column
            column_tiles = []
            for y in range(BOARD_HEIGHT):
                if self.grid[y][x] is not None:
                    column_tiles.append(self.grid[y][x])
                    self.grid[y][x] = None
            
            # Place tiles at the bottom
            for i, tile in enumerate(column_tiles):
                new_y = BOARD_HEIGHT - len(column_tiles) + i
                if new_y != tile.grid_y:
                    moved = True
                    tile.set_position(x, new_y)
                    tile.start_falling()
                self.grid[new_y][x] = tile
        
        return moved
    
    def fill_empty_spaces(self):
        """Fill empty spaces with new tiles"""
        new_tiles = []
        
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.grid[y][x] is None:
                    tile_type = Tile.generate_random_type()
                    tile = Tile(x, y, tile_type)
                    # Start tiles above the board
                    tile.y = -TILE_SIZE * (BOARD_HEIGHT - y)
                    tile.rect.y = tile.y
                    tile.start_falling()
                    
                    self.tiles.add(tile)
                    self.grid[y][x] = tile
                    new_tiles.append(tile)
        
        return new_tiles
    
    def is_valid_move(self, pos1, pos2):
        """Check if a move between two positions is valid"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Check if positions are adjacent
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False
        
        # Temporarily swap tiles
        if self.swap_tiles(pos1, pos2):
            matches = self.check_matches()
            # Swap back
            self.swap_tiles(pos1, pos2)
            return len(matches) > 0
        
        return False
    
    def get_possible_moves(self):
        """Get all possible moves on the board"""
        possible_moves = []
        
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                # Check right
                if x < BOARD_WIDTH - 1:
                    if self.is_valid_move((x, y), (x + 1, y)):
                        possible_moves.append(((x, y), (x + 1, y)))
                
                # Check down
                if y < BOARD_HEIGHT - 1:
                    if self.is_valid_move((x, y), (x, y + 1)):
                        possible_moves.append(((x, y), (x, y + 1)))
        
        return possible_moves
    
    def has_possible_moves(self):
        """Check if there are any possible moves"""
        return len(self.get_possible_moves()) > 0
    
    def shuffle_board(self):
        """Shuffle the board when no moves are available"""
        tile_types = []
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.grid[y][x]:
                    tile_types.append(self.grid[y][x].tile_type)
        
        random.shuffle(tile_types)
        
        index = 0
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.grid[y][x] and index < len(tile_types):
                    self.grid[y][x].tile_type = tile_types[index]
                    self.grid[y][x].update_appearance()
                    index += 1
    
    def update(self):
        """Update the board state"""
        self.tiles.update()
        
        # Check if any tiles are still falling
        falling_tiles = [tile for tile in self.tiles if tile.falling]
        self.animation_in_progress = len(falling_tiles) > 0
    
    def draw(self, screen):
        """Draw the board"""
        # Draw board background
        board_rect = pygame.Rect(
            BOARD_OFFSET_X - 5, 
            BOARD_OFFSET_Y - 5,
            BOARD_WIDTH * TILE_SIZE + 10,
            BOARD_HEIGHT * TILE_SIZE + 10
        )
        pygame.draw.rect(screen, DARK_GRAY, board_rect)
        
        # Draw grid lines
        for x in range(BOARD_WIDTH + 1):
            start_pos = (BOARD_OFFSET_X + x * TILE_SIZE, BOARD_OFFSET_Y)
            end_pos = (BOARD_OFFSET_X + x * TILE_SIZE, BOARD_OFFSET_Y + BOARD_HEIGHT * TILE_SIZE)
            pygame.draw.line(screen, GRAY, start_pos, end_pos, 1)
        
        for y in range(BOARD_HEIGHT + 1):
            start_pos = (BOARD_OFFSET_X, BOARD_OFFSET_Y + y * TILE_SIZE)
            end_pos = (BOARD_OFFSET_X + BOARD_WIDTH * TILE_SIZE, BOARD_OFFSET_Y + y * TILE_SIZE)
            pygame.draw.line(screen, GRAY, start_pos, end_pos, 1)
        
        # Draw tiles
        self.tiles.draw(screen)
        
        # Highlight selected tile
        if self.selected_tile:
            x, y = self.selected_tile
            highlight_rect = pygame.Rect(
                BOARD_OFFSET_X + x * TILE_SIZE,
                BOARD_OFFSET_Y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(screen, YELLOW, highlight_rect, 3)
