#holds functions/classes for drawing individual gauges

import pygame

#dynamic font sizing - based on value betweeen minimum and maximum
def _clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

#dynamic gauge box sizing
def _grid_rects(screen_width, screen_height, rows, cols, padding, gap):
    """
    pygame.Rect object: a layout
    x, y: top left corner
    width, height: dimensions in pixels
    """
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

    return rects

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

#renders a single gauge
def draw_gauge_box(screen, rect, label, value_text, unit):
    """
    - screen:     Pygame surface
    - rect:       pygame.Rect defining box position/size
    - label:      string label for value gauge is displaying
    - value_text: string of the value to display
    - unit:       string unit to display next to value
    """
    #colors
    background_color = (40, 40, 40)
    border_color = (100, 100, 100)
    label_color = (180, 180, 255)
    value_color = (0,255, 140)
    unit_color = (200, 200, 200)

    #draw background/border
    pygame.draw.rect(screen, background_color, rect, border_radius=20)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=20)

    #dynamic font sizes based on box size: _clamp(value, minimum, maximum)
    label_size = _clamp(int(rect.height * 0.18), 16, 40)
    value_size = _clamp(int(rect.height * 0.42), 28, 90)
    unit_size  = _clamp(int(rect.height * 0.14), 14, 30)

    label_font = pygame.font.SysFont('Arial', label_size, bold=True)
    value_font = pygame.font.SysFont('Consolas', value_size, bold=True)
    unit_font  = pygame.font.SysFont('Arial', unit_size, bold=False)

    #render text surface (Surface: finished image. True = anti-aliasing: smoother edges)
    label_surface = label_font.render(label, True, label_color)
    value_surface = value_font.render(value_text, True, value_color)
    unit_surface  = unit_font.render(unit, True, unit_color)

    #position text inside the gauge box
    label_rect = label_surface.get_rect(center=(rect.centerx, rect.top + int(rect.height * 0.22)))
    value_rect = value_surface.get_rect(center=(rect.centerx, rect.centery))
    unit_rect  = unit_surface.get_rect(center =(rect.centerx, rect.bottom - int(rect.height * 0.18)))

    #draw text to screen (blit: copy surface to screen)
    screen.blit(label_surface, label_rect)
    screen.blit(value_surface, value_rect)
    screen.blit(unit_surface, unit_rect)