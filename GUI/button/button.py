from enum import Enum
import pygame
from GUI.styles import *
from GUI.tooltip import Tooltip

class Button:
    class BehaviorTypes(Enum):
        """The different types of button behaviors."""
        SINGLE = 1
        DOUBLE = 2
        HOVER = 3

    def __init__(
            self,
            surface: pygame.Surface, rect: pygame.Rect,
            text: str,
            style: Style, tooltip: Tooltip # type: ignore
            ) -> None:
        """Initialize the button with a predefined surface and rect."""
        self.surface = surface
        self.rect = rect
        self.text = text
        self.style = style
        self.tooltip = tooltip # this is a Tooltip object for hover info text
        self.text_surf, self.text_rect, self.font = self.set_text(text)
        self.surface.fill(self.style.colors.button)
        self.add_border_around_surface(self.style.border)
        

    def update_text(self, text: str) -> None:
        """Update the button text."""
        self.text = text
        self.text_surf, self.text_rect, self.font = self.set_text(text)

    def set_text(self, text: str, padding: int = 5) -> tuple[pygame.Surface, pygame.Rect, pygame.font.Font]:
        """Dynamically finds the best font size using binary search."""
        min_size, max_size = 1, self.rect.width 
        while min_size < max_size:
            size = (min_size + max_size) // 2
            _, text_rect, _ = self.process_text(text, size)
            if text_rect.width + 5 > self.rect.width - padding: max_size = size
            else: min_size = size + 1
        return self.process_text(text, min_size)

    def process_text(self, text: str, size: int) -> tuple[pygame.Surface, pygame.Rect, pygame.font.Font]:
        """Creates a surface and rect for the text."""
        font = pygame.font.Font(None, size)
        text_surf = font.render(text, True, self.style.colors.text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect, font

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the button onto the provided surface."""
        self.add_border_around_surface(self.style.border)
        surface.blit(self.surface, self.rect.topleft)
        surface.blit(self.text_surf, self.text_rect.topleft)
        if self.tooltip and self.hovered: self.tooltip.draw_at(pygame.mouse.get_pos())

    def update_style(self, style: Style) -> None:
        """Update the button style."""
        self.style = style
        self.surface.fill(self.style.colors.button if not self.hovered else self.style.colors.hovered)
        self.text_surf = self.font.render(self.text, True, self.style.colors.text)

    def add_border_around_surface(self, border: Border) -> None:
        """Add a border around the button."""
        self.surface.fill(border.color, (0, 0, self.rect.width, border.top))
        self.surface.fill(border.color, (0, 0, border.left, self.rect.height))
        self.surface.fill(border.color, (0, self.rect.height - border.bottom, self.rect.width, border.bottom))
        self.surface.fill(border.color, (self.rect.width - border.right, 0, border.right, self.rect.height))

    def update(self) -> None:
        """Update the button."""
        self.update_style(self.style)

    @property
    def clicked(self) -> bool:
        """Returns True if the button was clicked."""
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    @property
    def hovered(self) -> bool:
        """Returns True if the button is hovered."""
        return self.rect.collidepoint(pygame.mouse.get_pos())
    

    @classmethod
    def from_surface(cls, surface: pygame.Surface, pos: tuple[int, int] = (0, 0), text: str = "test", style: Style = Style(), tooltip: Tooltip = Tooltip("center")) -> "Button":
        """Create a button from a surface."""
        return cls(surface, surface.get_rect(topleft=pos), text, style, tooltip)
    
    @classmethod
    def from_rect(cls, rect: pygame.Rect, text: str = "test", style: Style = Style(), tooltip: Tooltip = Tooltip("center")) -> "Button":
        """Create a button from a rect."""
        return cls(pygame.Surface(rect.size), rect, text, style, tooltip)
    
    @classmethod
    def default(cls, text: str = "Default Button", style: Style = Style(), tooltip: Tooltip = Tooltip("center")) -> "Button":
        """Create a default button."""
        return cls.from_rect(pygame.Rect(0, 0, 100, 50), text, style, tooltip)