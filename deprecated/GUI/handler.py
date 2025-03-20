from GUI.button import Button, ButtonHandler
from typing import Callable, Any
from pygame import Surface
from pygame.event import Event
from functools import wraps

__all__ = [
    "ButtonHandler", 
    "GUIHandler",
    "Button",
    "auto_connect"
]

def auto_connect(button_name: str, click_type: Button.BehaviorTypes):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(wrapper, "__connect_info__", (button_name, click_type))
        return wrapper
    return decorator

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

    def button_connect(self, button: Button, listener: Callable[[Button], None], click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE):
        """Attach a listener to a button. If single=True, the listener is removed after being called once."""
        self._buttons.connect(button, listener, click_type)

    def button_disconnect(self, button: Button, click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE):
        """Remove a listener from a button."""
        self._buttons.disconnect(button, click_type)

    def handle_events(self, event: Event):
        """Handle mouse click events and trigger listeners."""
        self._buttons.handle_events(event)

    def connect(self, button: Any, click_type: Button.BehaviorTypes) -> Callable[[Callable[[Button], None]], Callable[[Button], None]]:
        """Decorator for connecting a listener to a button."""
        def decorator(listener: Callable[[Any], None]):
            if isinstance(button, Button):
                self.button_connect(button, listener, click_type)
            return listener
        return decorator
    
    def update(self):
        """Update the handler."""
        self._buttons.update()

    def auto_connect(self, cls: object):
        """Automatically connect all button listeners in the class."""
        for attr in dir(cls):
            method = getattr(cls, attr)
            if callable(method) and hasattr(method, "__connect_info__"):
                button_name, click_type = method.__connect_info__
                button = getattr(cls, button_name, None)
                if button: self.button_connect(button, method, click_type) # type: ignore
        return cls