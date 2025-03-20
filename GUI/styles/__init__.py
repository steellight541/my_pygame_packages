class Colors:
    button: tuple[int, int, int]|str
    hovered: tuple[int, int, int]|str
    text: tuple[int, int, int]|str
    """A class to represent the colors of a button."""
    def __init__(
            self, 
            button: tuple[int, int, int] = (200, 200, 200), 
            hovered: tuple[int, int, int] = (150, 150, 150), 
            text: tuple[int, int, int] = (0, 0, 0), 
            tooltip: tuple[int, ...] = (0,0,0)
            ) -> None:
        """Initialize the colors of the button."""
        self.button = button
        self.hovered = hovered
        self.text = text
        self.tooltip = tooltip

    @classmethod
    def default(cls) -> "Colors":
        """Create a default color scheme."""
        return cls()
class Border:
    """A class to represent the border of a button."""
    color: tuple[int, int, int]|str
    top: int
    right: int
    bottom: int
    left: int
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0), top: int = 2, right: int = 2, bottom: int = 2, left: int = 2) -> None:
        """Initialize the border with default values."""
        self.color = color
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @classmethod
    def default(cls) -> "Border":
        """Create a default border."""
        return cls()

    def __repr__(self) -> str:
        return f"Border({self.color}, {self.top}, {self.right}, {self.bottom}, {self.left})"

class Padding:
    """Padding class for padding in GUI elements."""
    all: int
    left: int
    right: int
    top: int
    bottom: int
    def __init__(self, *args: int) -> None:
        if len(args) == 1:
            self.all = args[0]
            self.left = args[0]
            self.right = args[0]
            self.top = args[0]
            self.bottom = args[0]

        elif len(args) == 2:
            self.left = args[0]
            self.right = args[0]
            self.top = args[1]
            self.bottom = args[1]

        elif len(args) == 4:
            self.left = args[0]
            self.right = args[1]
            self.top = args[2]
            self.bottom = args[3]

        else: raise ValueError("Padding must have 1, 2, or 4 arguments.")


    @classmethod
    def default(cls) -> "Padding":
        return cls(5, 5, 5, 5)

    def __repr__(self) -> str:
        return f"Padding({self.left}, {self.right}, {self.top}, {self.bottom})"


class Style:
    """A class to represent the style of a button."""
    def __init__(self, colors: Colors = Colors(), border: Border = Border(), padding: int = 5) -> None:
        """Initialize the style with default colors and border."""
        self.colors = colors
        self.border = border
        self.padding = padding

    @classmethod
    def default(cls) -> "Style":
        """Create a default style."""
        return cls(Colors.default(), Border.default())

    def __repr__(self) -> str:
        return f"Style({self.colors}, {self.border})"