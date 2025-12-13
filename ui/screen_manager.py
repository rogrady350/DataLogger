#Screen Manager for drawing pages
import pygame

class ScreenManager:
    def __init__(self, screen):
        self.screen = screen

        #font for title - create once and reuse for each frame
        self.title_font = pygame.font.SysFont(
            'Arial', 32, bold=True
        )

    def draw(self):
        #fill screen with dark gray
        self.screen.fill((30, 30, 30))

        #render title text
        title_text = self.title_font.render(
            "RaceDash", True, (200, 200, 200)
        )

        #title text top center
        text_rect = title_text.get_rect()
        text_rect.center = (self.screen.get_width() // 2, 30)   

        #draw text to screen
        self.screen.blit(title_text, text_rect)