from GUI.button import *
from typing import Callable
from pygame import Surface
from pygame.event import Event
__all__ = [
    "ButtonHandler", 
    "ClickType", 
    "GUIHandler", 
    "Button"
]

class GUIHandler:
    """renders and manages GUI elements on a separate Thread."""
    def __init__(self):
        self._buttons = ButtonHandler()
        self._running = False
        self._thread = None

    def add_button(self, button: Button) -> Button:
        """Add a button to the handler."""
        return self._buttons.add_button(button)

    def remove_button(self, button: Button):
        """Remove a button from the handler."""
        self._buttons.remove_button(button)

    def clear(self):
        """Remove all buttons and their listeners."""
        self._buttons.clear()

    def draw(self, surface: Surface):
        """Draw all buttons on the given surface."""
        self._buttons.draw(surface)

    def button_connect(self, button: Button, listener: Callable[[Button], None], click_type: ClickType = ClickType.ONCE):
        """Attach a listener to a button. If single=True, the listener is removed after being called once."""
        self._buttons.connect(button, listener, click_type)

    def disconnect(self, button: Button, click_type: ClickType = ClickType.ONCE):
        """Remove a listener from a button."""
        self._buttons.disconnect(button, click_type)

    def handle_events(self, event: Event):
        """Handle mouse click events and trigger listeners."""
        self._buttons.handle_events(event)
