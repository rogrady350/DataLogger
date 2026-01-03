#Screen Manager for drawing pages
import pygame
from ui.gauges import get_layout_rects, draw_gauge_box
import json
import os

class ScreenManager:
    def __init__(self, screen, data_source):
        self.screen = screen
        self.data_source = data_source
        self.settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
        self.gauge_count = 1 #default 1 gauge if no saved settings

        self._load_settings()

        #fonts
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.btn_font = pygame.font.SysFont('Arial', 22, bold=True)

        #header buttons for number of gauges displayed (x, y, width, height) - may need to adjust
        self.btn1 = pygame.Rect(20, 8, 60, 34)
        self.btn2 = pygame.Rect(90, 8, 60, 34)
        self.btn4 = pygame.Rect(160, 8, 60, 34)

    def on_tap(self, pos):
        if self.btn1.collidepoint(pos):
            self.gauge_count = 1
        elif self.btn2.collidepoint(pos):
            self.gauge_count = 2
        elif self.btn4.collidepoint(pos):
            self.gauge_count = 4

        self._save_settings()

    def draw(self):
        #constants
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        HEADER_HEIGHT = 40

        readings = self.data_source.get_readings() #get current sensor readings (using test data source for now)

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

        #helper for drawing header buttons
        def _draw_btn(rect, text, active):
            bg = (70, 70, 70) if not active else (110, 110, 110)
            border = (140, 140, 140)
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, border, rect, width=2, border_radius=8)

            surface = self.btn_font.render(text, True, (220, 220, 220))
            self.screen.blit(surface, surface.get_rect(center=rect.center))

        _draw_btn(self.btn1, "1", self.gauge_count == 1)
        _draw_btn(self.btn2, "2", self.gauge_count == 2)
        _draw_btn(self.btn4, "4", self.gauge_count == 4)

        sensor_keys = ["oil_temp", "trans_out", "trans_post", "fuel_psi"] #simple default order for now

        #gauge rects
        gauge_rects = get_layout_rects(
            screen_width, 
            screen_height - HEADER_HEIGHT, 
            count=self.gauge_count
        )
        
        #shift gagues below header
        for rect in gauge_rects:
            rect.top += HEADER_HEIGHT

        #render gauges
        """
        rect: current gauge being drawn for key: sensor assigned to that gauge box
        gauge_rects: list of all gauge boxes
        """
        for rect, key in zip(gauge_rects, sensor_keys):
            value, unit, label = readings[key]
            draw_gauge_box(
                self.screen,
                rect,
                label=label,
                value_text=f"{value:.1f}", #format float to 1 decimal place. may change later to vary based on input selection
                unit=unit
            )

    #load/save settings helpers
    def _load_settings(self):
        try:
            with open(self.settings_path, 'r') as f:
                data = json.load(f)
            self.gauge_count = int(data.get('gauge_count', self))
            #self.selected_sensors = data.get('selected_sensors', self.selected_sensors)

        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
            pass #first run or no settings file
        except Exception as e:
            print(f"Error loading settings: {e}")
            pass #file corrupt, use defaults

    def _save_settings(self):
        data = {
            'gauge_count': self.gauge_count,
            #'selected_sensors': self.selected_sensors
        }
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving settings: {e}")