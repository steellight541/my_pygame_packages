import pygame

class Button:
    def __init__(self, rect, color=(200, 200, 200), name=""):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.name = name

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ButtonHandler:
    def __init__(self):
        self.buttons = {}
        self.handlers = {}

    def add(self, button, name):
        """Registers a button with a given name."""
        self.buttons[name] = button

    def easy_connect(self, name, event_type="click"):
        """Decorator for binding functions to button events."""
        def decorator(func):
            self.handlers[(name, event_type)] = func
            return func
        return decorator

    def handle_event(self, event):
        """Handles pygame events and triggers functions if a button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, button in self.buttons.items():
                if button.rect.collidepoint(event.pos):
                    if (name, "click") in self.handlers:
                        self.handlers[(name, "click")]()

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# Create button handler and buttons
bh = ButtonHandler()
btn1 = Button((50, 100, 100, 50), color=(0, 255, 0), name="btn1")
bh.add(btn1, "btn1")

@bh.easy_connect("btn1", "click")
def on_click():
    print("Button clicked!")

running = True
while running:
    screen.fill((30, 30, 30))

    # Draw buttons
    btn1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        bh.handle_event(event)  # Handle button events

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
