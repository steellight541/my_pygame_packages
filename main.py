import pygame
from GUI.handler import GUIHandler
from GUI.button import *

pygame.init()
i = 0
window = pygame.display.set_mode((800, 600))
def on_double_click(button: Button):
    print("Double clicked")
handler = GUIHandler()
btn = handler.add_button(Button.from_surface(pygame.Surface((100,100)), (100, 100)))
handler.button_connect(btn, on_double_click, click_type=ClickType.DOUBLE)
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handler.handle_events(event)
    window.fill((255, 255, 255))
    handler.draw(window)
    pygame.display.flip()