from pygame.draw import rect
from pygame.mouse import get_pos, get_pressed
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
        if not get_pressed()[0]:
            self.__dragging = False
            return False
        mouse_pos = get_pos()
        if (self.drag_bar_rect.x < mouse_pos[0] < self.drag_bar_rect.x + self.drag_bar_rect.w and
            self.drag_bar_rect.y < mouse_pos[1] < self.drag_bar_rect.y + self.drag_bar_rect.h):
            if not self.__dragging:
                self.__dragging = True
                self.__offset = (mouse_pos[0] - self.drag_bar_rect.x, mouse_pos[1] - self.drag_bar_rect.y)
            return True
        return False

    @property
    def offset(self):
        return self.__offset
