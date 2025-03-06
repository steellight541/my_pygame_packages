from pygame.font import Font
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect

class Button():
    def __init__(self, screen, x, y, width, height, text, color=(255, 255, 255), text_color=(0, 0, 0), text_centered=True):
        self.screen = screen
        self.button_rect = ((x, y), (width, height))
        self.__text = text
        self.__text_centered = text_centered
        self.__text_color = text_color
        self.__color = color

    @property
    def screen(self):
        return self.__screen
    
    @screen.setter
    def screen(self, screen):
        self.__screen = screen

    def draw(self):
        rect(self.screen, self.__color, self.button_rect)
        font = Font(None, 36)
        text = font.render(self.__text, True, self.__text_color)
        if self.__text_centered:
            self.screen.blit(text, (self.button_rect[0][0] + self.button_rect[1][0]//2 - text.get_width()//2, self.button_rect[0][1] + self.button_rect[1][1]//2 - text.get_height()//2))
        else:
            self.screen.blit(text, (self.button_rect[0][0] + 10, self.button_rect[0][1] + 10))

    @property
    def pressed(self):
        if not get_pressed()[0]:
            return False
        mouse_pos = get_pos()
        return (self.button_rect[0][0] < mouse_pos[0] < self.button_rect[0][0] + self.button_rect[1][0] and self.button_rect[0][1] < mouse_pos[1] < self.button_rect[0][1] + self.button_rect[1][1])

