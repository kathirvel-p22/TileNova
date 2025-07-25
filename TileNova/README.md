# TileNova - Enhanced Match-3 Puzzle Game

TileNova is a modern, feature-rich match-3 puzzle game built with Python and Pygame. Experience beautiful curved square fruit tiles, smooth swipe controls, stunning visual effects, and progressively challenging levels.

## 🎮 Features

### Visual Enhancements
- **Curved Square Fruit Tiles**: Beautiful gradient-filled curved square tiles with shadows and highlights
- **Animated UI**: Pulsing buttons, animated progress bars, and dynamic visual feedback
- **Particle Effects**: Explosion effects when tiles are matched
- **Score Popups**: Floating score indicators for immediate feedback
- **Combo Effects**: Special visual effects for combo multipliers
- **Swipe Trails**: Visual feedback for swipe gestures

### Gameplay Features
- **Intuitive Swipe Controls**: Natural swipe-to-move tile mechanics
- **Progressive Difficulty**: 5 challenging levels with increasing complexity
- **Multiple Game Modes**: Score-based, time-based, and obstacle-clearing objectives
- **Combo System**: Multiplier bonuses for consecutive matches
- **Hint System**: Press 'H' for move suggestions
- **Smooth Animations**: Fluid tile movements and falling effects

### Enhanced UI
- **Animated Intro Screen**: Particle background with glowing title effects
- **Modern HUD**: Gradient backgrounds, animated progress bars, and warning indicators
- **Visual Feedback**: Flash effects for invalid moves, glow effects for achievements
- **Responsive Design**: Clean, modern interface with consistent styling

## 🎯 How to Play

1. **Objective**: Match 3 or more tiles of the same type to score points
2. **Controls**: 
   - Swipe tiles to move them in any direction (up, down, left, right)
   - Adjacent tiles will swap positions if the move creates a match
3. **Scoring**: 
   - Basic matches: 10 points per tile
   - Combo multipliers increase with consecutive matches
   - Swipe bonuses: 1.5x multiplier for swipe-initiated matches
4. **Win Condition**: Reach the target score within the move limit

## 🕹️ Controls

| Key/Action | Function |
|------------|----------|
| **Mouse Swipe** | Move tiles |
| **ESC** | Pause game |
| **R** | Restart current level |
| **H** | Show hint |
| **SPACE/ENTER** | Start game (menu) |

## 🏆 Game Modes

### Level 1-2: Basic Scoring
- Reach target score within move limit
- Learn basic matching mechanics

### Level 3: Advanced Scoring
- Higher target scores
- Introduction of special tile effects

### Level 4: Time Challenge
- Score-based with time pressure
- Special rainbow and bomb tiles

### Level 5: Obstacle Course
- Clear obstacles while scoring
- Multiple special tile types
- Strategic gameplay required

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Installation Steps

1. **Clone or download the TileNova project**
2. **Install dependencies**:
   ```bash
   pip install pygame
   ```
3. **Generate fruit images** (first time setup):
   ```bash
   python create_fruit_images.py
   ```
4. **Run the game**:
   ```bash
   python src/main.py
   ```

## 📁 Project Structure

```
TileNova/
├── src/
│   ├── main.py              # Game entry point
│   ├── game.py              # Main game logic
│   ├── board.py             # Game board management
│   ├── tile.py              # Tile class and animations
│   ├── effects.py           # Visual effects system
│   ├── config.py            # Game configuration
│   ├── level_manager.py     # Level loading system
│   ├── database.py          # Progress tracking
│   ├── sound_manager.py     # Audio management
│   ├── animation.py         # Animation utilities
│   └── ui/
│       ├── intro_screen.py  # Main menu
│       ├── hud.py          # Heads-up display
│       └── pause_menu.py   # Pause screen
├── levels/
│   ├── level_1.json        # Level definitions
│   ├── level_2.json
│   ├── level_3.json
│   ├── level_4.json
│   └── level_5.json
├── assets/
│   └── images/
│       └── tiles/          # Generated fruit images
├── create_fruit_images.py  # Image generation script
└── README.md
```

## 🎨 Technical Features

### Advanced Graphics
- **Gradient Backgrounds**: Dynamic color transitions
- **Alpha Blending**: Smooth transparency effects
- **Particle Systems**: Dynamic particle explosions
- **Curved Rectangles**: Modern rounded tile design
- **Real-time Animations**: Smooth 60 FPS gameplay

### Game Architecture
- **Modular Design**: Separated concerns for easy maintenance
- **Event-Driven**: Responsive input handling
- **State Management**: Clean game state transitions
- **Effect System**: Centralized visual effects management
- **Level System**: JSON-based level configuration

### Performance Optimizations
- **Efficient Rendering**: Optimized drawing routines
- **Memory Management**: Proper resource cleanup
- **Smooth Animations**: Interpolated movement systems
- **Responsive Controls**: Low-latency input processing

## 🔧 Customization

### Adding New Levels
Create new JSON files in the `levels/` directory with the following structure:
```json
{
    "level": 6,
    "objective": "score",
    "target_score": 8000,
    "moves": 35,
    "special_tiles": ["rainbow", "bomb", "lightning"],
    "board": [[...], [...], ...]
}
```

### Modifying Visual Effects
Edit `src/effects.py` to customize:
- Particle colors and behaviors
- Animation durations
- Effect intensities
- New effect types

### Adjusting Difficulty
Modify `src/config.py` for:
- Tile colors and types
- Board dimensions
- Animation speeds
- Scoring multipliers

## 🐛 Troubleshooting

### Common Issues
1. **Missing Images**: Run `python create_fruit_images.py` to generate tile images
2. **Pygame Not Found**: Install with `pip install pygame`
3. **Performance Issues**: Reduce particle count in effects.py
4. **Audio Problems**: Check sound_manager.py configuration

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.7+
- **RAM**: 512MB minimum
- **Graphics**: Any modern graphics card
- **Storage**: 50MB free space

## 🎯 Future Enhancements

- **Power-ups**: Special tiles with unique abilities
- **Achievements**: Unlock system with rewards
- **Leaderboards**: High score tracking
- **Sound Effects**: Audio feedback for actions
- **Mobile Support**: Touch-optimized controls
- **Multiplayer**: Competitive and cooperative modes

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Enjoy playing TileNova!** 🎮✨

*Experience the next generation of match-3 puzzle gaming with beautiful visuals, smooth controls, and engaging gameplay.*
#   T i l e N o v a  
 