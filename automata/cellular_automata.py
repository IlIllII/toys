from multiprocessing import process
import pygame

CELL_DIM = 10
INACTIVE_COLOR = (0, 0, 0)
ACTIVE_COLOR = (255, 255, 255)
MANUALLY_PLACED_COLOR = (100, 140, 250)
BOARD_DIM = (100, 100)


def process_cell(board, i, j):
    left = board[i - 1][j - 1] == 1
    middle = board[i][j - 1] == 1
    right = board[i + 1][j - 1] == 1

    if left and middle and right:
        return 0
    elif left and middle and not right:
        return 0
    elif left and not middle and right:
        return 0
    elif not left and not middle and not right:
        return 0
    else:
        return 1


def update_board_state(board, manually_placed_tiles):
    for i in range(BOARD_DIM[1]):
        for j in range(BOARD_DIM[0]):
            if i == 0 or j == 0 or i == BOARD_DIM[0] - 1 or j == BOARD_DIM[1] - 1:
                continue
            else:
                board[i][j] = process_cell(board, i, j)
                if (i, j) in manually_placed_tiles:
                    board[i][j] = 1


def draw_cell(screen, i, j, color):
    pygame.draw.rect(
        screen,
        color,
        (i * CELL_DIM, j * CELL_DIM, CELL_DIM, CELL_DIM),
    )


def draw_board(screen, board, manually_placed_tiles):
    for i in range(BOARD_DIM[1]):
        for j in range(BOARD_DIM[0]):
            if (i, j) in manually_placed_tiles:
                draw_cell(screen, i, j, MANUALLY_PLACED_COLOR)
            elif board[i][j] == 0:
                draw_cell(screen, i, j, INACTIVE_COLOR)
            else:
                draw_cell(screen, i, j, ACTIVE_COLOR)


def process_events(board, manually_placed_tiles):
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            board = [[0 for i in range(BOARD_DIM[0])] for j in range(BOARD_DIM[1])]
            manually_placed_tiles.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // CELL_DIM
            y = y // CELL_DIM
            board[x][y] = 1 - board[x][y]
            if (x, y) in manually_placed_tiles:
                manually_placed_tiles.remove((x, y))
            else:
                manually_placed_tiles.add((x, y))


def main_loop(screen, board, manually_placed_tiles):
    while True:
        process_events(board, manually_placed_tiles)
        update_board_state(board, manually_placed_tiles)
        draw_board(screen, board, manually_placed_tiles)
        pygame.display.update()


def main():
    pygame.init()

    screen = pygame.display.set_mode((BOARD_DIM[0] * CELL_DIM, BOARD_DIM[1] * CELL_DIM))
    board = [[0 for i in range(BOARD_DIM[0])] for j in range(BOARD_DIM[1])]
    manually_placed_tiles = set()

    main_loop(screen, board, manually_placed_tiles)


if __name__ == "__main__":
    main()
