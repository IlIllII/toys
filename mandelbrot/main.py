from numba import njit, prange  # type: ignore
import pygame
import numpy as np
import matplotlib.pyplot as plt
from colormaps import ColorMaps
from util import resize_for_aspect_ratio

pygame.init()


info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
aspect_ratio = 2
width, height = resize_for_aspect_ratio(screen_width, screen_height, aspect_ratio)
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("Mandelbrot Set Visualization")

max_iter = 30
zoom = 1
mandelbrot_shift_x = -0.5
julia_zoom = 1
julia_shift_x = 0
julia_shift_y = 0


def mandelbrot(c: complex, max_iter: int) -> int:
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def julia(c: complex, max_iter: int, z: complex) -> int:
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def xy_to_mandelbrot(x: int, y: int) -> complex:
    centering_offset = 0.5
    return complex(
        3 * (x / (width / 2) - centering_offset) / zoom + mandelbrot_shift_x,
        3 * (y / height - centering_offset) / zoom,
    )


def xy_to_julia(x: int, y: int) -> complex:
    centering_offset = 0.5
    return complex(
        3.5 * ((x - width / 2) / (width / 2) - centering_offset) / julia_zoom
        + julia_shift_x,
        2 * (y / height - centering_offset) / julia_zoom + julia_shift_y,
    )


def draw_mandelbrot() -> pygame.Surface:
    surface = pygame.Surface((width // 2, height))
    for x in range(width // 2):
        for y in range(height):
            c = xy_to_mandelbrot(x, y)
            color = mandelbrot(c, max_iter)
            gray_scale = int(255 * color / max_iter)
            surface.set_at((x, y), (gray_scale, gray_scale, gray_scale))
    return surface


@njit(parallel=True)
def compute_julia_set(width: int, height: int, c: complex, max_iter: int) -> np.ndarray:
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


def get_julia_surface(
    c: complex, width: int, height: int, max_iter: int, color_str: str
) -> pygame.Surface:
    julia_data = compute_julia_set(width, height, c, max_iter)
    normalized_data = julia_data / max_iter
    colormap = plt.get_cmap(color_str)
    colored_data = colormap(normalized_data)
    julia_image = (colored_data[:, :, :3] * 255).astype(np.uint8).swapaxes(0, 1)
    return pygame.surfarray.make_surface(julia_image)


def get_label_surface(
    text: str, font_size: int, color: tuple[int, int, int]
) -> pygame.Surface:
    font = pygame.font.Font(None, font_size)
    return font.render(text, True, color)


def draw_info_panel(screen: pygame.Surface, color_maps: ColorMaps) -> None:
    padding = 10
    font_height = 50
    white = (255, 255, 255)
    black = (0, 0, 0)
    iter_text = get_label_surface(f"Max Iterations: {max_iter}", font_height, white)
    color_text = get_label_surface(f"Color: {color_maps.get_map()}", font_height, white)
    max_width = max(iter_text.get_width(), color_text.get_width())
    max_height = color_text.get_height() + iter_text.get_height() + padding * 2

    for border_width, color in enumerate([black, white]):
        pygame.draw.rect(
            screen,
            color,
            (padding, padding, max_width + padding * 2, max_height),
            width=border_width,
        )
    screen.blit(iter_text, (padding * 2, padding * 2))
    screen.blit(color_text, (padding * 2, max_height - color_text.get_height()))


def adjusted_max_iter(
    current_fps: float, max_iter: int, prev_mouse_pos: tuple[int, int]
) -> int:
    target_fps = 10
    fps_difference = target_fps - current_fps
    mouse_move_delta = abs(prev_mouse_pos[0] - pygame.mouse.get_pos()[0]) + abs(
        prev_mouse_pos[1] - pygame.mouse.get_pos()[1]
    )

    mouse_sensitivity = 1 if mouse_move_delta < 5 else -2
    if fps_difference > 0:
        max_iter -= int(min(2, fps_difference / 5) * mouse_sensitivity)
    elif fps_difference < 0:
        max_iter += int(1 * mouse_sensitivity)

    max_iter = max(30, min(max_iter, 200))
    return max_iter


def handle_pygame_events(
    color_maps: ColorMaps, running: bool, changed: bool
) -> tuple[bool, bool]:
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
    return running, changed


def main():
    running = True
    mandelbrot_surface = draw_mandelbrot()
    color_maps = ColorMaps()
    prev_mouse_pos = pygame.mouse.get_pos()
    frame_time = 0
    while running:
        changed = False

        global max_iter
        current_fps = 1000 / (pygame.time.get_ticks() - frame_time)
        max_iter = adjusted_max_iter(current_fps, max_iter, prev_mouse_pos)
        frame_time = pygame.time.get_ticks()
        prev_mouse_pos = pygame.mouse.get_pos()

        running, changed = handle_pygame_events(color_maps, running, changed)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_on_mandelbrot = mouse_x < width // 2
        if mouse_on_mandelbrot or changed:
            c = xy_to_mandelbrot(mouse_x, mouse_y)
            julia_surface = get_julia_surface(
                c, width // 2, height, max_iter, color_maps.get_map()
            )
            screen.blit(julia_surface, (width // 2, 0))

        screen.blit(mandelbrot_surface, (0, 0))

        draw_info_panel(screen, color_maps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
