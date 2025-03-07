from pygame_windows.content import WindowContent
import random
import math


class Bouncingball(WindowContent):
    def __init__(self, num_balls=5):
        super().__init__()
        self.balls = []
        for _ in range(num_balls):
            ball = {
                'x': random.uniform(10, 30),
                'y': random.uniform(10, 30),
                'dx': random.uniform(0.05, 0.15),
                'dy': random.uniform(-0.05, 0.05),
                'radius': 10,
                'gravity': 0.01,
            }
            self.balls.append(ball)

    def _draw(self, screen):
        for i, ball in enumerate(self.balls):
            self.draw_circle(screen, (ball['x'], ball['y']), ball['radius'], (255, 0, 0))
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']
            ball['dy'] += ball['gravity']

            # Check for bounce with walls
            if ball['y'] + ball['radius'] >= self.bounding_box.height:
                ball['y'] = self.bounding_box.height - ball['radius']
                ball['dy'] = -ball['dy'] * 0.8

            # Check for bounce with walls
            if ball['y'] - ball['radius'] <= 0:
                ball['y'] = ball['radius']
                ball['dy'] = -ball['dy']

            # Check for bounce with walls
            if ball['x'] + ball['radius'] >= self.bounding_box.width:
                ball['x'] = self.bounding_box.width - ball['radius']
                ball['dx'] = -ball['dx']

            # Check for bounce with walls
            if ball['x'] - ball['radius'] <= 0:
                ball['x'] = ball['radius']
                ball['dx'] = -ball['dx']

        self.handle_collisions()

    def handle_collisions(self):
        for i, ball1 in enumerate(self.balls):
            for j, ball2 in enumerate(self.balls):
                if i != j:
                    dx = ball2['x'] - ball1['x']
                    dy = ball2['y'] - ball1['y']
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < ball1['radius'] + ball2['radius']:
                        # Simple elastic collision response
                        angle = math.atan2(dy, dx)
                        ball1['dx'], ball2['dx'] = ball2['dx'], ball1['dx']
                        ball1['dy'], ball2['dy'] = ball2['dy'], ball1['dy']
                        overlap = 0.5 * (ball1['radius'] + ball2['radius'] - distance + 1)
                        ball1['x'] -= math.cos(angle) * overlap
                        ball1['y'] -= math.sin(angle)
