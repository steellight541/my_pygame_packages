import pygame
from GUI.handler import GUIHandler
from GUI.button import *

pygame.init()
window = pygame.display.set_mode((800, 600))

handler = GUIHandler()
btn = handler.add_button(Button.from_surface(pygame.Surface((100,100)), (100, 100)))
running = True

@handler.connect(btn, ClickType.DOUBLE)
def on_click(btn: Button):
    print("Button clicked")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handler.handle_events(event)
    window.fill((255, 255, 255))
    handler.draw(window)
    pygame.display.flip()