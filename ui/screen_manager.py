#Screen Manager for drawing pages
import pygame

class ScreenManager:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        #fill screen with dark gray
        self.screen.fill((30, 30, 30))