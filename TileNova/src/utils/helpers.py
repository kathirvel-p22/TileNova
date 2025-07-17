# FILE: src/utils/helpers.py
import pygame

def load_image(path):
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as message:
        print("Cannot load image:", path)
        raise SystemExit(message)