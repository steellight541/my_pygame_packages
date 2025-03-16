from typing import Callable
from button import Button
from pygame import Surface, Event
from enum import Enum

class ClickType(Enum):
    SINGLE = 1
    DOUBLE = 2
    ONCE = 3
    ALL = 4
    HOVER = 5

class ButtonHandler:
    _buttons: set[Button]
    _listeners: dict[Button, Callable[[Button], None]]
    _single_events: dict[Button, Callable[[Button], None]]
    _double_click: dict[Button, Callable[[Button], None]]
    _double_click_time: dict[Button, float]
    DOUBLE_CLICK_TIME: float

    def __init__(self) -> None: ...
    def add_button(self, button: Button) -> Button: ...
    def remove_button(self, btn: Button) -> None: ...
    def clear(self) -> None: ...
    def draw(self, surface: Surface) -> None: ...
    def connect(self, button: Button, listener: Callable[[Button], None], click_type: ClickType = ClickType.SINGLE) -> None: ...
    def disconnect(self, button: Button, click_type: ClickType = ClickType.SINGLE) -> None: ...
    def handle_events(self, event: Event) -> None: ...