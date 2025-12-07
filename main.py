#Entry point for RaceDash app. Sets up Pygame, creates screen, runs main loop
import pygame
import sys

from ui.screen_manager import ScreenManager

#screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

def main():
    pygame.init()
    pygame.display.set_caption("RaceDash")

    #create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    screen_manager = ScreenManager(screen) #handle all drawing

    running = True

    while running:
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    #drawing
    screen_manager.draw()
    pygame.display.flip()
    clock.tick(30)        #limit to 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()