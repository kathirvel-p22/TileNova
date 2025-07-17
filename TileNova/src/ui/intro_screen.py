import pygame
import math
import random
from config import *

class IntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, TITLE_FONT_SIZE + 20)
        self.font_button = pygame.font.Font(None, FONT_SIZE)
        self.font_small = pygame.font.Font(None, 20)
        self.animation_time = 0
        
        # Button definitions with better positioning
        self.buttons = {
            'start': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 320, BUTTON_WIDTH, BUTTON_HEIGHT + 10),
            'quit': pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT + 10)
        }
        
        self.hovered_button = None
        
        # Particle system for background
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(1, 3),
                'color': random.choice([CYAN, YELLOW, ORANGE, PURPLE])
            })
        
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
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return "start"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
                
        return None
    
    def update_particles(self):
        """Update background particles"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0

    def draw(self):
        """Draw the enhanced intro screen"""
        self.animation_time += 0.05
        self.update_particles()
        
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(10 * (1 - color_factor))
            g = int(20 * (1 - color_factor))
            b = int(40 * (1 - color_factor))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw animated particles
        for particle in self.particles:
            alpha = int(128 + 127 * abs(math.sin(self.animation_time + particle['x'] * 0.01)))
            color = (*particle['color'][:3], alpha)
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            self.screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Animated title with glow effect
        title_scale = 1.0 + 0.1 * abs(math.sin(self.animation_time))
        title_text = self.font_title.render("TileNova", True, CYAN)
        
        if title_scale != 1.0:
            original_size = title_text.get_size()
            new_size = (int(original_size[0] * title_scale), int(original_size[1] * title_scale))
            title_text = pygame.transform.scale(title_text, new_size)
        
        # Add glow effect
        glow_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        glow_surface.fill((0, 255, 255, 50))
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        glow_rect = glow_surface.get_rect(center=title_rect.center)
        
        # Draw glow
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            self.screen.blit(glow_surface, (glow_rect.x + offset[0], glow_rect.y + offset[1]))
        
        self.screen.blit(title_text, title_rect)
        
        # Animated subtitle
        subtitle_color = (255, 255, int(128 + 127 * abs(math.sin(self.animation_time * 2))))
        subtitle_text = self.font_button.render("Match-3 Puzzle Adventure", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Enhanced buttons with hover effects
        for button_name, button_rect in self.buttons.items():
            is_hovered = self.hovered_button == button_name
            
            # Button shadow
            shadow_rect = button_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
            
            # Button background with gradient
            if is_hovered:
                # Animated hover effect
                hover_intensity = abs(math.sin(self.animation_time * 3))
                button_color = (int(100 + 50 * hover_intensity), int(100 + 50 * hover_intensity), 150)
                border_color = CYAN
            else:
                button_color = DARK_GRAY
                border_color = WHITE
            
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=8)
            
            # Button text with glow on hover
            button_text = button_name.upper()
            text_color = YELLOW if is_hovered else WHITE
            text_surface = self.font_button.render(button_text, True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            
            if is_hovered:
                # Add text glow
                glow_text = self.font_button.render(button_text, True, (255, 255, 0, 100))
                for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    self.screen.blit(glow_text, (text_rect.x + offset[0], text_rect.y + offset[1]))
            
            self.screen.blit(text_surface, text_rect)
        
        # Enhanced instructions with better formatting
        instructions_title = self.font_button.render("HOW TO PLAY", True, ORANGE)
        title_rect = instructions_title.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(instructions_title, title_rect)
        
        # Underline
        underline_rect = pygame.Rect(title_rect.x, title_rect.bottom + 2, title_rect.width, 2)
        pygame.draw.rect(self.screen, ORANGE, underline_rect)
        
        instructions = [
            "• Swipe to move tiles and create matches",
            "• Match 3+ tiles of the same type to score",
            "• Reach target score within move limit",
            "• Use special combos for bonus points"
        ]
        
        y_offset = 510
        for instruction in instructions:
            # Bullet point
            bullet_color = YELLOW
            bullet_text = self.font_small.render("●", True, bullet_color)
            self.screen.blit(bullet_text, (SCREEN_WIDTH // 2 - 150, y_offset))
            
            # Instruction text
            text = self.font_small.render(instruction[2:], True, LIGHT_GRAY)  # Remove bullet from text
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 130, y_offset))
            y_offset += 25
        
        # Controls section
        controls_y = y_offset + 20
        controls_title = self.font_small.render("CONTROLS: ESC-Pause | R-Restart | H-Hint", True, CYAN)
        controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, controls_y))
        self.screen.blit(controls_title, controls_rect)
