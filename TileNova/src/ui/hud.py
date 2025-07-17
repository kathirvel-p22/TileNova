import pygame
import math
from config import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 36)
        self.animation_time = 0
        
    def draw(self, score, moves_left, target_score, level):
        """Draw the enhanced HUD elements with animations"""
        self.animation_time += 0.1
        
        # Enhanced HUD background with gradient effect
        hud_rect = pygame.Rect(BOARD_OFFSET_X + BOARD_WIDTH * TILE_SIZE + 20, BOARD_OFFSET_Y, 220, 450)
        
        # Create gradient background
        gradient_surface = pygame.Surface((hud_rect.width, hud_rect.height))
        for y in range(hud_rect.height):
            color_factor = y / hud_rect.height
            r = int(DARK_GRAY[0] * (1 - color_factor * 0.3))
            g = int(DARK_GRAY[1] * (1 - color_factor * 0.3))
            b = int(DARK_GRAY[2] * (1 - color_factor * 0.3))
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (hud_rect.width, y))
        
        self.screen.blit(gradient_surface, hud_rect.topleft)
        
        # Animated border
        border_color = (100 + int(50 * abs(math.sin(self.animation_time))), 
                       100 + int(50 * abs(math.sin(self.animation_time + 1))), 
                       255)
        pygame.draw.rect(self.screen, border_color, hud_rect, 3, border_radius=10)
        
        y_offset = hud_rect.y + 20
        
        # Animated Level title
        level_scale = 1.0 + 0.1 * abs(math.sin(self.animation_time * 2))
        level_text = self.font_title.render(f"LEVEL {level}", True, CYAN)
        if level_scale != 1.0:
            original_size = level_text.get_size()
            new_size = (int(original_size[0] * level_scale), int(original_size[1] * level_scale))
            level_text = pygame.transform.scale(level_text, new_size)
        
        level_rect = level_text.get_rect(centerx=hud_rect.centerx, y=y_offset)
        self.screen.blit(level_text, level_rect)
        y_offset += 50
        
        # Score section with glow effect
        self.draw_section_header("SCORE", hud_rect.x + 10, y_offset, YELLOW)
        y_offset += 30
        
        score_text = self.font_large.render(f"{score:,}", True, WHITE)
        # Add glow effect for high scores
        if score > target_score * 0.8:
            glow_color = (255, 255, 0, 100)
            glow_surface = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)
            glow_surface.fill(glow_color)
            self.screen.blit(glow_surface, (hud_rect.x + 10 - 2, y_offset - 2))
            self.screen.blit(glow_surface, (hud_rect.x + 10 + 2, y_offset + 2))
        
        self.screen.blit(score_text, (hud_rect.x + 10, y_offset))
        y_offset += 40
        
        # Target Score
        self.draw_section_header("TARGET", hud_rect.x + 10, y_offset, ORANGE)
        y_offset += 30
        
        target_text = self.font.render(f"{target_score:,}", True, YELLOW)
        self.screen.blit(target_text, (hud_rect.x + 10, y_offset))
        y_offset += 40
        
        # Enhanced Progress bar with animation
        progress = min(1.0, score / target_score)
        progress_rect = pygame.Rect(hud_rect.x + 10, y_offset, 200, 25)
        
        # Background
        pygame.draw.rect(self.screen, (40, 40, 40), progress_rect, border_radius=12)
        
        if progress > 0:
            fill_width = int(progress_rect.width * progress)
            fill_rect = pygame.Rect(progress_rect.x, progress_rect.y, fill_width, progress_rect.height)
            
            # Animated progress color
            if progress >= 1.0:
                color = GREEN
                # Add sparkle effect when complete
                sparkle_alpha = int(128 + 127 * abs(math.sin(self.animation_time * 5)))
                sparkle_surface = pygame.Surface((fill_width, progress_rect.height), pygame.SRCALPHA)
                sparkle_surface.fill((*WHITE, sparkle_alpha))
                pygame.draw.rect(sparkle_surface, (*WHITE, sparkle_alpha), sparkle_surface.get_rect(), border_radius=12)
                self.screen.blit(sparkle_surface, fill_rect.topleft)
            else:
                # Gradient progress bar
                color = (int(255 * (1 - progress)), int(255 * progress), 0)
            
            pygame.draw.rect(self.screen, color, fill_rect, border_radius=12)
        
        # Progress bar border
        pygame.draw.rect(self.screen, WHITE, progress_rect, 2, border_radius=12)
        
        # Progress percentage text
        progress_text = self.font.render(f"{int(progress * 100)}%", True, WHITE)
        progress_text_rect = progress_text.get_rect(center=progress_rect.center)
        self.screen.blit(progress_text, progress_text_rect)
        y_offset += 50
        
        # Moves Left with warning animation
        self.draw_section_header("MOVES LEFT", hud_rect.x + 10, y_offset, LIGHT_GRAY)
        y_offset += 30
        
        moves_color = WHITE
        if moves_left <= 5:
            # Pulsing red warning
            pulse = abs(math.sin(self.animation_time * 3))
            moves_color = (255, int(100 * pulse), int(100 * pulse))
        elif moves_left <= 10:
            moves_color = YELLOW
        
        moves_text = self.font_large.render(str(moves_left), True, moves_color)
        self.screen.blit(moves_text, (hud_rect.x + 10, y_offset))
        y_offset += 60
        
        # Enhanced Controls section
        self.draw_section_header("CONTROLS", hud_rect.x + 10, y_offset, CYAN)
        y_offset += 30
        
        controls = [
            ("Swipe", "Move tiles"),
            ("ESC", "Pause game"),
            ("R", "Restart level"),
            ("H", "Show hint")
        ]
        
        small_font = pygame.font.Font(None, 18)
        for key, action in controls:
            key_text = small_font.render(key, True, YELLOW)
            action_text = small_font.render(f"- {action}", True, LIGHT_GRAY)
            
            self.screen.blit(key_text, (hud_rect.x + 10, y_offset))
            self.screen.blit(action_text, (hud_rect.x + 50, y_offset))
            y_offset += 22
    
    def draw_section_header(self, text, x, y, color):
        """Draw a section header with underline"""
        header_text = self.font.render(text, True, color)
        self.screen.blit(header_text, (x, y))
        
        # Underline
        underline_rect = pygame.Rect(x, y + header_text.get_height() + 2, header_text.get_width(), 2)
        pygame.draw.rect(self.screen, color, underline_rect)
