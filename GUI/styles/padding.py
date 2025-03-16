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