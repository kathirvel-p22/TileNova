# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 64
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
ANIMATION_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Tile colors for different types
TILE_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN]

# Fruit images for different tile types
FRUIT_IMAGES = {
    0: "apple.png",
    1: "banana.png",
    2: "cherry.png",
    3: "grape.png",
    4: "orange.png",
    5: "pear.png",
    6: "strawberry.png"
}

# Special tile types
SPECIAL_TILE_ROCKET = 100  # Rocket bomb - clears row/column
SPECIAL_TILE_LIGHTNING = 101  # Lightning - clears all tiles of same color
SPECIAL_TILE_BOMB = 102  # Bomb - clears 3x3 area

SPECIAL_TILES = {
    SPECIAL_TILE_ROCKET: "rocket.png",
    SPECIAL_TILE_LIGHTNING: "lightning.png", 
    SPECIAL_TILE_BOMB: "bomb.png"
}

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"

# Asset paths
TILE_ASSETS = "assets/images/tiles/"
AUDIO_BG = "assets/audio/bg_music.mp3"
AUDIO_MATCH = "assets/audio/match_sfx.wav"

# Board settings
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 100

# UI settings
FONT_SIZE = 24
TITLE_FONT_SIZE = 48
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
