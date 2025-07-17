import pygame
import sys
from config import *
from board import Board
from ui.intro_screen import IntroScreen
from ui.pause_menu import PauseMenu
from ui.hud import HUD
from level_manager import LevelManager
from database import Database
from sound_manager import SoundManager
from effects import Effects

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.state = MENU
        self.score = 0
        self.moves_left = 20
        self.level = 1
        self.target_score = 3000
        
        # Initialize managers
        self.level_manager = LevelManager()
        self.db = Database()
        self.sound_manager = SoundManager()
        self.effects = Effects()
        
        # Initialize UI components
        self.intro_screen = IntroScreen(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        self.hud = HUD(self.screen)
        
        # Game state
        self.selected_tile = None
        self.processing_matches = False
        self.combo_multiplier = 1
        self.is_swiping = False
        self.swipe_start_pos = None
        self.boost_multiplier = 1.5
        
        # Load level data
        self.load_level(1)
        
    def load_level(self, level_num):
        """Load a specific level"""
        level_data = self.level_manager.load_level(level_num)
        if level_data:
            self.level = level_data.get('level', 1)
            self.target_score = level_data.get('target_score', 3000)
            self.moves_left = level_data.get('moves', 20)
            self.score = 0
            self.combo_multiplier = 1
            self.board.initialize()
        
    def handle_event(self, event):
        """Handle game events"""
        if self.state == MENU:
            result = self.intro_screen.handle_event(event)
            if result == "start":
                self.state = PLAYING
                self.load_level(1)
            elif result == "quit":
                return False
                
        elif self.state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = PAUSED
                elif event.key == pygame.K_r:
                    self.load_level(self.level)  # Restart level
                elif event.key == pygame.K_h:
                    self.show_hint()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.processing_matches:
                self.is_swiping = True
                self.swipe_start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and self.is_swiping:
                self.is_swiping = False
                self.handle_swipe(self.swipe_start_pos, event.pos)
            elif event.type == pygame.MOUSEMOTION and self.is_swiping:
                # Optional: Visual feedback during swipe
                pass
                
        elif self.state == PAUSED:
            result = self.pause_menu.handle_event(event)
            if result == "resume":
                self.state = PLAYING
            elif result == "restart":
                self.load_level(self.level)
                self.state = PLAYING
            elif result == "menu":
                self.state = MENU
            elif result == "quit":
                return False
                
        elif self.state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.load_level(self.level)
                    self.state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = MENU
                    
        return True
    
    
    def deselect_tile(self):
        """Deselect the currently selected tile"""
        if self.selected_tile:
            tile = self.board.get_tile_at(*self.selected_tile)
            if tile:
                tile.set_selected(False)
        self.selected_tile = None
        self.board.selected_tile = None
    
    def try_swap(self, pos1, pos2):
        """Try to swap two tiles"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Check if tiles are adjacent
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False
        
        tile1 = self.board.get_tile_at(x1, y1)
        tile2 = self.board.get_tile_at(x2, y2)
        
        # Check if either tile is a special tile
        if tile1 and tile1.is_special_tile():
            affected_positions = self.board.activate_special_tile(x1, y1)
            if affected_positions:
                self.activate_special_effects(affected_positions, tile1.get_special_type())
                return True
        
        if tile2 and tile2.is_special_tile():
            affected_positions = self.board.activate_special_tile(x2, y2)
            if affected_positions:
                self.activate_special_effects(affected_positions, tile2.get_special_type())
                return True
            
        # Perform the swap
        if self.board.swap_tiles(pos1, pos2):
            # Check if swap creates matches
            matches, _ = self.board.check_matches()
            if matches:
                return True
            else:
                # Swap back if no matches
                self.board.swap_tiles(pos1, pos2)
                return False
        
        return False
    
    def activate_special_effects(self, affected_positions, special_type):
        """Activate special tile effects"""
        # Remove affected tiles and add score
        removed_count = 0
        for x, y in affected_positions:
            tile = self.board.get_tile_at(x, y)
            if tile:
                # Add visual effect
                screen_x = BOARD_OFFSET_X + x * TILE_SIZE + TILE_SIZE // 2
                screen_y = BOARD_OFFSET_Y + y * TILE_SIZE + TILE_SIZE // 2
                
                if special_type == SPECIAL_TILE_ROCKET:
                    self.effects.add_particle_explosion((screen_x, screen_y), ORANGE, 20)
                elif special_type == SPECIAL_TILE_LIGHTNING:
                    self.effects.add_particle_explosion((screen_x, screen_y), PURPLE, 25)
                elif special_type == SPECIAL_TILE_BOMB:
                    self.effects.add_particle_explosion((screen_x, screen_y), RED, 15)
                
                # Remove tile
                self.board.tiles.remove(tile)
                self.board.grid[y][x] = None
                removed_count += 1
        
        # Add score for special tile activation
        points = removed_count * 20 * self.combo_multiplier  # Higher points for special tiles
        self.score += points
        
        # Show score popup
        if removed_count > 0:
            center_x = BOARD_OFFSET_X + BOARD_WIDTH * TILE_SIZE // 2
            center_y = BOARD_OFFSET_Y + BOARD_HEIGHT * TILE_SIZE // 2
            self.effects.add_score_popup((center_x, center_y), points)
        
        # Apply gravity and fill spaces
        self.board.apply_gravity()
        self.board.fill_empty_spaces()
        self.wait_for_animations()
        
        # Process any new matches created
        self.process_matches()
    
    def process_matches(self):
        """Process all matches and cascading effects"""
        self.processing_matches = True
        
        while True:
            matches, match_groups = self.board.check_matches()
            if not matches:
                break
            
            # Create special tiles for 4+ matches before removing tiles
            special_tiles = self.board.create_special_tiles(match_groups)
            
            # Remove matches and update score
            removed_count = self.board.remove_matches(matches)
            points = removed_count * 10 * self.combo_multiplier
            if self.is_swiping:
                points *= self.boost_multiplier
            self.score += points
            
            # Add visual effects for matches
            for match_pos in matches:
                screen_x = BOARD_OFFSET_X + match_pos[0] * TILE_SIZE + TILE_SIZE // 2
                screen_y = BOARD_OFFSET_Y + match_pos[1] * TILE_SIZE + TILE_SIZE // 2
                self.effects.add_particle_explosion((screen_x, screen_y), YELLOW, 15)
            
            # Show score popup
            if matches:
                center_x = BOARD_OFFSET_X + BOARD_WIDTH * TILE_SIZE // 2
                center_y = BOARD_OFFSET_Y + BOARD_HEIGHT * TILE_SIZE // 2
                self.effects.add_score_popup((center_x, center_y), points)
            
            # Show combo effect for multipliers > 1
            if self.combo_multiplier > 1:
                combo_x = BOARD_OFFSET_X + BOARD_WIDTH * TILE_SIZE // 2
                combo_y = BOARD_OFFSET_Y + 50
                self.effects.add_combo_effect((combo_x, combo_y), self.combo_multiplier)
            
            self.combo_multiplier += 1
            
            # Play sound effect
            self.sound_manager.play_match_sound()
            
            # Apply gravity
            self.board.apply_gravity()
            
            # Fill empty spaces
            self.board.fill_empty_spaces()
            
            # Place special tiles after gravity and filling
            for x, y, special_tile in special_tiles:
                self.board.place_special_tile(x, y, special_tile)
                # Add special effect for special tile creation
                screen_x = BOARD_OFFSET_X + x * TILE_SIZE + TILE_SIZE // 2
                screen_y = BOARD_OFFSET_Y + y * TILE_SIZE + TILE_SIZE // 2
                self.effects.add_particle_explosion((screen_x, screen_y), CYAN, 25)
            
            # Wait for animations to complete
            self.wait_for_animations()
        
        self.processing_matches = False
        self.check_game_state()
    
    def wait_for_animations(self):
        """Wait for tile animations to complete"""
        waiting = True
        while waiting:
            self.board.update()
            waiting = self.board.animation_in_progress
            
            # Draw frame during animation
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def check_game_state(self):
        """Check if game is won, lost, or continues"""
        if self.score >= self.target_score:
            # Level completed
            self.level += 1
            if self.level_manager.has_level(self.level):
                self.load_level(self.level)
            else:
                # Game completed
                self.state = GAME_OVER
                
        elif self.moves_left <= 0:
            # Game over
            self.state = GAME_OVER
            
        elif not self.board.has_possible_moves():
            # No moves available, shuffle board
            self.board.shuffle_board()
    
    def show_hint(self):
        """Show a hint for possible moves"""
        possible_moves = self.board.get_possible_moves()
        if possible_moves:
            # Highlight first possible move
            move = possible_moves[0]
            pos1, pos2 = move
            # Could implement visual hint here
            print(f"Hint: Try swapping tiles at {pos1} and {pos2}")
    
    def handle_swipe(self, start_pos, end_pos):
        """Handle a swipe gesture to swap tiles with improved detection."""
        if not start_pos or not end_pos:
            return

        # Calculate swipe distance and direction
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        swipe_distance = (dx**2 + dy**2)**0.5
        
        # Minimum swipe distance to register
        if swipe_distance < 30:
            return

        start_grid_x = (start_pos[0] - BOARD_OFFSET_X) // TILE_SIZE
        start_grid_y = (start_pos[1] - BOARD_OFFSET_Y) // TILE_SIZE

        # Check if starting position is valid
        if not (0 <= start_grid_x < BOARD_WIDTH and 0 <= start_grid_y < BOARD_HEIGHT):
            return

        # Determine swipe direction with improved logic
        end_grid_x, end_grid_y = start_grid_x, start_grid_y
        
        if abs(dx) > abs(dy):  # Horizontal swipe
            if dx > 0:
                end_grid_x += 1
            else:
                end_grid_x -= 1
        else:  # Vertical swipe
            if dy > 0:
                end_grid_y += 1
            else:
                end_grid_y -= 1

        # Check bounds for end position
        if not (0 <= end_grid_x < BOARD_WIDTH and 0 <= end_grid_y < BOARD_HEIGHT):
            return

        # Visual feedback for swipe
        self.show_swipe_feedback(start_pos, end_pos)

        # Try to perform the swap
        if self.try_swap((start_grid_x, start_grid_y), (end_grid_x, end_grid_y)):
            self.moves_left -= 1
            self.combo_multiplier = 1
            self.process_matches()
        else:
            # Show invalid move feedback
            self.show_invalid_move_feedback((start_grid_x, start_grid_y), (end_grid_x, end_grid_y))

    def show_swipe_feedback(self, start_pos, end_pos):
        """Show visual feedback for swipe gesture"""
        # Add swipe trail effect to effects manager
        self.effects.add_swipe_trail(start_pos, end_pos)
    
    def show_invalid_move_feedback(self, pos1, pos2):
        """Show feedback for invalid moves"""
        # Flash the tiles red to indicate invalid move
        tile1 = self.board.get_tile_at(*pos1)
        tile2 = self.board.get_tile_at(*pos2)
        
        if tile1:
            self.effects.add_flash_effect(tile1, RED)
        if tile2:
            self.effects.add_flash_effect(tile2, RED)

    def update(self):
        """Update game state"""
        if self.state == PLAYING and not self.processing_matches:
            self.board.update()
            
            # Check for automatic matches (shouldn't happen in match-3)
            if not self.processing_matches:
                matches = self.board.check_matches()
                if matches:
                    self.process_matches()
        
        # Always update effects
        self.effects.update()
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(BLACK)
        
        if self.state == MENU:
            self.intro_screen.draw()
            
        elif self.state == PLAYING:
            self.board.draw(self.screen)
            self.hud.draw(self.score, self.moves_left, self.target_score, self.level)
            self.effects.draw(self.screen)
            
        elif self.state == PAUSED:
            self.board.draw(self.screen)
            self.hud.draw(self.score, self.moves_left, self.target_score, self.level)
            self.effects.draw(self.screen)
            self.pause_menu.draw()
            
        elif self.state == GAME_OVER:
            self.board.draw(self.screen)
            self.hud.draw(self.score, self.moves_left, self.target_score, self.level)
            self.effects.draw(self.screen)
            self.draw_game_over()
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        if self.score >= self.target_score:
            text = font.render("LEVEL COMPLETE!", True, GREEN)
        else:
            text = font.render("GAME OVER", True, RED)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Score text
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("Press R to restart, ESC for menu", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(inst_text, inst_rect)
