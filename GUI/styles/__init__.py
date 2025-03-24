from typing import overload

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
    @overload
    def __init__(self, color: tuple[int, int, int], top: int, right: int, bottom: int, left: int) -> None:
        pass

    @overload
    def __init__(self, color: tuple[int, int, int], top_bottom: int, left_right: int) -> None:
        pass

    @overload
    def __init__(self, color: tuple[int, int, int], width: int) -> None:
        pass

    def __init__(self, color: tuple[int, int, int]|str = (0, 0, 0), *args) -> None: # type: ignore
        """Initialize the border with a color and width."""
        self.color = color
        if len(args) == 1:
            width = args[0]
            self.top = width
            self.right = width
            self.bottom = width
            self.left = width

        elif len(args) == 2:
            top_bottom, left_right = args
            self.top = top_bottom
            self.right = left_right
            self.bottom = top_bottom
            self.left = left_right

        elif len(args) == 4:
            self.top, self.right, self.bottom, self.left = args

        else:
            raise ValueError("Border must have 1, 2, or 4 arguments.")

    @classmethod
    def default(cls) -> "Border":
        """Create a default border."""
        return cls((0,0,0), 1)

    def __repr__(self) -> str:
        return f"Border({self.color}, {self.top}, {self.right}, {self.bottom}, {self.left})"

class Padding:
    """Padding class for padding in GUI elements."""
    left: int
    right: int
    top: int
    bottom: int
    def __init__(self, *args: int) -> None:
        if len(args) == 1:
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

        else: 
            raise ValueError("Padding must have 1, 2, or 4 arguments.")

    @classmethod
    def default(cls) -> "Padding":
        return cls(5, 5, 5, 5)

    def __repr__(self) -> str:
        return f"Padding({self.left}, {self.right}, {self.top}, {self.bottom})"

class Style:
    """A class to represent the style of a button."""
    def __init__(self, colors: Colors = Colors(), border: Border = Border.default(), padding: Padding = Padding.default()) -> None:
        """Initialize the style with default colors, border, and padding."""
        self.colors = colors
        self.border = border
        self.padding = padding

    @classmethod
    def default(cls) -> "Style":
        """Create a default style."""
        return cls(Colors.default(), Border.default(), Padding.default())

    def __repr__(self) -> str:
        return f"Style({self.colors}, {self.border}, {self.padding})"