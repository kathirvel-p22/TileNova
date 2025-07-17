import pygame
from config import *

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, FONT_SIZE)
        
        # Button definitions
        self.buttons = {
            'resume': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 250, BUTTON_WIDTH, BUTTON_HEIGHT),
            'restart': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 320, BUTTON_WIDTH, BUTTON_HEIGHT),
            'menu': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 390, BUTTON_WIDTH, BUTTON_HEIGHT),
            'quit': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 460, BUTTON_WIDTH, BUTTON_HEIGHT)
        }
        
        self.hovered_button = None
        
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered_button = None
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(event.pos):
                    self.hovered_button = button_name
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(event.pos):
                    return button_name
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "resume"
            elif event.key == pygame.K_r:
                return "restart"
                
        return None
    
    def draw(self):
        """Draw the pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Menu background
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 150, 300, 400)
        pygame.draw.rect(self.screen, DARK_GRAY, menu_rect)
        pygame.draw.rect(self.screen, WHITE, menu_rect, 3)
        
        # Title
        title_text = self.font_title.render("PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button_name, button_rect in self.buttons.items():
            # Button background
            button_color = LIGHT_GRAY if self.hovered_button == button_name else GRAY
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Button text
            button_text = button_name.upper()
            text_surface = self.font_button.render(button_text, True, BLACK if self.hovered_button == button_name else WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
