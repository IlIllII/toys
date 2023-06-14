import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_POINTS = 8


def random_points(num_points):
    points = []
    for _ in range(num_points):
        points.append(
            (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )
    return points


def random_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        colors.append(
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
    return colors


def naive_voronoi(points, screen):
    colors = random_colors(len(points))
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            closest = None
            closest_distance = float("inf")
            for i, p in enumerate(points):
                distance = (x - p[0]) ** 2 + (y - p[1]) ** 2
                if distance < closest_distance:
                    closest = i
                    closest_distance = distance
            pygame.draw.circle(screen, colors[closest], (x, y), 1)


def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Voronoi Diagram")
    points = random_points(NUM_POINTS)

    running = True
    first = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if first:
            screen.fill((255, 255, 255))
            naive_voronoi(points, screen)
            for p in points:
                pygame.draw.circle(screen, (0, 0, 0), p, 5)
            first = False

        # pygame.draw.circle(screen, (0, 0, 0), pygame.mouse.get_pos(), 5)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
