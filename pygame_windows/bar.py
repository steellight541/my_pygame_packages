from pygame.draw import rect
from pygame.mouse import (
    get_pos as mouse_pos, 
    get_pressed as get_mouse_pressed
)
from pygame.rect import Rect

class DragBar():
    def __init__(self, screen, x, y, width, height, color=(0, 255, 255)):
        self.screen = screen
        self.drag_bar_rect = Rect((x, y), (width, height))
        self.__color = color
        self.__dragging = False
        self.__offset = (0, 0)

    def draw(self):
        rect(self.screen, self.__color, self.drag_bar_rect)

    @property
    def pressed(self):
        if get_mouse_pressed()[0]:
            if self.drag_bar_rect.collidepoint(mouse_pos()):
                self.__offset = (mouse_pos()[0] - self.drag_bar_rect.x, mouse_pos()[1] - self.drag_bar_rect.y) if not self.__dragging else self.__offset
                self.__dragging =  self.__dragging or True
                return True
        else: self.__dragging = False
        return False

    @property
    def offset(self):
        return self.__offset
