from typing import Callable
from button import Button
from pygame import Surface, Event
from enum import Enum

class ButtonHandler:
    _buttons: set[Button]
    _listeners: dict[Button, Callable[[Button], None]]
    _double_click_time: dict[Button, float]
    DOUBLE_CLICK_TIME: float

    def __init__(self) -> None: ...
    def add_button(self, button: Button) -> Button: ...
    def remove_button(self, btn: Button) -> None: ...
    def clear(self) -> None: ...
    def draw(self, surface: Surface) -> None: ...
    def connect(self, button: Button, listener: Callable[[Button], None], click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE) -> None: ...
    def disconnect(self, button: Button, click_type: Button.BehaviorTypes = Button.BehaviorTypes.SINGLE) -> None: ...
    def handle_events(self, event: Event) -> None: ...
    def update(self) -> None: ...