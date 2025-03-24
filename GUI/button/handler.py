from GUI.button import Button
from typing import Callable, Dict, Set
import pygame
import time


class ButtonHandler:
    """A class to manage multiple buttons and their listeners."""
    DOUBLE_CLICK_TIME = 0.300

    def __init__(self) -> None:
        self._buttons: Set[Button] = set()
        self._listeners: Dict[str, Dict[Button, Set[Callable[[Button], None]]]] = {
            "single": {},
            "double": {},
            "hover": {}
        }
        self._last_click_times: Dict[Button, float] = {}
        self._to_be_processed: Dict[Button, Button.BehaviorTypes] = {}

    def add_button(self, button: Button) -> None:
        """Add a button to the handler."""
        self._buttons.add(button)

    def remove_button(self, button: Button) -> None:
        """Remove a button from the handler."""
        self._buttons.discard(button)
        for behavior in self._listeners.values():
            behavior.pop(button, None)

    def add_listener(self, button: Button, listener: Callable[[Button], None], behavior: Button.BehaviorTypes) -> None:
        """Attach a listener to a button for a specific behavior."""
        behavior_key = behavior.name.lower()
        if behavior_key not in self._listeners:
            raise ValueError(f"Unsupported behavior type: {behavior}")
        if button not in self._listeners[behavior_key]:
            self._listeners[behavior_key][button] = set()
        self._listeners[behavior_key][button].add(listener)

    def remove_listener(self, button: Button, listener: Callable[[Button], None], behavior: Button.BehaviorTypes) -> None:
        """Remove a listener from a button for a specific behavior."""
        behavior_key = behavior.name.lower()
        if behavior_key in self._listeners and button in self._listeners[behavior_key]:
            self._listeners[behavior_key][button].discard(listener)
            if not self._listeners[behavior_key][button]:
                del self._listeners[behavior_key][button]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all buttons on the given surface."""
        for button in self._buttons:
            button.draw(surface)


    def update(self) -> None:
        """Update all buttons."""
        for button in self._buttons:
            button.update()

        self.process_clicks()

    def _handle_click(self, event: pygame.event.Event) -> None:
        """Handle single and double-click events."""
        for button in self._buttons:
            if not button.hovered: continue
            current_time = time.time()
            is_double_click = button in self._last_click_times and current_time - self._last_click_times[button] < self.DOUBLE_CLICK_TIME
            self._handle_double_click(button) if is_double_click else self._schedule_single_click(button, current_time)


    def _schedule_single_click(self, button, current_time):
        self._last_click_times[button] = current_time
        pygame.time.set_timer(pygame.USEREVENT + 1, int(self.DOUBLE_CLICK_TIME * 1000), True)

    def _handle_double_click(self, button):
        self._to_be_processed[button] = Button.BehaviorTypes.DOUBLE
        self._last_click_times.pop(button, None)

    def process_clicks(self) -> None:
        """Process the clicks stored in the to-be-processed dictionary."""
        [listener(button) for button, behavior in self._to_be_processed.items() for listener in self._listeners.get(behavior.name.lower(), {}).get(button, [])]
        self._to_be_processed.clear()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse events and trigger listeners."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_hover()
        elif event.type == pygame.USEREVENT + 1:
            # Handle delayed single-click detection
            for button, last_click_time in self._last_click_times.copy().items():
                if time.time() - last_click_time >= self.DOUBLE_CLICK_TIME:
                    self._to_be_processed[button] = Button.BehaviorTypes.SINGLE
                    self._last_click_times.pop(button, None)

    def _handle_hover(self) -> None:
        """Handle hover events."""
        [listener(button) for button in self._buttons for listener in self._listeners["hover"].get(button, []) if button.hovered]

    #decorator for adding listeners
    def connect(self, behavior: Button.BehaviorTypes, button: Button):
        """
        Decorator to add a listener to a button for a specific behavior.

        usage:
        @button_handler.connect(Button.BehaviorTypes.SINGLE_CLICK, button)
        def listener(button: Button):
            pass
        """
        def decorator(listener):
            self.add_listener(button, listener, behavior)
            return listener
        return decorator