from enum import Enum
from pygame import Surface, Rect
from pygame.font import Font
from GUI.styles.color import Colors
from GUI.tooltip.tooltip import Tooltip
from GUI.styles.border import Border
from GUI.styles.style import Style


class Button:
    class BehaviorTypes(Enum):
        SINGLE = 1
        DOUBLE = 2
        HOVER = 3

    surface: Surface
    rect: Rect
    text: str
    style: Style
    colors: Colors
    text_surf: Surface
    text_rect: Rect
    font: Font
    tooltip: Tooltip
    
    def __init__(self, surface: Surface, rect: Rect, text: str, style:Style=Style(), tooltip: Tooltip=Tooltip("center")): ...
    def update_text(self, text: str) -> None: ...
    def set_text(self, text: str, padding: int = 5) -> tuple[Surface, Rect, Font]: ...
    def process_text(self, text: str, size: int) -> tuple[Surface, Rect, Font]: ...
    def draw(self, surface: Surface): ...
    def update_colors(self, colors: Colors): ...
    def _on_hover(self): ...
    def update(self) -> None: ...
    def add_border_around_surface(self, border: Border): ...
    
    @property
    def clicked(self) -> bool: ...

    @property
    def hovered(self) -> bool: ...

    @classmethod
    def from_surface(cls, surface: Surface, pos: tuple[int, int] = (0, 0), text: str = "test", style: Style= Style()): ...
    @classmethod  
    def from_rect(cls, rect: Rect, text: str = "test", style: Style=Style()): ...
    @classmethod
    def default(cls, text: str = "Default Button", style: Style=Style()): ...