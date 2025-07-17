import pygame
import os
import numpy
from config import *

class SoundManager:
    def __init__(self):
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.music_enabled = True
        self.sfx_enabled = True
        
        # Load sounds
        self.load_sounds()
        
    def load_sounds(self):
        """Load all sound effects"""
        # Create placeholder sounds if audio files don't exist
        try:
            # Background music
            if os.path.exists(AUDIO_BG):
                pygame.mixer.music.load(AUDIO_BG)
            
            # Match sound effect
            if os.path.exists(AUDIO_MATCH):
                self.sounds['match'] = pygame.mixer.Sound(AUDIO_MATCH)
            else:
                # Create a simple beep sound as placeholder
                self.sounds['match'] = self.create_beep_sound(440, 0.1)
                
            # Additional sound effects (created programmatically)
            self.sounds['swap'] = self.create_beep_sound(220, 0.05)
            self.sounds['invalid'] = self.create_beep_sound(150, 0.2)
            self.sounds['level_complete'] = self.create_melody([440, 554, 659, 880], 0.3)
            self.sounds['game_over'] = self.create_melody([220, 196, 175, 147], 0.5)
            
        except pygame.error as e:
            print(f"Error loading sounds: {e}")
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 4096 * (0.5 * (1 + (time * frequency * 2 * 3.14159) % (2 * 3.14159) / 3.14159 - 1))
            # Adapt to the mixer's 8-channel requirement
            arr.append([int(wave)] * 8)
        
        sound = pygame.sndarray.make_sound(numpy.array(arr, dtype=numpy.int16))
        return sound
    
    def create_melody(self, frequencies, note_duration):
        """Create a simple melody from frequencies"""
        sample_rate = 22050
        total_duration = len(frequencies) * note_duration
        frames = int(total_duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            note_index = int(time / note_duration)
            if note_index < len(frequencies):
                frequency = frequencies[note_index]
                wave = 2048 * (0.5 * (1 + (time * frequency * 2 * 3.14159) % (2 * 3.14159) / 3.14159 - 1))
            else:
                wave = 0
            # Adapt to the mixer's 8-channel requirement
            arr.append([int(wave)] * 8)
        
        sound = pygame.sndarray.make_sound(numpy.array(arr, dtype=numpy.int16))
        return sound
    
    def play_bg_music(self):
        """Play background music"""
        if self.music_enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            except pygame.error:
                pass  # No music file available
    
    def stop_bg_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
    
    def play_match_sound(self):
        """Play match sound effect"""
        if self.sfx_enabled and 'match' in self.sounds:
            self.sounds['match'].set_volume(self.sfx_volume)
            self.sounds['match'].play()
    
    def play_swap_sound(self):
        """Play tile swap sound effect"""
        if self.sfx_enabled and 'swap' in self.sounds:
            self.sounds['swap'].set_volume(self.sfx_volume * 0.5)
            self.sounds['swap'].play()
    
    def play_invalid_sound(self):
        """Play invalid move sound effect"""
        if self.sfx_enabled and 'invalid' in self.sounds:
            self.sounds['invalid'].set_volume(self.sfx_volume * 0.3)
            self.sounds['invalid'].play()
    
    def play_level_complete_sound(self):
        """Play level complete sound effect"""
        if self.sfx_enabled and 'level_complete' in self.sounds:
            self.sounds['level_complete'].set_volume(self.sfx_volume)
            self.sounds['level_complete'].play()
    
    def play_game_over_sound(self):
        """Play game over sound effect"""
        if self.sfx_enabled and 'game_over' in self.sounds:
            self.sounds['game_over'].set_volume(self.sfx_volume)
            self.sounds['game_over'].play()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_bg_music()
        else:
            self.stop_bg_music()
    
    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        self.sfx_enabled = not self.sfx_enabled
    
    def cleanup(self):
        """Clean up sound resources"""
        pygame.mixer.quit()
