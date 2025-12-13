#Entry point for RaceDash app. Sets up Pygame, creates screen, runs main loop
import pygame
import sys

from ui.screen_manager import ScreenManager
from data.test_data_source import TestDataSource

#screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

#initialize Pygame
def main():
    pygame.init()

    data_source = TestDataSource()  #simulated test data source for now

    #create window
    pygame.display.set_caption("RaceDash")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()            #initialize clock for fps control
    screen_manager = ScreenManager(screen, data_source) #handle all drawing

    #main loop
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
        screen_manager.draw() #delegate draw to UI system
        pygame.display.flip() #updates window
        clock.tick(30)        #limit to 30 FPS

    #cleanup - safely exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()