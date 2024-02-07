from numba import njit, prange
import pygame
import numpy as np
import matplotlib.pyplot as plt

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
    julia_width, julia_height = 600, 400
    x = np.linspace(-2, 2, julia_width)
    y = np.linspace(-1, 1, julia_height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = np.full(Z.shape, c)
    iterations = np.zeros(Z.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask] ** 2 + C[mask]
        iterations[mask] = i
    iterations[iterations == max_iter] = 0

    iterations = iterations / max_iter
    surface = pygame.surfarray.make_surface(
        (plt.cm.viridis(iterations)[:, :, :3] * 255).swapaxes(0, 1)
    )
    screen.blit(surface, (600, 0))


def main():
    running = True
    draw_mandelbrot()
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

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_on_mandelbrot = mouse_x < width // 2
        if mouse_on_mandelbrot:
            c = xy_to_mandelbrot(mouse_x, mouse_y)
            draw_julia(c)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
