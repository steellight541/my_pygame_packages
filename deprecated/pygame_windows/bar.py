from pygame.draw import rect as pygame_rect
from pygame.mouse import get_pos as mouse_pos, get_pressed as get_mouse_pressed
from pygame.rect import Rect
from pygame import Surface
from pygame.event import Event

class DragBar():
    
    def __init__(self, screen: Surface, x:int, y:int, width:int, height:int, color: tuple[int, int, int] =(0, 255, 255)):
        self.screen = screen
        self.rect = Rect((x, y), (width, height))
        self.__color = color
        self.__dragging = False
        self.__offset = (0, 0)

    def draw(self):
        pygame_rect(self.screen, self.__color, self.rect)

    @property
    def pressed(self):
        mouse_position = mouse_pos()
        if get_mouse_pressed()[0]:
            if (self.rect.collidepoint(mouse_position) or self.__dragging):
                if not self.__dragging: self.__offset = (mouse_position[0] - self.rect.x, mouse_position[1] - self.rect.y)
                self.__dragging = True
                return True
        else: self.__dragging = False
        return False

    @property
    def offset(self):
        return self.__offset
    
    def event_handler(self, event: Event):
        pass
