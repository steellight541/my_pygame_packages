from GUI import *
import pygame

class MyApp:
    def __init__(self):
        self.gui = GUIHandler()
        self.button_1 = Button(
            surface=pygame.Surface((100, 50)),
            rect=pygame.Rect(100, 100, 100, 50),
            text="Click me!",
            style=Style.default(),
            tooltip=Tooltip("center", "this is a tooltip"),
        )
        self.gui.add_button(self.button_1)
        self.gui.auto_connect(self)

    @auto_connect("button_1", Button.BehaviorTypes.DOUBLE)
    def on_button_1_double(self, button):
        print("Double-click detected!")


screen = pygame.display.set_mode((800,600))
app = MyApp()

@app.gui.connect(app.button_1, Button.BehaviorTypes.SINGLE)
def on_button_1_single(button):
    print("Single-click detected!")

while True:
    screen.fill((255, 255, 255))
    app.gui.draw(screen)
    pygame.display.flip()
    app.gui.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        app.gui.handle_event(event)