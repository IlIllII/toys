from turtle import color
from numba import njit, prange, jit
import pygame
import numpy as np
import matplotlib.pyplot as plt
from colormaps import ColorMaps

pygame.init()
width, height = 2400, 800
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
            screen.set_at((x, y), (green, green, green))


@njit(parallel=True)
def compute_julia_set(width, height, c, max_iter):
    result = np.zeros((height, width), dtype=np.int32)
    x_span = np.linspace(-2, 2, width)
    y_span = np.linspace(-2, 2, height)

    for i in prange(height):
        for j in range(width):
            z = complex(x_span[j], y_span[i])
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z**2 + c
                n += 1
            result[i, j] = n
    return result


def get_julia_surface(c, width, height, max_iter, color_str):
    julia_data = compute_julia_set(width, height, c, max_iter)
    normalized_data = julia_data / max_iter
    colormap = plt.get_cmap(color_str)
    colored_data = colormap(normalized_data)
    julia_image = (colored_data[:, :, :3] * 255).astype(np.uint8).swapaxes(0, 1)
    return pygame.surfarray.make_surface(julia_image)


def main():
    running = True
    draw_mandelbrot()
    color_maps = ColorMaps()
    while running:
        changed = False
        global max_iter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                changed = True
                if event.key == pygame.K_UP:
                    max_iter += 1
                elif event.key == pygame.K_DOWN:
                    max_iter -= 1
                elif event.key == pygame.K_LEFT:
                    color_maps.previous_map()
                elif event.key == pygame.K_RIGHT:
                    color_maps.next_map()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_on_mandelbrot = mouse_x < width // 2
        if mouse_on_mandelbrot or changed:
            c = xy_to_mandelbrot(mouse_x, mouse_y)
            julia_surface = get_julia_surface(
                c, width // 2, height, max_iter, color_maps.get_map()
            )
            screen.blit(julia_surface, (width // 2, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
