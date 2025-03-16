from color import Colors 
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mouse import get_pos
__all__ = ["Button"]
__file__ = "GUI/button/button.py"

class Button:
    def __init__(self, surface: Surface, rect: Rect, text: str, colors: Colors | None):
        """Initialize the button with a predefined surface and rect."""
        self.surface = surface
        self.rect = rect
        self.colors = colors or Colors()
        # Fill and set text
        self.surface.fill(self.colors.button)
        self.update_text(text)

    def update_text(self, text: str) -> None:
        """Update the button text."""
        self.text = text
        self.text_surf, self.text_rect = self.set_text(text)

    @classmethod
    def from_surface(cls, surface: Surface, pos: tuple[int, int] = (0, 0), text: str = "test", colors: Colors | None = None):
        """Alternative constructor: Create a button from an existing surface."""
        rect = surface.get_rect(topleft=pos)
        return cls(surface, rect, text, colors)

    @classmethod
    def from_rect(cls, rect: Rect, text: str = "test", colors: Colors | None = None):
        """Alternative constructor: Create a button from a rect."""
        surface = Surface(rect.size)
        return cls(surface, rect, text, colors)

    @classmethod
    def default(cls, text: str = "Default Button", colors: Colors | None = None):
        """Alternative constructor: Create a default button (150x50)."""
        return cls.from_rect(Rect(0, 0, 150, 50), text, colors)

    def set_text(self, text: str, padding: int = 5) -> tuple[Surface, Rect]:
        """Dynamically finds the best font size using binary search."""
        min_size, max_size = 1, self.rect.width 
        while min_size < max_size:
            size = (min_size + max_size) // 2
            _, text_rect = self.process_text(text, size)
            if text_rect.width + 5 > self.rect.width - padding: max_size = size
            else: min_size = size + 1
        return self.process_text(text, min_size)

    def process_text(self, text: str, size: int) -> tuple[Surface, Rect]:
        """Creates a surface and rect for the text."""
        font = Font(None, size)
        text_surf = font.render(text, True, self.colors.text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect
    
    def update_visuals(self):
        """Update the button visuals."""
        if self.hovered: self.surface.fill(self.colors.hovered)
        else: self.surface.fill(self.colors.button)

    def draw(self, surface: Surface):
        """Draws the button onto the provided surface."""
        self.update_visuals()
        surface.blit(self.surface, self.rect.topleft)
        surface.blit(self.text_surf, self.text_rect.topleft)

    def update_colors(self, colors: Colors):
        """Update the button colors."""
        self.colors = colors
        self.surface.fill(self.colors.button)
        self.text_surf, self.text_rect = self.set_text(self.text)

    @property
    def clicked(self) -> bool:
        """Returns True if the button is clicked."""
        return self.rect.collidepoint(*get_pos())
    
    @property
    def hovered(self) -> bool:
        """Returns True if the button is hovered."""
        return self.rect.collidepoint(*get_pos())