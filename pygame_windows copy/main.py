from pygame.draw import rect
from pygame.mouse import get_pos
from .button import Button
from .bar import DragBar

class WindowContent(): ... # Placeholder for now

class BaseWindow():
    def __init__(self, screen, width=500, height=400, x=50, y=50):
        self.screen = screen
        self.__window_border_rect = ((x, y), (width, height))
        self.__inner_window_rect = ((x+1, y+1), (width-2, height-2))
        self.__active = True
        self.__buttons = {
            # close button at top right
            "close": Button(screen, x + width - 30, y, 30, 30, "X", (255, 0, 0)),
            "minimize": Button(screen, x + width - 60, y, 30, 30, "_", (0, 255, 0))
        }
        self.__drag_bar = DragBar(screen, x, y, width, 30)

        self.__content = WindowContent()

    

    @property
    def screen(self):
        return self.__screen
    
    @screen.setter
    def screen(self, screen):
        self.__screen = screen

    def draw(self):
        rect(self.screen, (255, 200, 255), self.__inner_window_rect) # window background
        self.__drag_bar.draw()
        [button.draw() for button in self.__buttons.values()]
        rect(self.screen, (0, 0, 0), self.__window_border_rect, 1) # window border

    @property
    def active(self) -> bool:
        return self.__active
    
    @active.setter
    def active(self, active):
        self.__active = active

    def event_handler(self, event):
        if self.__buttons["close"].pressed:
            self.active = False
            return
        if self.__buttons["minimize"].pressed:
            self.active = False
            return
        if self.__drag_bar.pressed:
            mouse_pos = get_pos()
            new_x = mouse_pos[0] - self.__drag_bar.offset[0]
            new_y = mouse_pos[1] - self.__drag_bar.offset[1]
            self.__window_border_rect = ((new_x, new_y), self.__window_border_rect[1])
            self.__inner_window_rect = ((new_x + 1, new_y + 1), self.__inner_window_rect[1])
            self.__buttons["close"].button_rect = ((new_x + self.__window_border_rect[1][0] - 30, new_y), (30, 30))
            self.__buttons["minimize"].button_rect = ((new_x + self.__window_border_rect[1][0] - 60, new_y), (30, 30))
            self.__drag_bar.drag_bar_rect = ((new_x, new_y), (self.__window_border_rect[1][0], 30))
