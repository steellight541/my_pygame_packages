import pygame
from pygame_windows.main import BaseWindow
pygame.init()
screen = pygame.display.set_mode((800, 600))
windows = [BaseWindow(screen)]



while True:
    [windows.remove(window) for window in windows if not window.active]
    for event in pygame.event.get():
        [window.event_handler(event) for window in windows]
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    screen.fill((255, 255, 255))
    [window.draw() for window in windows]
    pygame.display.update()