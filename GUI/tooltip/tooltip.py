from pygame.display import get_surface
from pygame import Surface
from pygame.font import Font
from pygame.rect import Rect
from ..styles.border import Border # type: ignore

class Tooltip:
    screen: Surface|None
    surface: Surface
    rect: Rect
    text_surf: Surface
    text_rect: Rect
    def __init__(self): 
        self.surface = Surface((100, 100))
        self.surface.fill("red")
        self.rect = self.surface.get_rect()
        self.screen = get_surface()
        self.update_text("test", Font(None, 12))
        self.add_text_to_surface()
        self.add_border_around_surface()

    def set_text(self, text: str, font: Font, padding: int = 5) -> tuple[Surface, Rect]:
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        return text_surf, text_rect

    def update_text(self, text: str, font: Font, padding: int = 5):
        self.text_surf, self.text_rect = self.set_text(text, font, padding)

    def add_text_to_surface(self):
        self.surface.blit(self.text_surf, self.text_rect.topleft)


    def add_border_around_surface(self, border: Border = Border("black", 2, 20)):
        self.surface.fill(border.color, (0, 0, self.rect.width, border.top))# Top
        self.surface.fill(border.color, (0, self.rect.height-border.bottom, self.rect.width, border.bottom))# Bottom
        self.surface.fill(border.color, (0, 0, border.left, self.rect.height))# Left
        self.surface.fill(border.color, (self.rect.width-border.right, 0, border.right, self.rect.height)) # Right


    def draw_at(self, pos: tuple[int, int], pos_type: str = "center"):
        # atribute rect to pos
        if any([pos_type == "center", pos_type == "topleft", pos_type == "topright", pos_type == "bottomleft", pos_type == "bottomright"]):
            setattr(self.rect, pos_type, pos)
        else: raise ValueError("pos_type must be 'center', 'topleft', 'topright', 'bottomleft', or 'bottomright'")
        self.screen.blit(self.surface, self.rect) if self.screen else None


if __name__ == "__main__":
    import pygame
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    tooltip = Tooltip()
    tooltip.update_text("Hello, World!", Font(None, 12))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.fill((255, 255, 255))
        tooltip.draw_at(pygame.mouse.get_pos())
        pygame.display.flip()