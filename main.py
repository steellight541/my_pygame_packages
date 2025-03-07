import pygame
from pygame_windows.windows import BaseWindow, WindowHandler
p = pygame.init()
# get monitor size
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h-100), vsync=True, flags=pygame.HWACCEL|pygame.DOUBLEBUF|pygame.RESIZABLE)
windows = WindowHandler(
    window_1=BaseWindow(screen, 500, 400, 50, 50),
    window_2=BaseWindow(screen, 500, 400, 100, 100),
    window_3=BaseWindow(screen, 500, 400, 150, 150),
    window_4=BaseWindow(screen, 500, 400, 200, 200),
    window_5=BaseWindow(screen, 500, 400, 250, 250),
    window_6=BaseWindow(screen, 500, 400, 300, 300),
    window_7=BaseWindow(screen, 500, 400, 350, 350),
    
)

clock = pygame.time.Clock()


while True:
    pygame.display.set_caption(f"FPS: {clock.get_fps()}")
    for event in pygame.event.get():
        windows.event_handler(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((255, 255, 255))
    windows.draw()
    pygame.display.flip()
    clock.tick(165)