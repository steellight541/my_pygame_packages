# pygame imports
from pygame.draw import ( rect as pygame_rect )
from pygame.mouse import get_pos
from pygame.rect import ( Rect as pygame_Rect )
from pygame.display import get_surface



# local imports
from .button import Button, ButtonHandler
from .bar import DragBar
from .demos import Bouncingball


class BaseWindow:
    def __init__(self, screen, width=500, height=400, x=50, y=50):
        self.getting_dragged = False
        self.last_dragged = False
        self.screen = screen
        self.__window_frame_rect = pygame_Rect((x, y), (width, height))
        self.__content_area_rect = pygame_Rect((x+1, y+30), (width-2, height-31))  # Adjusted for draggable bar height
        self.__active = True
        self.__buttons = ButtonHandler(
            close=Button.close_button(screen, x + width - 30, y, 30, 30),
            minimize=Button.minimize_button(screen, x + width - 60, y, 30, 30),
            maximize=Button.maximize_button(screen, x + width - 90, y, 30, 30)
        )
        self.__drag_bar = DragBar(screen, x, y, width, 30)
        self.__content = Bouncingball()

    def draw(self):
        pygame_rect(self.screen, (255, 200, 255), self.__content_area_rect) # window background
        self.__drag_bar.draw()
        self.__buttons.draw()
        pygame_rect(self.screen, (0, 0, 0), self.__window_frame_rect, 1)
        self.__content.draw(self.screen, self.__content_area_rect)

    @property
    def active(self) -> bool:
        return self.__active
    
    @active.setter
    def active(self, active):
        self.__active = active

    def event_handler(self, event):
        self.getting_dragged = False
        if self.__buttons["close"].pressed: self.__close()
        elif self.__buttons["minimize"].pressed: self.__minimize()
        elif self.__buttons["maximize"].pressed: self.__maximize()
        elif self.__drag_bar.pressed: self.__dragging()

    def __close(self):
        self.__active = False

    def __minimize(self):
        pass

    def __maximize(self):
        pass

    def __dragging(self):
        self.getting_dragged = True
        mouse_pos = get_pos()
        new_x = mouse_pos[0] - self.__drag_bar.offset[0]
        new_y = mouse_pos[1] - self.__drag_bar.offset[1]
        self.__window_frame_rect.topleft = (new_x, new_y)
        self.__content_area_rect.topleft = (new_x + 1, new_y + 30)
        for i,  button in enumerate(self.__buttons): button.rect.topleft = (new_x + self.__window_frame_rect.width - (i + 1) *30, new_y)
        self.__drag_bar.rect.topleft = (new_x, new_y)


class WindowHandler:
    def __init__(self, **windows):
        self.screen = get_surface()
        if not all(isinstance(window, BaseWindow) for window in windows.values()): raise ValueError("All values must be instances of the BaseWindow class")
        self.windows = windows

    def add_window(self, window, name):
        self.windows[name] = window

    def draw(self):
        [window.draw() for window in self.window_list("last_dragged")[::-1]]

    def event_handler(self, event):
        for window in self.window_list():
            window.event_handler(event)
            if window.getting_dragged == True:
                [setattr(win, "last_dragged", False) for win in self.windows.values()]; window.last_dragged = True
                break
            if not window.active: self.windows = {name: win for name, win in self.windows.items() if win != window}

    def window_list(self, priority="getting_dragged"):
        # returns a list of all windows instances in the handler and if its dragging it will be the first element
        return sorted(self.windows.values(), key=lambda window: getattr(window, priority), reverse=True)

