import pygame
from GUI.main import Button, Tooltip


pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


btn = Button(pygame.Rect(100, 100, 100, 50), text="Hello World", tooltip=Tooltip("Hello World"))


while True:
    pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((255, 255, 255))
    btn.draw(screen)
    pygame.display.flip()
    clock.tick(165)