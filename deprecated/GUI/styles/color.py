class Colors:
    def __init__(self, button:str="cyan", text:str="red", hovered: str="blue", clicked: str="green") -> None:
        self.button = button
        self.text = text
        self.hovered = hovered
        self.clicked = clicked

    @classmethod
    def default(cls) -> "Colors":
        return cls()
    
    @classmethod
    def buttonColors(cls) -> "Colors":
        return cls("cyan", "red", "blue", "green")
    
    def __repr__(self) -> str:
        return str(self.__dict__)