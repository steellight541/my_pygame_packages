from pygame.draw import rect, circle
from pygame.mouse import get_pos
from .button import Button
from .bar import DragBar

from pygame.rect import Rect
import pygame


class WindowContent:
    def __init__(self):
        # Initialize content here
        self.bounding_box = None
        pass

    def draw(self, screen, bounding_box):
        self.bounding_box = Rect(bounding_box)
        screen.set_clip(bounding_box)
        self._draw(screen)
        screen.set_clip(None)

    def _draw(self, screen):
        # Draw content here
        self.draw_rect(screen, (0, 0, 100, 100), (0, 0, 255))

    def draw_rect(self, screen, rect_, color):
        # make rect_ relative to bounding_box
        rect(screen, color, Rect(rect_).move(self.bounding_box.topleft))


    def draw_circle(self, screen, pos, radius, color):
        circle(screen, color, Rect(self.bounding_box.topleft, (0,0)).move(pos).center, radius)

class Bouncingball(WindowContent):
    # this is a subclass of WindowContent to demonstrate how to create a custom content class
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 20
        self.dx = 0.1
        self.dy = 0
        self.gravity = 0.01

    def _draw(self, screen):
        self.draw_circle(screen, (self.x, self.y), 10, (255, 0, 0))
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity

        # Check for bounce
        if self.y + 10 >= self.bounding_box.height:
            self.y = self.bounding_box.height - 10
            self.dy = -self.dy * 0.8  # Reverse direction and reduce speed

        # if it hits the top, reverse direction
        if self.y - 10 <= 0:
            self.y = 9

        # Reset bounce if speed is very low
        if abs(self.dy) < 0.1 and self.y + 10 >= self.bounding_box.height:
            import random
            self.dy = random.uniform(-5, 1)

        if self.x + 10 >= self.bounding_box.width:
            self.x = self.bounding_box.width - 10
            self.dx = -self.dx

        if self.x - 10 <= 0:
            self.x = 10
            self.dx = -self.dx



class BaseWindow:
    def __init__(self, screen, width=500, height=400, x=50, y=50):
        self.screen = screen
        self.__window_border_rect = ((x, y), (width, height))
        self.__inner_window_rect = ((x+1, y+31), (width-2, height-32))  # Adjusted for draggable bar height
        self.__active = True
        self.__buttons = {
            # close button at top right
            "close": Button(screen, x + width - 30, y, 30, 30, "X", (255, 0, 0)),
            "minimize": Button(screen, x + width - 60, y, 30, 30, "_", (0, 255, 0))
        }
        self.__drag_bar = DragBar(screen, x, y, width, 30)

        self.__content = Bouncingball()

    def draw(self):
        rect(self.screen, (255, 200, 255), self.__inner_window_rect) # window background
        self.__drag_bar.draw()
        [button.draw() for button in self.__buttons.values()]
        rect(self.screen, (0, 0, 0), self.__window_border_rect, 1) # window border
        self.__content.draw(self.screen, self.__inner_window_rect)

    @property
    def active(self) -> bool:
        return self.__active
    
    @active.setter
    def active(self, active):
        self.__active = active

    def event_handler(self, event):
        if self.__buttons["close"].pressed:
            self.active = False
        elif self.__buttons["minimize"].pressed:
            self.active = False
        elif self.__drag_bar.pressed:
            mouse_pos = get_pos()
            new_x = mouse_pos[0] - self.__drag_bar.offset[0]
            new_y = mouse_pos[1] - self.__drag_bar.offset[1]
            self.__window_border_rect = ((new_x, new_y), self.__window_border_rect[1])
            self.__inner_window_rect = ((new_x + 1, new_y + 31), (self.__window_border_rect[1][0] - 2, self.__window_border_rect[1][1] - 32))  # Adjusted for draggable bar height
            self.__buttons["close"].button_rect = Rect((new_x + self.__window_border_rect[1][0] - 30, new_y), (30, 30))
            self.__buttons["minimize"].button_rect = Rect((new_x + self.__window_border_rect[1][0] - 60, new_y), (30, 30))
            self.__drag_bar.drag_bar_rect = Rect((new_x, new_y), (self.__window_border_rect[1][0], 30))
