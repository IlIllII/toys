import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_POINTS = 10


def random_points(num_points):
    points = []
    for _ in range(num_points):
        points.append(
            (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )
    return points


def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Voronoi Diagram")
    points = random_points(NUM_POINTS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        for p in points:
            pygame.draw.circle(screen, (0, 0, 0), p, 5)
        pygame.draw.circle(screen, (0, 0, 0), pygame.mouse.get_pos(), 5)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
