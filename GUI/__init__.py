from .tooltip import Tooltip
from .button import Button, ButtonHandler
from .styles import Style, Border, Padding, Colors
from functools import wraps

def auto_connect(button_name: str, click_type: Button.BehaviorTypes):
    def decorator(func):
        # Attach connection info to the function
        func.__connect_info__ = (button_name, click_type)
        return func
    return decorator

class GUIHandler:
    _button_handler: ButtonHandler = ButtonHandler()

    def add_handler(self, handler):
        if isinstance(handler, ButtonHandler):
            self._button_handler = handler
        else:
            raise Exception(f"handler: {handler} is unknown")

    def add_handlers(self, *args):
        for h in args:
            self.add_handler(h)

    def add_button(self, btn):
        self._button_handler.add_button(btn)

    def button_connect(self, btn, callback, clicktype):
        self._button_handler.add_listener(btn, callback, clicktype)

    def handle_event(self, event):
        self._button_handler.handle_event(event)

    def draw(self, surf):
        self._button_handler.draw(surf)

    def update(self):
        self._button_handler.update()

    def auto_connect(self, cls: object):
        """Automatically connect all button listeners in the class."""
        for attr_name in dir(cls):
            method = getattr(cls, attr_name)
            if callable(method) and hasattr(method, "__connect_info__"):
                button_name, click_type = method.__connect_info__
                button = getattr(cls, button_name, None)
                if button: self.button_connect(button, method, click_type)  # Properly register the callback
                else: raise AttributeError(f"Button '{button_name}' not found in the class.")


    # @GUIHandler.connect(btn, clicktype)
    def connect(self, btn, clicktype):
        def decorator(func):
            self.button_connect(btn, func, clicktype)
            return func
        return decorator
