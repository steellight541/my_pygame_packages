from GUI.styles import Style, Border
import pygame


class Tooltip:
    def __init__(self, pos_style: str, txt: str = "Hello, World!", style: Style = Style()) -> None:
        pygame.font.init()
        self.pos_style = pos_style
        self.update_text(txt, style)

    def update_text(self, text: str, style: Style) -> None:
        """Update the tooltip text."""
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(style.colors.tooltip)
        self.rect = self.surface.get_rect()
        self.text_surf, self.text_rect, _ = self.set_text(text, style)
        self.add_text_to_surface()

    def set_text(self, text: str, style: Style, padding: int = 5) -> tuple[pygame.Surface, pygame.Rect, pygame.font.Font]:
        """Dynamically finds the best font size using binary search."""
        min_size, max_size = 1, self.rect.width 
        while min_size < max_size:
            size = (min_size + max_size) // 2
            _, text_rect, _ = self.process_text(text, size, style)
            if text_rect.width + 5 > self.rect.width - padding: max_size = size
            else: min_size = size + 1
        return self.process_text(text, min_size, style)
    

    def process_text(self, text: str, size: int, style: Style) -> tuple[pygame.Surface, pygame.Rect, pygame.font.Font]:
        """Creates a surface and rect for the text."""
        font = pygame.font.Font(None, size)
        text_surf = font.render(text, True, style.colors.text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect, font
    
    def add_text_to_surface(self):
        """Add the text to the surface."""
        self.surface.fill("red")
        self.surface.blit(self.text_surf, self.text_rect.topleft)

    def draw_at(self, pos: tuple[int, int]) -> None:
        """Draw the tooltip at the provided position."""
        self.rect.topleft = pos
        self.add_border_around_surface()
        if any([self.pos_style == "topleft", self.pos_style == "bottomleft", self.pos_style == "topright", self.pos_style == "bottomright"]): setattr(self.rect, self.pos_style, pos)
        pygame.display.get_surface().blit(self.surface, self.rect.topleft) # type: ignore

    def add_border_around_surface(self, border: Border = Border("black", 2, 2)):# type: ignore
        self.surface.fill(border.color, (0, 0, self.rect.width, border.top))
        self.surface.fill(border.color, (0, 0, border.left, self.rect.height))
        self.surface.fill(border.color, (0, self.rect.height - border.bottom, self.rect.width, border.bottom))
        self.surface.fill(border.color, (self.rect.width - border.right, 0, border.right, self.rect.height))