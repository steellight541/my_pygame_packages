from pygame_windows.content import WindowContent

class Bouncingball(WindowContent):
    # this is a subclass of WindowContent to demonstrate how to create a custom content class
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 20
        self.dx = 0.1
        self.dy = 0
        self.gravity = 0.01

    def _draw(self, screen):
        self.draw_circle(screen, (self.x, self.y), 10, (255, 0, 0))
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity

        # Check for bounce
        if self.y + 10 >= self.bounding_box.height:
            self.y = self.bounding_box.height - 10
            self.dy = -self.dy * 0.8  # Reverse direction and reduce speed

        # if it hits the top, reverse direction
        if self.y - 10 <= 0:
            self.y = 9

        # Reset bounce if speed is very low
        if abs(self.dy) < 0.1 and self.y + 10 >= self.bounding_box.height:
            import random
            self.dy = random.uniform(-5, 1)

        if self.x + 10 >= self.bounding_box.width:
            self.x = self.bounding_box.width - 10
            self.dx = -self.dx

        if self.x - 10 <= 0:
            self.x = 10
            self.dx = -self.dx