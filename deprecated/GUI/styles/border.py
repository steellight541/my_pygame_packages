from typing import Any

class Border:
    """A border for a GUI element."""
    color: Any
    width: tuple[int, int, int, int]

    def __init__(self, color: Any, *width: int) -> None:
        self.color = color
        if len(width) == 1:
            self.width = (width[0], width[0], width[0], width[0])
        elif len(width) == 2:
            self.width = (width[0], width[1], width[0], width[1])
        elif len(width) == 4:
            self.width = width
        else: raise ValueError("Border must have 1, 2, or 4 arguments.")

    @property
    def top(self) -> int:
        return self.width[0]
    
    @property
    def right(self) -> int:
        return self.width[1]
    
    @property
    def bottom(self) -> int:
        return self.width[2]
    
    @property
    def left(self) -> int:
        return self.width[3]
    
    @classmethod
    def default(cls) -> "Border":
        return cls("black", 2, 2, 2, 2)
    
    def __repr__(self) -> str:
        return f"Border({self.color}, {self.width})"