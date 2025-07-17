import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="game_progress.db"):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create levels table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS levels (
                    level_id INTEGER PRIMARY KEY,
                    best_score INTEGER DEFAULT 0,
                    completed BOOLEAN DEFAULT FALSE,
                    stars INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    last_played TIMESTAMP
                )
            ''')
            
            # Create game_stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_stats (
                    id INTEGER PRIMARY KEY,
                    total_score INTEGER DEFAULT 0,
                    total_matches INTEGER DEFAULT 0,
                    total_moves INTEGER DEFAULT 0,
                    play_time INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    last_updated TIMESTAMP
                )
            ''')
            
            # Create settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # Initialize default settings
            default_settings = {
                'music_volume': '0.5',
                'sfx_volume': '0.7',
                'music_enabled': 'True',
                'sfx_enabled': 'True'
            }
            
            for key, value in default_settings.items():
                cursor.execute('''
                    INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
                ''', (key, value))
            
            # Initialize game stats if not exists
            cursor.execute('''
                INSERT OR IGNORE INTO game_stats (id, last_updated) VALUES (1, ?)
            ''', (datetime.now(),))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def save_level_progress(self, level_id, score, completed=False, stars=0):
        """Save progress for a specific level"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get current best score
            cursor.execute('SELECT best_score FROM levels WHERE level_id = ?', (level_id,))
            result = cursor.fetchone()
            
            if result:
                current_best = result[0]
                new_best = max(current_best, score)
                
                cursor.execute('''
                    UPDATE levels SET 
                    best_score = ?, completed = ?, stars = ?, 
                    attempts = attempts + 1, last_played = ?
                    WHERE level_id = ?
                ''', (new_best, completed, stars, datetime.now(), level_id))
            else:
                cursor.execute('''
                    INSERT INTO levels (level_id, best_score, completed, stars, attempts, last_played)
                    VALUES (?, ?, ?, ?, 1, ?)
                ''', (level_id, score, completed, stars, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error saving level progress: {e}")
            return False
    
    def get_level_progress(self, level_id):
        """Get progress for a specific level"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT best_score, completed, stars, attempts, last_played
                FROM levels WHERE level_id = ?
            ''', (level_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'best_score': result[0],
                    'completed': bool(result[1]),
                    'stars': result[2],
                    'attempts': result[3],
                    'last_played': result[4]
                }
            else:
                return {
                    'best_score': 0,
                    'completed': False,
                    'stars': 0,
                    'attempts': 0,
                    'last_played': None
                }
                
        except sqlite3.Error as e:
            print(f"Database error getting level progress: {e}")
            return None
    
    def update_game_stats(self, score_gained=0, matches_made=0, moves_made=0, time_played=0):
        """Update overall game statistics"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE game_stats SET
                total_score = total_score + ?,
                total_matches = total_matches + ?,
                total_moves = total_moves + ?,
                play_time = play_time + ?,
                games_played = games_played + 1,
                last_updated = ?
                WHERE id = 1
            ''', (score_gained, matches_made, moves_made, time_played, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error updating game stats: {e}")
            return False
    
    def get_game_stats(self):
        """Get overall game statistics"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT total_score, total_matches, total_moves, play_time, games_played, last_updated
                FROM game_stats WHERE id = 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'total_score': result[0],
                    'total_matches': result[1],
                    'total_moves': result[2],
                    'play_time': result[3],
                    'games_played': result[4],
                    'last_updated': result[5]
                }
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Database error getting game stats: {e}")
            return None
    
    def save_setting(self, key, value):
        """Save a game setting"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
            ''', (key, str(value)))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error saving setting: {e}")
            return False
    
    def get_setting(self, key, default_value=None):
        """Get a game setting"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                value = result[0]
                # Try to convert to appropriate type
                if value.lower() in ['true', 'false']:
                    return value.lower() == 'true'
                try:
                    return float(value)
                except ValueError:
                    return value
            else:
                return default_value
                
        except sqlite3.Error as e:
            print(f"Database error getting setting: {e}")
            return default_value
    
    def get_all_level_progress(self):
        """Get progress for all levels"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT level_id, best_score, completed, stars, attempts
                FROM levels ORDER BY level_id
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            progress = {}
            for result in results:
                progress[result[0]] = {
                    'best_score': result[1],
                    'completed': bool(result[2]),
                    'stars': result[3],
                    'attempts': result[4]
                }
            
            return progress
            
        except sqlite3.Error as e:
            print(f"Database error getting all level progress: {e}")
            return {}
    
    def reset_progress(self):
        """Reset all game progress"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM levels')
            cursor.execute('''
                UPDATE game_stats SET
                total_score = 0, total_matches = 0, total_moves = 0,
                play_time = 0, games_played = 0, last_updated = ?
                WHERE id = 1
            ''', (datetime.now(),))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error resetting progress: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        # SQLite connections are closed after each operation
        pass
