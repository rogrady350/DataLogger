#holds functions/classes for drawing individual gauges

import pygame

#dynamic font sizing
def _clamp(value, min, max):
    return max(min, min(value, max))

#dynamic box sizing
def _grid_rects(screen_width, screen_height, rows, cols, padding, gap):
    cell_width = (
        screen_width - (2 * padding) - (gap * (cols - 1)                                 )
    ) // cols

    cell_height = (
        screen_height - (2 * padding) - (gap * (rows - 1))
    ) // rows

    rects = []

    for row in range(rows):
        for col in range(cols):
            x = padding + col * (cell_width + gap)
            y = padding + row * (cell_height + gap)
            rects.append(pygame.Rect(x, y, cell_width, cell_height))

#layouts for 1, 2, 4 gauge boxes
def get_layout_rects(screen_width, screen_height, count):
    padding = 20
    gap = 20

    if count == 1:
        return _grid_rects(screen_width, screen_height, rows=1, cols=1, padding=padding, gap=gap)
    
    elif count == 2:
        return _grid_rects(screen_width, screen_height, rows=1, cols=2, padding=padding, gap=gap)
    
    elif count == 4:
        return _grid_rects(screen_width, screen_height, rows=2, cols=2, padding=padding, gap=gap)
    
    else:
        raise ValueError("Unsupported gauge count for layout. Must be 1, 2, or 4.")

def draw_gauge_box(screen, rect, label, value, unit):
    """
    Draw a value box with 
    - label (top)
    - value (center)
    - unit (bottom)
    """

    #colors
    background_color = (40, 40, 40)
    border_color = (100, 100, 100)
    label_color = (180, 180, 255)
    value_color = (0, 255, 140)

    #draw box background
    pygame.draw.rect(screen, background_color, rect, border_radius=20)

    #draw box border
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=20)

    #fonts
    label_font = pygame.font.SysFont('Arial', 28, bold=True)
    value_font = pygame.font.SysFont('Consolas', 48, bold=True)
