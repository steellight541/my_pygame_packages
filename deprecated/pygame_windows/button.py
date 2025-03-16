from pygame.font import SysFont
from pygame.mouse import (
    get_pos as get_mouse_pos, 
    get_pressed as get_mouse_pressed
)
from pygame.draw import (rect as pygame_rect)
from pygame.rect import (Rect as pygame_Rect)


class Button:
    def __init__(self, screen, x, y, width, height, text="this is a button", color=(255, 255, 255), text_color=(0, 0, 0), text_centered=True):
        self.screen = screen
        self.rect = pygame_Rect((x, y), (width, height))
        self.__text = {
            "content": text,
            "centered": text_centered,
            "color": text_color,
            "size": 24,
            "font": "arialrounded"
        }
        self.__color = color


    def draw(self):
        pygame_rect(self.screen, self.__color, self.rect)
        text = SysFont(self.__text["font"], self.__text["size"]).render(self.__text["content"], True, self.__text["color"])
        self.screen.blit(
            text, 
            (self.rect.x + self.rect.w //2 - text.get_width()//2, self.rect.y + self.rect.h//2 - text.get_height()//2) 
            if self.__text["centered"] else 
            (self.rect.x + 10, self.rect.y + 10)
        )


    @property
    def pressed(self): return ((self.rect.x <  get_mouse_pos()[0] < self.rect.x + self.rect.y and self.rect.y <  get_mouse_pos()[1] < self.rect.y  + self.rect.h) and get_mouse_pressed()[0])

    @classmethod
    def close_button(cls, screen, x, y, width, height):
        return cls(screen, x, y, width, height, "X", (255, 0, 0), (0, 0, 0), True)
    
    @classmethod
    def minimize_button(cls, screen, x, y, width, height):
        return cls(screen, x, y, width, height, "_", (0, 255, 0), (0, 0, 0), True)
    
    @classmethod
    def maximize_button(cls, screen, x, y, width, height):
        return cls(screen, x, y, width, height, "[]", (0, 0, 255), (0, 0, 0), True)


class ButtonHandler:
    def __init__(self, **buttons):
        # check if all values are Button instances
        if not all(isinstance(button, Button) for button in buttons.values()): raise ValueError("All values must be instances of the Button class")
        self.__buttons = buttons

    def add_button(self, button, name): self.__buttons[name] = button

    def draw(self): [button.draw() for button in self.__buttons.values()]

    def event_handler(self, event): [button.event_handler(event) for button in self.__buttons]

    def get_pressed(self, name): return self[name].pressed

    def update_positions(self, x, y): 
        for button in self.__buttons.values():
            button.rect.topleft = (button.rect.x + x, button.rect.y + y)
    
    def __getitem__(self, key): return self.__buttons[key]
    
    def __iter__(self): return iter(self.__buttons.values())