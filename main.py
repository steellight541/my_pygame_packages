import pygame
from pygame_windows.main import BaseWindow, WindowHandler
pygame.init()
screen = pygame.display.set_mode((800, 600))
windows = WindowHandler(
    window_1=BaseWindow(screen, 500, 400, 50, 50),
    window_2=BaseWindow(screen, 500, 400, 100, 100)
)



while True:
    for event in pygame.event.get():
        windows.event_handler(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    screen.fill((255, 255, 255))
    windows.draw()
    pygame.display.update()