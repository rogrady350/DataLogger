#Screen Manager for drawing pages
import pygame
from ui.gauges import get_layout_rects, draw_gauge_box

class ScreenManager:
    def __init__(self, screen, data_source):
        self.screen = screen
        self.data_source = data_source

        #font for title - create once and reuse for each frame
        self.title_font = pygame.font.SysFont(
            'Arial', 32, bold=True
        )

    def draw(self):
        #constants
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        readings = self.data_source.get_readings() #get current sensor readings (using test data source for now)
        value, unit, label = readings["oil_temp"]  #example: get oil temp reading for testing

        #fill screen with dark gray
        self.screen.fill((30, 30, 30))

        #render title text
        title_text = self.title_font.render(
            "RaceDash", True, (200, 200, 200)
        )

        #title text top center
        text_rect = title_text.get_rect()
        text_rect.center = (self.screen.get_width() // 2, 30)   

        #draw title text to screen
        self.screen.blit(title_text, text_rect)

        #gauge rects
        gauge_rects = get_layout_rects(screen_width, screen_height, count=1) #test with 1 gauge

        #render gauge
        draw_gauge_box(
            self.screen,
            gauge_rects[0],
            label=label,
            value_text=f"{value:.1f}", #format float to 1 decimal place. may change later to vary based on input selection
            unit=unit
        )