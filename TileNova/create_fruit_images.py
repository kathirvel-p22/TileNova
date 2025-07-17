import pygame
import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from config import TILE_COLORS, FRUIT_IMAGES, TILE_ASSETS

def create_curved_square_fruit_images():
    """Create beautiful curved square fruit images with gradients and shadows"""
    pygame.init()
    
    # Ensure the assets directory exists
    os.makedirs(TILE_ASSETS, exist_ok=True)
    
    # Fruit colors and details
    fruit_details = {
        0: {"name": "apple", "color": (220, 20, 60), "accent": (255, 69, 0)},      # Apple - red with orange accent
        1: {"name": "banana", "color": (255, 255, 0), "accent": (255, 215, 0)},   # Banana - yellow with gold accent
        2: {"name": "cherry", "color": (139, 0, 0), "accent": (255, 20, 147)},    # Cherry - dark red with pink accent
        3: {"name": "grape", "color": (128, 0, 128), "accent": (186, 85, 211)},   # Grape - purple with medium orchid accent
        4: {"name": "orange", "color": (255, 165, 0), "accent": (255, 140, 0)},   # Orange - orange with dark orange accent
        5: {"name": "pear", "color": (154, 205, 50), "accent": (124, 252, 0)},    # Pear - yellow green with lawn green accent
        6: {"name": "strawberry", "color": (255, 20, 147), "accent": (255, 105, 180)} # Strawberry - deep pink with hot pink accent
    }
    
    for tile_type, image_name in FRUIT_IMAGES.items():
        # Create surface with alpha channel
        surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Get fruit details
        fruit = fruit_details.get(tile_type, {"color": TILE_COLORS[tile_type % len(TILE_COLORS)], "accent": (255, 255, 255)})
        base_color = fruit["color"]
        accent_color = fruit["accent"]
        
        # Create gradient effect
        for y in range(64):
            for x in range(64):
                # Calculate distance from center for rounded corners
                center_x, center_y = 32, 32
                corner_radius = 12
                
                # Check if pixel is within rounded rectangle
                if (x < corner_radius and y < corner_radius):
                    # Top-left corner
                    if math.sqrt((x - corner_radius)**2 + (y - corner_radius)**2) > corner_radius:
                        continue
                elif (x >= 64 - corner_radius and y < corner_radius):
                    # Top-right corner
                    if math.sqrt((x - (64 - corner_radius))**2 + (y - corner_radius)**2) > corner_radius:
                        continue
                elif (x < corner_radius and y >= 64 - corner_radius):
                    # Bottom-left corner
                    if math.sqrt((x - corner_radius)**2 + (y - (64 - corner_radius))**2) > corner_radius:
                        continue
                elif (x >= 64 - corner_radius and y >= 64 - corner_radius):
                    # Bottom-right corner
                    if math.sqrt((x - (64 - corner_radius))**2 + (y - (64 - corner_radius))**2) > corner_radius:
                        continue
                
                # Create gradient from top-left to bottom-right
                gradient_factor = (x + y) / 128.0
                
                # Interpolate between base color and accent color
                r = int(base_color[0] * (1 - gradient_factor) + accent_color[0] * gradient_factor)
                g = int(base_color[1] * (1 - gradient_factor) + accent_color[1] * gradient_factor)
                b = int(base_color[2] * (1 - gradient_factor) + accent_color[2] * gradient_factor)
                
                # Add some brightness variation for depth
                brightness_factor = 0.8 + 0.4 * (1 - abs(x - 32) / 32) * (1 - abs(y - 32) / 32)
                r = min(255, int(r * brightness_factor))
                g = min(255, int(g * brightness_factor))
                b = min(255, int(b * brightness_factor))
                
                surface.set_at((x, y), (r, g, b, 255))
        
        # Add subtle shadow effect
        shadow_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, 30)
        
        # Draw shadow (offset by 2 pixels)
        for y in range(2, 64):
            for x in range(2, 64):
                center_x, center_y = 32, 32
                corner_radius = 12
                
                # Check if pixel is within rounded rectangle (same logic as above)
                if (x < corner_radius + 2 and y < corner_radius + 2):
                    if math.sqrt((x - corner_radius - 2)**2 + (y - corner_radius - 2)**2) > corner_radius:
                        continue
                elif (x >= 64 - corner_radius and y < corner_radius + 2):
                    if math.sqrt((x - (64 - corner_radius))**2 + (y - corner_radius - 2)**2) > corner_radius:
                        continue
                elif (x < corner_radius + 2 and y >= 64 - corner_radius):
                    if math.sqrt((x - corner_radius - 2)**2 + (y - (64 - corner_radius))**2) > corner_radius:
                        continue
                elif (x >= 64 - corner_radius and y >= 64 - corner_radius):
                    if math.sqrt((x - (64 - corner_radius))**2 + (y - (64 - corner_radius))**2) > corner_radius:
                        continue
                
                shadow_surface.set_at((x, y), shadow_color)
        
        # Combine shadow and main surface
        final_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        final_surface.blit(shadow_surface, (0, 0))
        final_surface.blit(surface, (0, 0))
        
        # Add highlight effect
        highlight_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        highlight_color = (255, 255, 255, 60)
        
        # Add highlight in top-left area
        for y in range(20):
            for x in range(20):
                if x + y < 25:  # Create diagonal highlight
                    highlight_surface.set_at((x + 8, y + 8), highlight_color)
        
        final_surface.blit(highlight_surface, (0, 0))
        
        # Save the image
        pygame.image.save(final_surface, f"{TILE_ASSETS}{image_name}")
        print(f"Created {image_name} with curved square design")

def create_special_tile_images():
    """Create special power-up tile images"""
    pygame.init()
    
    # Ensure the assets directory exists
    os.makedirs(TILE_ASSETS, exist_ok=True)
    
    # Rocket tile (for 4-tile matches)
    rocket_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Create rocket background with gradient
    for y in range(64):
        for x in range(64):
            # Rounded rectangle check
            corner_radius = 12
            if (x < corner_radius and y < corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y < corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x < corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            
            # Red to orange gradient for rocket
            gradient_factor = y / 64.0
            r = int(255 * (1 - gradient_factor * 0.3))
            g = int(100 * gradient_factor)
            b = 0
            rocket_surface.set_at((x, y), (r, g, b, 255))
    
    # Add rocket shape
    pygame.draw.polygon(rocket_surface, (255, 255, 0), [(32, 10), (25, 35), (39, 35)])  # Tip
    pygame.draw.rect(rocket_surface, (200, 200, 200), (28, 35, 8, 20))  # Body
    pygame.draw.polygon(rocket_surface, (255, 100, 0), [(20, 55), (32, 45), (44, 55)])  # Flames
    
    pygame.image.save(rocket_surface, f"{TILE_ASSETS}rocket.png")
    print("Created rocket.png")
    
    # Lightning tile (for 5-tile matches)
    lightning_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Create lightning background with gradient
    for y in range(64):
        for x in range(64):
            # Rounded rectangle check (same as above)
            corner_radius = 12
            if (x < corner_radius and y < corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y < corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x < corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            
            # Purple to blue gradient for lightning
            gradient_factor = (x + y) / 128.0
            r = int(128 * (1 - gradient_factor))
            g = int(50 * gradient_factor)
            b = int(255 * (0.7 + 0.3 * gradient_factor))
            lightning_surface.set_at((x, y), (r, g, b, 255))
    
    # Add lightning bolt shape
    lightning_points = [(35, 8), (25, 30), (30, 30), (20, 56), (30, 35), (25, 35)]
    pygame.draw.polygon(lightning_surface, (255, 255, 255), lightning_points)
    pygame.draw.polygon(lightning_surface, (255, 255, 0), lightning_points, 2)
    
    pygame.image.save(lightning_surface, f"{TILE_ASSETS}lightning.png")
    print("Created lightning.png")
    
    # Bomb tile (for L/T shaped matches)
    bomb_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Create bomb background with gradient
    for y in range(64):
        for x in range(64):
            # Rounded rectangle check (same as above)
            corner_radius = 12
            if (x < corner_radius and y < corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y < corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - corner_radius)**2) > corner_radius:
                    continue
            elif (x < corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - corner_radius)**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            elif (x >= 64 - corner_radius and y >= 64 - corner_radius):
                if math.sqrt((x - (64 - corner_radius))**2 + (y - (64 - corner_radius))**2) > corner_radius:
                    continue
            
            # Dark gradient for bomb
            gradient_factor = (x + y) / 128.0
            r = int(50 * (1 - gradient_factor * 0.5))
            g = int(50 * (1 - gradient_factor * 0.5))
            b = int(50 * (1 - gradient_factor * 0.5))
            bomb_surface.set_at((x, y), (r, g, b, 255))
    
    # Add bomb shape
    pygame.draw.circle(bomb_surface, (40, 40, 40), (32, 40), 18)  # Main body
    pygame.draw.circle(bomb_surface, (60, 60, 60), (32, 40), 18, 2)  # Outline
    pygame.draw.line(bomb_surface, (139, 69, 19), (32, 22), (28, 15), 3)  # Fuse
    pygame.draw.circle(bomb_surface, (255, 100, 0), (26, 13), 3)  # Spark
    
    pygame.image.save(bomb_surface, f"{TILE_ASSETS}bomb.png")
    print("Created bomb.png")

if __name__ == "__main__":
    create_curved_square_fruit_images()
    create_special_tile_images()
    print("All curved square fruit images and special tiles created successfully!")
