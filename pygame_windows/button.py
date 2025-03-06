from pygame.font import Font
from pygame.mouse import (
    get_pos as get_mouse_pos, 
    get_pressed as get_mouse_pressed
)
from pygame.draw import rect
from pygame.rect import Rect


class Button():
    def __init__(self, screen, x, y, width, height, text, color=(255, 255, 255), text_color=(0, 0, 0), text_centered=True):
        self.screen = screen
        self.button_rect = Rect((x, y), (width, height))
        self.__text = text
        self.__text_centered = text_centered
        self.__text_color = text_color
        self.__color = color

    def draw(self):
        rect(self.screen, self.__color, self.button_rect)
        text = Font(None, 36).render(self.__text, True, self.__text_color)
        self.screen.blit(
            text, 
            (self.button_rect.x + self.button_rect.w //2 - text.get_width()//2, self.button_rect.y + self.button_rect.h//2 - text.get_height()//2) 
            if self.__text_centered else 
            (self.button_rect.x + 10, self.button_rect.y + 10)
        )

    @property
    def pressed(self): return ((self.button_rect.x <  get_mouse_pos()[0] < self.button_rect.x + self.button_rect.y and self.button_rect.y <  get_mouse_pos()[1] < self.button_rect.y  + self.button_rect.h) and get_mouse_pressed()[0])
