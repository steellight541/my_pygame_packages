from pygame.display import get_surface
from pygame import Surface
from pygame.font import Font
from pygame.rect import Rect
from ..styles.border import Border # type: ignore
import pygame

class Tooltip:
    screen: Surface|None
    surface: Surface
    rect: Rect
    text_surf: Surface
    text_rect: Rect
    pos: str
    def __init__(self, pos: str, txt: str = "Hello, World!") -> None:
        pygame.font.init()
        self.pos = pos
        self.update_text(txt)

    def update_text(self, text: str) -> None:
        """Update the tooltip text."""
        self.surface = Surface((100, 100))
        self.surface.fill("red")
        self.rect = self.surface.get_rect()
        self.screen = get_surface()
        self.text_surf, self.text_rect, _ = self.set_text(text)
        self.add_text_to_surface()
        self.add_border_around_surface()


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
        text_surf = font.render(text, True, "black")
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect, font


    def add_text_to_surface(self):
        """Add the text to the surface."""
        self.surface.fill("red")  # Clear the surface
        self.surface.blit(self.text_surf, self.text_rect.topleft)


    def add_border_around_surface(self, border: Border = Border("black", 2, 2)):
        self.surface.fill(border.color, (0, 0, self.rect.width, border.top))
        self.surface.fill(border.color, (0, 0, border.left, self.rect.height))
        self.surface.fill(border.color, (0, self.rect.height - border.bottom, self.rect.width, border.bottom))
        self.surface.fill(border.color, (self.rect.width - border.right, 0, border.right, self.rect.height))

    def draw_at(self, pos: tuple[int, int]):
        # atribute rect to pos
        if not self.screen: self.screen = get_surface()
        if any([self.pos == "center", self.pos == "topleft", self.pos == "topright", self.pos == "bottomleft", self.pos == "bottomright"]): setattr(self.rect, self.pos, pos)
        else: raise ValueError("pos_type must be 'center', 'topleft', 'topright', 'bottomleft', or 'bottomright'")
        self.screen.blit(self.surface, self.rect) if self.screen else None # if screen is None, don't draw

if __name__ == "__main__":
    import pygame
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    tooltip = Tooltip("center")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.fill((255, 255, 255))
        tooltip.draw_at(pygame.mouse.get_pos())
        pygame.display.flip()