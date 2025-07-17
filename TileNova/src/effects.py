import pygame
import math
import random
from config import *

class Effect:
    """Base class for visual effects"""
    def __init__(self, duration):
        self.duration = duration
        self.timer = 0
        self.active = True
    
    def update(self, dt):
        """Update the effect"""
        self.timer += dt
        if self.timer >= self.duration:
            self.active = False
    
    def draw(self, screen):
        """Draw the effect"""
        pass

class SwipeTrail(Effect):
    """Visual trail effect for swipe gestures"""
    def __init__(self, start_pos, end_pos, duration=0.3):
        super().__init__(duration)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = (255, 255, 255, 180)
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Calculate alpha based on remaining time
        alpha = int(255 * (1 - self.timer / self.duration))
        color = (*self.color[:3], alpha)
        
        # Create surface for trail
        trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw trail line with varying thickness
        thickness = max(1, int(8 * (1 - self.timer / self.duration)))
        pygame.draw.line(trail_surface, color, self.start_pos, self.end_pos, thickness)
        
        # Add glow effect
        glow_color = (*self.color[:3], alpha // 3)
        pygame.draw.line(trail_surface, glow_color, self.start_pos, self.end_pos, thickness + 4)
        
        screen.blit(trail_surface, (0, 0))

class FlashEffect(Effect):
    """Flash effect for tiles"""
    def __init__(self, tile, color, duration=0.5):
        super().__init__(duration)
        self.tile = tile
        self.color = color
        self.original_image = tile.image.copy()
    
    def update(self, dt):
        super().update(dt)
        if self.active:
            # Create pulsing effect
            pulse = abs(math.sin(self.timer * 10))
            alpha = int(128 * pulse)
            
            # Apply flash overlay
            flash_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            flash_surface.fill((*self.color, alpha))
            
            self.tile.image = self.original_image.copy()
            self.tile.image.blit(flash_surface, (0, 0))
        else:
            # Restore original appearance
            self.tile.image = self.original_image.copy()

class ParticleEffect(Effect):
    """Particle explosion effect"""
    def __init__(self, position, color, particle_count=20, duration=1.0):
        super().__init__(duration)
        self.position = position
        self.particles = []
        
        # Create particles
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            size = random.uniform(2, 6)
            life = random.uniform(0.5, 1.0)
            
            particle = {
                'x': position[0],
                'y': position[1],
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'life': life,
                'max_life': life,
                'color': color
            }
            self.particles.append(particle)
    
    def update(self, dt):
        super().update(dt)
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 200 * dt  # Gravity
            particle['life'] -= dt
    
    def draw(self, screen):
        if not self.active:
            return
        
        for particle in self.particles:
            if particle['life'] > 0:
                # Calculate alpha based on remaining life
                alpha = int(255 * (particle['life'] / particle['max_life']))
                color = (*particle['color'], alpha)
                
                # Draw particle
                pos = (int(particle['x']), int(particle['y']))
                size = max(1, int(particle['size'] * (particle['life'] / particle['max_life'])))
                
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size, size), size)
                screen.blit(particle_surface, (pos[0] - size, pos[1] - size))

class ScorePopup(Effect):
    """Floating score popup effect"""
    def __init__(self, position, score, duration=1.5):
        super().__init__(duration)
        self.start_pos = position
        self.score = score
        self.font = pygame.font.Font(None, 32)
        self.color = YELLOW if score >= 100 else WHITE
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Calculate position (float upward)
        progress = self.timer / self.duration
        y_offset = -50 * progress
        alpha = int(255 * (1 - progress))
        
        # Render text
        text = self.font.render(f"+{self.score}", True, self.color)
        text.set_alpha(alpha)
        
        pos = (self.start_pos[0], self.start_pos[1] + y_offset)
        text_rect = text.get_rect(center=pos)
        screen.blit(text, text_rect)

class ComboEffect(Effect):
    """Combo multiplier effect"""
    def __init__(self, position, combo, duration=2.0):
        super().__init__(duration)
        self.position = position
        self.combo = combo
        self.font = pygame.font.Font(None, 48)
        self.color = ORANGE
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Pulsing scale effect
        scale = 1.0 + 0.3 * abs(math.sin(self.timer * 5))
        alpha = int(255 * (1 - self.timer / self.duration))
        
        # Render combo text
        text = self.font.render(f"COMBO x{self.combo}!", True, self.color)
        text.set_alpha(alpha)
        
        # Scale the text
        if scale != 1.0:
            original_size = text.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            text = pygame.transform.scale(text, new_size)
        
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)

class Effects:
    """Manager for all visual effects"""
    def __init__(self):
        self.effects = []
        self.clock = pygame.time.Clock()
    
    def add_swipe_trail(self, start_pos, end_pos):
        """Add a swipe trail effect"""
        effect = SwipeTrail(start_pos, end_pos)
        self.effects.append(effect)
    
    def add_flash_effect(self, tile, color):
        """Add a flash effect to a tile"""
        effect = FlashEffect(tile, color)
        self.effects.append(effect)
    
    def add_particle_explosion(self, position, color, particle_count=20):
        """Add a particle explosion effect"""
        effect = ParticleEffect(position, color, particle_count)
        self.effects.append(effect)
    
    def add_score_popup(self, position, score):
        """Add a floating score popup"""
        effect = ScorePopup(position, score)
        self.effects.append(effect)
    
    def add_combo_effect(self, position, combo):
        """Add a combo multiplier effect"""
        effect = ComboEffect(position, combo)
        self.effects.append(effect)
    
    def update(self):
        """Update all effects"""
        dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Update effects and remove inactive ones
        self.effects = [effect for effect in self.effects if effect.active]
        
        for effect in self.effects:
            effect.update(dt)
    
    def draw(self, screen):
        """Draw all effects"""
        for effect in self.effects:
            effect.draw(screen)
    
    def clear_all(self):
        """Clear all effects"""
        self.effects.clear()

    def play_match_sound(self):
        """Placeholder for match sound"""
        pass

    def explosion(self, position):
        """Create explosion effect at position"""
        self.add_particle_explosion(position, RED)
