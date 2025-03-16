from typing import Callable
from .button import Button
from pygame import Surface, Event, MOUSEBUTTONDOWN
from enum import Enum
import time
__all__ = ["ButtonHandler", "ClickType"] # this is a list of strings that will be imported when using "from button import *" in another file
__file__ = "GUI/button/buttonhandler.py" # this is the path to the file

class ClickType(Enum):
    SINGLE = 1 # Single click
    DOUBLE = 2 # Double click
    ONCE = 3 # Single event listener
    ALL = 4 # Remove all listeners
    HOVER = 5 # Not implemented yet

class ButtonHandler:
    """A class to manage multiple buttons and their listeners."""
    _buttons: set[Button]
    _listeners: dict[Button, Callable[[Button], None]]
    _single_events: dict[Button, Callable[[Button], None]]
    _double_click: dict[Button, Callable[[Button], None]]
    _double_click_time: dict[Button, float]
    _hover_events: dict[Button, Callable[[Button], None]]
    DOUBLE_CLICK_TIME = 0.3
    
    def __init__(self):
        self._buttons = set()
        self._listeners = {}
        self._single_events = {}
        self._double_click = {}
        self._double_click_time = {}
        self._hover_events = {}

    def add_button(self, button: Button) -> Button:
        """Add a button to the handler."""
        self._buttons.add(button)
        return button

    def remove_button(self, btn: Button):
        """Remove a button from the handler."""
        self._buttons.remove(btn)
        self._listeners.pop(btn, None)
        self._single_events.pop(btn, None)

    def clear(self):
        """Remove all buttons and their listeners."""
        self._buttons.clear()
        self._listeners.clear()
        self._single_events.clear()

    def draw(self, surface: Surface):
        """Draw all buttons on the given surface."""
        [button.draw(surface) for button in self._buttons]

    def connect(self, button: Button, listener: Callable[[Button], None], click_type: ClickType = ClickType.ONCE):
        """Attach a listener to a button. If single=True, the listener is removed after being called once."""
        match click_type:
            case ClickType.SINGLE:
                self._single_events[button] = listener
            case ClickType.DOUBLE:
                self._double_click[button] = listener
            case ClickType.ONCE:
                self._listeners[button] = listener
            case ClickType.ALL: ...
            case ClickType.HOVER:
                self._hover_events[button] = listener
            case _:
                raise ValueError("Invalid click type")

    def disconnect(self, button: Button, click_type: ClickType = ClickType.ONCE):
        """Remove a listener from a button."""
        match click_type:
            case ClickType.SINGLE:
                self._single_events.pop(button, None)
            case ClickType.ONCE:
                self._listeners.pop(button, None)
            case ClickType.DOUBLE:
                self._double_click.pop(button, None)
            case ClickType.ALL:
                map(self.disconnect, [button], [ClickType.SINGLE, ClickType.ONCE, ClickType.DOUBLE])
            case ClickType.HOVER:
                self._hover_events.pop(button, None)
            case _:
                raise ValueError("Invalid click type")

    def handle_events(self, event: Event):
        """Handle mouse click events and trigger listeners."""
        if event.type == MOUSEBUTTONDOWN:
            
            for button in self._buttons.copy():
                if button.clicked:
                    if button in self._listeners:
                        self._listeners[button](button)
                    if button in self._single_events:
                        self._single_events.pop(button)(button)
                    if button in self._double_click:
                        current_time = time.time()
                        if button in self._double_click_time:
                            if current_time - self._double_click_time[button] < self.DOUBLE_CLICK_TIME:
                                self._double_click[button](button)
                                del self._double_click_time[button]
                            else: self._double_click_time[button] = current_time
                        else: self._double_click_time[button] = current_time


        for button in self._buttons.copy():
            if button.hovered:
                if button in self._hover_events:
                    self._hover_events[button](button)

if __name__ == "__main__":
    from button import Button
    import pygame
    pygame.init()
    