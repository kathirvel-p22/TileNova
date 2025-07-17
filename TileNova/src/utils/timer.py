# FILE: src/utils/timer.py
import pygame

class Timer:
    def __init__(self, duration, start_active=False, callback=None):
        self.duration = duration
        self.active = start_active
        self.start_time = 0
        self.callback = callback

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()
                if self.callback:
                    self.callback()
