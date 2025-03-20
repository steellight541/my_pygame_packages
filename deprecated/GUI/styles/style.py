from .padding import Padding
from .border import Border
from .color import Colors

class Style:
    colors: Colors
    padding: Padding
    border: Border

    def __init__(self, colors: Colors = Colors.default(), padding: Padding = Padding.default(), border: Border = Border.default()):
        self.colors = colors
        self.padding = padding
        self.border = border

    def __repr__(self) -> str:
        return str(self.__dict__)