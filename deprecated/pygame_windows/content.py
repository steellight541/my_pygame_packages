from pygame.locals import *
from pygame.draw import rect, circle

class WindowContent:
    def __init__(self):
        self.bounding_box = None

    def draw(self, screen, bounding_box):
        self.bounding_box = Rect(bounding_box)
        screen.set_clip(bounding_box)
        self._draw(screen)
        screen.set_clip(None)

    def _draw(self, screen): ...

    def draw_rect(self, screen, rect_, color):
        rect(screen, color, Rect(rect_).move(self.bounding_box.topleft))


    def draw_circle(self, screen, pos, radius, color):
        circle(screen, color, Rect(self.bounding_box.topleft, (0,0)).move(pos).center, radius)