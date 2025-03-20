from GUI.styles.color import Colors 
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mouse import get_pos
from enum import Enum
from GUI.tooltip.tooltip import Tooltip
from GUI.styles.border import Border
from GUI.styles.style import Style

__all__ = ["Button"]
__file__ = "GUI/button/button.py"


class Button():
    class BehaviorTypes(Enum):
        SINGLE = 1 # Single click
        DOUBLE = 2 # Double click
        HOVER = 3 # Hover


    def __init__(self, surface: Surface, rect: Rect, text: str, style: Style = Style(), Tooltip: Tooltip = Tooltip("topleft")):
        """Initialize the button with a predefined surface and rect."""

        self.surface = surface
        self.rect = rect
        self.style = style
        self.colors = style.colors
        # Fill and set text
        self.surface.fill(self.colors.button)
        self.update_text(text)
        self.tooltip = Tooltip

    def update_text(self, text: str) -> None:
        """Update the button text."""
        self.text = text
        self.text_surf, self.text_rect, self.font = self.set_text(text)

    def set_text(self, text: str, padding: int = 5) -> tuple[Surface, Rect, Font]:
        """Dynamically finds the best font size using binary search."""
        min_size, max_size = 1, self.rect.width 
        while min_size < max_size:
            size = (min_size + max_size) // 2
            _, text_rect, _ = self.process_text(text, size)
            if text_rect.width + 5 > self.rect.width - padding: max_size = size
            else: min_size = size + 1
        return self.process_text(text, min_size)

    def process_text(self, text: str, size: int) -> tuple[Surface, Rect, Font]:
        """Creates a surface and rect for the text."""
        font = Font(None, size)
        text_surf = font.render(text, True, self.colors.text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect, font
    

    def draw(self, surface: Surface):
        """Draws the button onto the provided surface."""
        self.add_border_around_surface(self.style.border)
        surface.blit(self.surface, self.rect.topleft)
        surface.blit(self.text_surf, self.text_rect.topleft)
        if self.tooltip and self.hovered: self.tooltip.draw_at(get_pos())

    def update_colors(self, colors: Colors):
        """Update the button colors."""
        self.colors = colors
        self.surface.fill(self.colors.button if not self.hovered else self.colors.hovered)
        self.text_surf = self.font.render(self.text, True, self.colors.text)

    def add_border_around_surface(self, border: Border = Border("black", 2, 2)):
        """Add a border around the button."""
        self.surface.fill(border.color, (0, 0, self.rect.width, border.top))
        self.surface.fill(border.color, (0, 0, border.left, self.rect.height))
        self.surface.fill(border.color, (0, self.rect.height - border.bottom, self.rect.width, border.bottom))
        self.surface.fill(border.color, (self.rect.width - border.right, 0, border.right, self.rect.height))

    def _on_hover(self):
        """Called when the button is hovered."""
        ... # Placeholder for custom hover behavior

    def update(self):
        """Handle mouse click events."""
        self.update_colors(self.colors)

    def move(self, pos: tuple[int, int]):
        """Move the button to a new position."""
        self.rect.topleft = pos
        self.update_text(self.text)

    @property
    def clicked(self) -> bool:
        """Returns True if the button is clicked."""
        return self.rect.collidepoint(*get_pos())
    
    @property
    def hovered(self) -> bool:
        """Returns True if the button is hovered."""
        return self.rect.collidepoint(*get_pos())
    

    @classmethod
    def from_surface(cls, surface: Surface, pos: tuple[int, int] = (0, 0), text: str = "test", style: Style = Style()):
        """Alternative constructor: Create a button from an existing surface."""
        rect = surface.get_rect(topleft=pos)
        return cls(surface, rect, text, style)

    @classmethod
    def from_rect(cls, rect: Rect, text: str = "test", style: Style = Style()):
        """Alternative constructor: Create a button from a rect."""
        surface = Surface(rect.size)
        return cls(surface, rect, text, style)

    @classmethod
    def default(cls, text: str = "Default Button", style: Style = Style()):
        """Alternative constructor: Create a default button (150x50)."""
        return cls.from_rect(Rect(0, 0, 150, 50), text, style)
