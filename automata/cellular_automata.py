import pygame


CELL_DIM = 5
INACTIVE_COLOR = (0, 0, 0)
ACTIVE_COLOR = (255, 255, 255)
MANUALLY_PLACED_COLOR = (100, 140, 250)
BOARD_DIMS = (200, 100)


def main():
    pygame.init()
    pygame.display.set_caption("Cellular Automata")
    screen = pygame.display.set_mode(
        (BOARD_DIMS[0] * CELL_DIM, BOARD_DIMS[1] * CELL_DIM)
    )
    board = blank_board(BOARD_DIMS)
    manually_placed_tiles = set()
    main_loop(screen, board, manually_placed_tiles)


def blank_board(board_dimensions):
    board = [
        [0 for x in range(board_dimensions[0])] for y in range(board_dimensions[1])
    ]
    return board


def main_loop(screen, board, manually_placed_tiles):
    while True:
        process_events(board, manually_placed_tiles)
        update_board_state(board, manually_placed_tiles)
        draw_board(screen, board, manually_placed_tiles)
        pygame.display.update()


def process_events(board, manually_placed_tiles):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            board = blank_board(BOARD_DIMS)
            manually_placed_tiles.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = x // CELL_DIM, y // CELL_DIM
            if x < BOARD_DIMS[0] and y < BOARD_DIMS[1]:
                board[y][x] = 1 - board[y][x]
            manually_placed_tiles.symmetric_difference_update({(x, y)})


def update_board_state(board, manually_placed_tiles):
    for y in range(BOARD_DIMS[1] - 1, 0, -1):
        for x in range(1, BOARD_DIMS[0] - 1):
            update_cell_state(board, x, y)
            if (x, y) in manually_placed_tiles:
                board[y][x] = 1


def update_cell_state(board, x, y):
    above_left_alive = board[y - 1][x - 1] == 1
    above_middle_alive = board[y - 1][x] == 1
    above_right_alive = board[y - 1][x + 1] == 1
    res = 0

    if above_left_alive and above_middle_alive and above_right_alive:
        res = 0
    elif above_left_alive and above_middle_alive and not above_right_alive:
        res = 0
    elif above_left_alive and not above_middle_alive and above_right_alive:
        res = 0
    elif not above_left_alive and not above_middle_alive and not above_right_alive:
        res = 0
    else:
        res = 1

    board[y][x] = res


def draw_board(screen, board, manually_placed_tiles):
    for x in range(BOARD_DIMS[0]):
        for y in range(BOARD_DIMS[1]):
            if (x, y) in manually_placed_tiles:
                draw_cell(screen, x, y, MANUALLY_PLACED_COLOR)
            elif board[y][x] == 0:
                draw_cell(screen, x, y, INACTIVE_COLOR)
            else:
                draw_cell(screen, x, y, ACTIVE_COLOR)


def draw_cell(screen, x, y, color):
    pygame.draw.rect(
        screen,
        color,
        (x * CELL_DIM, y * CELL_DIM, CELL_DIM, CELL_DIM),
    )


if __name__ == "__main__":
    main()
