from pygame.draw import rect
from pygame.mouse import get_pos, get_pressed
class DragBar():
    def __init__(self, screen, x, y, width, height, color=(0, 255, 255)):
        self.screen = screen
        self.drag_bar_rect = ((x, y), (width, height))
        self.__color = color
        self.__dragging = False
        self.__offset = (0, 0)

    @property
    def screen(self):
        return self.__screen
    
    @screen.setter
    def screen(self, screen):
        self.__screen = screen

    def draw(self):
        rect(self.screen, self.__color, self.drag_bar_rect)

    @property
    def pressed(self):
        if not get_pressed()[0]:
            self.__dragging = False
            return False
        mouse_pos = get_pos()
        if (self.drag_bar_rect[0][0] < mouse_pos[0] < self.drag_bar_rect[0][0] + self.drag_bar_rect[1][0] and
            self.drag_bar_rect[0][1] < mouse_pos[1] < self.drag_bar_rect[0][1] + self.drag_bar_rect[1][1]):
            if not self.__dragging:
                self.__dragging = True
                self.__offset = (mouse_pos[0] - self.drag_bar_rect[0][0], mouse_pos[1] - self.drag_bar_rect[0][1])
            return True
        return False

    @property
    def offset(self):
        return self.__offset
