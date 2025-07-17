import json
import os
from config import *

class LevelManager:
    def __init__(self):
        self.levels_dir = "levels"
        self.current_level = 1
        self.levels_cache = {}
        
    def load_level(self, level_num):
        """Load level data from JSON file"""
        if level_num in self.levels_cache:
            return self.levels_cache[level_num]
            
        level_file = os.path.join(self.levels_dir, f"level_{level_num}.json")
        
        try:
            with open(level_file, 'r') as f:
                level_data = json.load(f)
                self.levels_cache[level_num] = level_data
                return level_data
        except FileNotFoundError:
            # Return default level data if file not found
            default_level = {
                "level": level_num,
                "objective": "score",
                "target_score": 3000 + (level_num - 1) * 1000,
                "moves": max(15, 25 - level_num),
                "board": None
            }
            return default_level
        except json.JSONDecodeError:
            print(f"Error parsing level file: {level_file}")
            return None
    
    def has_level(self, level_num):
        """Check if a level exists"""
        level_file = os.path.join(self.levels_dir, f"level_{level_num}.json")
        return os.path.exists(level_file) or level_num <= 10  # Support up to 10 levels
    
    def get_level_count(self):
        """Get the total number of available levels"""
        count = 0
        level_num = 1
        while self.has_level(level_num):
            count += 1
            level_num += 1
        return count
    
    def create_level_file(self, level_num, target_score, moves, objective="score"):
        """Create a new level file"""
        level_data = {
            "level": level_num,
            "objective": objective,
            "target_score": target_score,
            "moves": moves,
            "board": None  # Let the game generate random board
        }
        
        level_file = os.path.join(self.levels_dir, f"level_{level_num}.json")
        
        try:
            with open(level_file, 'w') as f:
                json.dump(level_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error creating level file: {e}")
            return False
    
    def get_level_progress(self, level_num):
        """Get progress information for a level"""
        # This would typically load from a save file or database
        # For now, return default values
        return {
            "completed": False,
            "best_score": 0,
            "stars": 0
        }
    
    def save_level_progress(self, level_num, score, completed=False):
        """Save progress for a level"""
        # This would typically save to a file or database
        # For now, just print the information
        print(f"Level {level_num} progress: Score={score}, Completed={completed}")
    
    def get_next_level(self):
        """Get the next level number"""
        return self.current_level + 1 if self.has_level(self.current_level + 1) else None
    
    def set_current_level(self, level_num):
        """Set the current level"""
        if self.has_level(level_num):
            self.current_level = level_num
            return True
        return False
