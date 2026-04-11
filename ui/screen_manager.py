#Screen Manager for drawing pages
import pygame
from ui.gauges import get_layout_rects, draw_gauge_box
import json
import os

class ScreenManager:
    def __init__(self, screen, data_source):
        #main screen config
        self.header_height = 40 #constant for header height
        self.screen = screen
        self.data_source = data_source
        self.settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
        self.gauge_count = 1 #number of gaugess displayed. default=1 gauge if no saved settings

        #holds sensor assignments - default config
        self.selected_sensors = [
            "nitrous_psi",
            "trans_in",
            "trans_out",
            "fuel_psi"
        ]

        #list of sensors to select from the sensor picker
        """
        Default list. Always contains values for max gauge count.
        draw() will only render first 'gauge_count' sensors from user selection.
        """
        self.available_sensors = [
            "nitrous_psi",
            "trans_in",
            "trans_out",
            "fuel_psi"
        ]

        #sensor selection config
        self.show_sensor_picker = False #bool - show/hide sensor picker selector True=open, False=close
        self.active_gauge_index = None  #int - holds index of gauge being configured. None if no active selection

        self._load_settings()

        #fonts
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.btn_font = pygame.font.SysFont('Arial', 22, bold=True)

        #header buttons for number of gauges displayed (x, y, width, height) - may need to adjust
        self.btn1 = pygame.Rect(20, 8, 60, 34)
        self.btn2 = pygame.Rect(90, 8, 60, 34)
        self.btn4 = pygame.Rect(160, 8, 60, 34)

    #master tap handling
    def on_tap(self, pos):
        if self.show_sensor_picker:
            self._handle_sensor_selection(pos)
        else:
            self._handle_dash_tap(pos)
        #save is within helpers

    #==Rendering==
    def draw(self):
        readings = self.data_source.get_readings() #get current sensor readings (using test data source for now)
        self.screen.fill((30, 30, 30))             #fill screen with dark gray

        #render title text
        title_text = self.title_font.render("RaceDash", True, (200, 200, 200))

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

        sensor_keys = self.selected_sensors   #render sensor config from screen_manager settings
        gauge_rects = self._get_gauge_rects() #load gauge geometry via helper function

        #render gauges - render first so gauges appear behind sensor picker if open
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

        #render gauge picker if active - render second so it appears on top of gauges when openn
        if self.show_sensor_picker:
            self._draw_sensor_picker(readings)

    #helper for rendering sensor picker
    def _draw_sensor_picker(self, readings):
        picker_rects = self._get_sensor_picker_rects()

        for rect, sensor in zip(picker_rects, self.available_sensors):
            label = readings[sensor][2] #label is index 2 in readings tuple (value, unit, label)

            pygame.draw.rect(self.screen, (60, 60, 60), rect, border_radius=10)
            pygame.draw.rect(self.screen, (180, 180, 180), rect, 2, border_radius=10)

            text = self.btn_font.render(label, True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))

    #===HELPERS===
    #=Geometry Helpers=
    #gauge geometry
    def _get_gauge_rects(self):
        #get screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        #build gauge layout
        gauge_rects = get_layout_rects(
            screen_width, 
            screen_height - self.header_height,
            count=self.gauge_count
        )

        #move gauges below header
        for rect in gauge_rects:
            rect.top += self.header_height
        return gauge_rects
    
    #sensor picker geometry
    def _get_sensor_picker_rects(self):
        box_width = 260
        box_height = 50
        gap = 12

        total_height = len(self.available_sensors) * box_height + (len(self.available_sensors) - 1) * gap
        start_x = (self.screen.get_width() - box_width) // 2
        start_y = (self.screen.get_height() - total_height) // 2

        rects = []
        for i in range(len(self.available_sensors)):
            y = start_y + i * (box_height + gap)
            rects.append(pygame.Rect(start_x, y, box_width, box_height))

        return rects
        
    #=Tap Handling Helpers=
    #dash taps - either change num of gauges displayed or show sensor picker
    def _handle_dash_tap(self, pos):
        #select number of gauges displayed
        if self.btn1.collidepoint(pos):
            self.gauge_count = 1
            self._save_settings()
        elif self.btn2.collidepoint(pos):
            self.gauge_count = 2
            self._save_settings()
        elif self.btn4.collidepoint(pos):
            self.gauge_count = 4
            self._save_settings()

        #gauge sensor selection
        else:
            gauge_rects = self._get_gauge_rects() #load gauge geometry via helper function

            #show sensor picker on tap
            for i, rect in enumerate(gauge_rects):
                if rect.collidepoint(pos):
                    self.active_gauge_index = i
                    self.show_sensor_picker = True
                    break

    #sensor selection
    def _handle_sensor_selection(self, pos):
        picker_rects = self._get_sensor_picker_rects()

        for i, rect in enumerate(picker_rects):
            #tap within sensor picker to select sensor
            if rect.collidepoint(pos):
                chosen_sensor = self.available_sensors[i]
                self.selected_sensors[self.active_gauge_index] = chosen_sensor
                self.show_sensor_picker = False
                self.active_gauge_index = None
                self._save_settings()
                return
            
        #tap outside picker to exit without changes
        self.show_sensor_picker = False
        self.active_gauge_index = None

    #=Load/Save Helpers=
    def _load_settings(self):
        try:
            with open(self.settings_path, 'r') as f:
                data = json.load(f)
            self.gauge_count = int(data.get('gauge_count', self.gauge_count))
            
            load_sensors = data.get('selected_sensors', self.selected_sensors)

            #safety: only load sensor config if it matches the max available gauge slots
            if isinstance(load_sensors, list) and len(load_sensors) == len(self.selected_sensors):
                self.selected_sensors = load_sensors
            else:
                print("Invalid sensor config in settings. Using defaults.")

        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
            pass #first run or no settings file
        except Exception as e:
            print(f"Error loading settings: {e}")
            pass #file corrupt, use defaults

    def _save_settings(self):
        data = {
            'gauge_count': self.gauge_count,
            'selected_sensors': self.selected_sensors
        }
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving settings: {e}")