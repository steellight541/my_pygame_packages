from typing import Callable
from .button import Button
from pygame import Surface, Event, MOUSEBUTTONDOWN
import time
__all__ = ["ButtonHandler"] # this is a list of strings that will be imported when using "from button import *" in another file
__file__ = "GUI/button/buttonhandler.py" # this is the path to the file



class ButtonHandler:
    """A class to manage multiple buttons and their listeners."""
    _buttons: set[Button]
    _listeners: dict[str, dict[Button, Callable[[Button], None]]]
    _double_click_time: dict[Button, float]
    DOUBLE_CLICK_TIME = 0.3
    
    def __init__(self):
        self._buttons = set()
        self._listeners = {
            "single": {},
            "double": {},
            "hover": {}
        }
        self._double_click_time = {}

    def add_button(self, button: Button) -> Button:
        """Add a button to the handler."""
        self._buttons.add(button)
        return button

    def remove_button(self, btn: Button):
        """Remove a button from the handler."""
        self._buttons.remove(btn)


    def clear(self):
        """Remove all buttons and their listeners."""
        self._buttons.clear()
        self._listeners.clear()

    def draw(self, surface: Surface):
        """Draw all buttons on the given surface."""
        [button.draw(surface) for button in self._buttons]

    def connect(self, button: Button, listener: Callable[[Button], None], click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE):
        """Attach a listener to a button. If single=True, the listener is removed after being called once."""
        match click_type:
            case Button.BehaviorTypes.SINGLE:
                self._listeners["single"][button] = listener
            case Button.BehaviorTypes.DOUBLE:
                self._listeners["double"][button] = listener
            case Button.BehaviorTypes.HOVER:
                self._listeners["hover"][button] = listener
            case _:
                raise ValueError("Invalid click type")

    def disconnect(self, button: Button, click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE):
        """Remove a listener from a button."""
        match click_type:
            case Button.BehaviorTypes.SINGLE:
                del self._listeners["single"][button]
            case Button.BehaviorTypes.DOUBLE:
                del self._listeners["double"][button]
            case _:
                raise ValueError("Invalid click type")

    def handle_events(self, event: Event):
        """Handle mouse click events and trigger listeners."""
        for button in self._buttons.copy():
            if event.type == MOUSEBUTTONDOWN and button.clicked and event.button == 1:
                if button in self._double_click_time:
                    if time.time() - self._double_click_time[button] < self.DOUBLE_CLICK_TIME:
                        if button in self._listeners["double"]:
                            self._listeners["double"][button](button)
                        del self._double_click_time[button]
                        continue
                self._double_click_time[button] = time.time()
                if button in self._listeners["single"]:
                    self._listeners["single"][button](button)

    def update(self):
        for button in self._buttons.copy():
            button.update()
            if button.hovered and button in self._listeners["hover"]:
                    self._listeners["hover"][button](button)

if __name__ == "__main__":
    from button import Button
    import pygame
    pygame.init()
    