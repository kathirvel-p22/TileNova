# FILE: src/animation.py
import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, images, duration, loop=False):
        super().__init__()
        self.images = images
        self.duration = duration
        self.loop = loop
        self.current_time = 0
        self.frame_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.playing = True

    def update(self, dt):
        if not self.playing:
            return

        self.current_time += dt
        if self.current_time >= self.duration / len(self.images):
            self.current_time = 0
            self.frame_index += 1

            if self.frame_index >= len(self.images):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.playing = False
                    self.kill()
                    return

            self.image = self.images[self.frame_index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def set_position(self, position):
        self.rect.center = position
