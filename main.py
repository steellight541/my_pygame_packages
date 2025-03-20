from GUI import *
import pygame
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    button = Button.from_surface(pygame.Surface((100, 50)),(100,100), text="Click Me!")
    button.style.colors.button = "blue"
    button.style.colors.hovered = "red"
    button.style.colors.text = "white"
    button.tooltip = Tooltip("center", "This is a button!")
    while True:
        screen.fill("white")
        button.update()
        button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.clicked:
                    print("Button Clicked!")

if __name__ == "__main__":
    main()