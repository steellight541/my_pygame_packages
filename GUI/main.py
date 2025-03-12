import pygame
from typing import Any

class Colors:
    background: tuple[int, int, int, int]|str
    border: tuple[int, int, int]|str
    text: str
    def __init__(self, background: tuple[int, int, int, int]|str, border: tuple[int, int, int]|str, text: str) -> None:
        self.background = background
        self.border = border
        self.text = text

    def keys(self):
        return ["background", "border", "text"]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __iter__(self):
        return iter(["background", "border", "text"])
    
    def __repr__(self) -> str:
        return f"Colors({self.background}, {self.border}, {self.text})"
    
    @classmethod
    def default_tooltip_colors(cls) -> "Colors":
        return cls((100, 100, 100, 200), "black", "black")


class Tooltip:
    def __init__(self, text: str, colors: Colors | dict[str, Any] = {}) -> None:
        self.text = text
        self.colors: dict[str, Any] = {**Colors.default_tooltip_colors(), **colors}

    def draw(self, window: pygame.Surface, pos: tuple[int, int]) -> None:
        """hover tooltip"""
        offset = 10
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, True, self.colors["text"])
        text_rect = text.get_rect(bottomleft=(pos[0]+offset//2, pos[1]-offset//2))

        background = pygame.Surface(text_rect.inflate(10, 10).size)
        background.fill(self.colors["background"])
        background.set_alpha(self.colors["background"][3])

        background_rect = background.get_rect()
        background_rect.bottomleft = pos

        pygame.draw.rect(background, self.colors["border"], background.get_rect(), 2)
        window.blit(background, background_rect)
        window.blit(text, text_rect)

class Button:
    def __init__(self, rect: pygame.Rect | pygame.Surface, value: int | None = None, text: str = "", resize: tuple[int, int] | None = None, pos: tuple[int, int] | None = None, tooltip: Tooltip | None = None) -> None:
        self.surface = pygame.Surface(rect.size) if isinstance(rect, pygame.Rect) else rect
        self.rect = rect if isinstance(rect, pygame.Rect) else self.surface.get_rect()
        self.surface.fill("lightblue") if isinstance(rect, pygame.Rect) else None
        
        if pos:
            self.rect.topleft = pos
        self.surface = pygame.transform.scale(self.surface, resize) if resize else self.surface
        self.rect.size = self.surface.get_size()
        
        self.value = value
        self.text = text
        self.tooltip = tooltip
        self.__frozen = False
        
        self.update_text(text)

    def update_text(self, text: str) -> None:
        self.text = text
        min_font_size, max_font_size = 1, self.rect.height - 10
        
        while max_font_size - min_font_size > 1:
            mid_font_size = (min_font_size + max_font_size) // 2
            self.layout_text(mid_font_size)
            if self.text_rect.width <= self.rect.width - 10:
                min_font_size = mid_font_size
            else:
                max_font_size = mid_font_size
        
        self.layout_text(min_font_size)

    def layout_text(self, font_size: int) -> None:
        font = pygame.font.Font(None, font_size)
        self.text_surface = font.render(self.text, True, "black")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.surface, self.rect)
        window.blit(self.text_surface, self.text_rect)
        
        if self.tooltip and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.tooltip.draw(window, pygame.mouse.get_pos())

    @property
    def pressed(self) -> bool:
        return not self.__frozen and self.rect.collidepoint(pygame.mouse.get_pos())

    def freeze(self) -> None:
        self.__frozen = True

    def unfreeze(self) -> None:
        self.__frozen = False
