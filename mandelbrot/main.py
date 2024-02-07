import pygame
import numpy as np

pygame.init()
width, height = 1200, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mandelbrot Set Visualization")

max_iter = 30
zoom = 1
mandelbrot_shift_x = -0.5
julia_zoom = 1
julia_shift_x = 0
julia_shift_y = 0


def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def julia(c, max_iter, z):
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def xy_to_mandelbrot(x, y):
    return complex(
        3.5 * (x / (width / 2) - 0.5) / zoom + mandelbrot_shift_x,
        2 * (y / height - 0.5) / zoom,
    )


def xy_to_julia(x, y):
    return complex(
        3.5 * ((x - width / 2) / (width / 2) - 0.5) / julia_zoom + julia_shift_x,
        2 * (y / height - 0.5) / julia_zoom + julia_shift_y,
    )


def draw_mandelbrot():
    for x in range(width // 2):
        for y in range(height):
            c = xy_to_mandelbrot(x, y)
            color = mandelbrot(c, max_iter)
            green = int(255 * color / max_iter)
            screen.set_at((x, y), (green, green, 255))


def draw_julia(c):
    for x in range(width // 2, width):
        for y in range(height):
            z = xy_to_julia(x, y)
            color = julia(c, max_iter, z)
            green = int(255 * color / max_iter)
            screen.set_at((x, y), (255, green, green))


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    global max_iter
                    max_iter += 1
                elif event.key == pygame.K_DOWN:
                    max_iter -= 1

        draw_mandelbrot()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_on_mandelbrot = mouse_x < width // 2
        if mouse_on_mandelbrot:
            c = xy_to_mandelbrot(mouse_x, mouse_y)
            draw_julia(c)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
