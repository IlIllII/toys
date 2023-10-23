import time
import os
from typing import List, Tuple

OFF_CELL = " "
ON_CELL = "O"

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.cells = [[OFF_CELL for x in range(width)] for y in range(height)]
        self.populate_tetronimo()

    def get(self, x: int, y: int) -> str:
        return self.cells[y % len(self.cells)][x % len(self.cells[y % len(self.cells)])]

    def set(self, x: int, y: int, val: str) -> None:
        try:
            self.cells[y % len(self.cells)][
                x % len(self.cells[y % len(self.cells)])
            ] = val
        except:
            raise Exception(f"cell {x}, {y} was not a valid board position")

    def num_surrounding(self, x: int, y: int) -> int:
        count = 0
        for i in [y - 1, y, y + 1]:
            for j in [x - 1, x, x + 1]:
                if i == y and j == x:
                    continue
                elif ON_CELL in self.get(j, i):
                    count += 1
        return count

    def process_step(self) -> None:
        new_cells = []
        for row in self.cells:
            new_cells.append(row.copy())
        for y in range(len(new_cells)):
            for x in range(len(new_cells[y])):
                if ON_CELL in self.get(x, y):
                    surrounding = self.num_surrounding(x, y)
                    valid = [2, 3]
                    if surrounding not in valid:
                        new_cells[y][x] = OFF_CELL
                    else:
                        new_cells[y][x] = "\033[94m" + ON_CELL + "\033[0m"
                if self.get(x, y) == OFF_CELL:
                    surrounding = self.num_surrounding(x, y)
                    if surrounding in [3]:
                        new_cells[y][x] = "\033[91m" + ON_CELL + "\033[0m"
                    else:
                        new_cells[y][x] = OFF_CELL

        self.cells = new_cells

    def populate_tetronimo(self) -> None:
        x = int(len(self.cells[0]) / 2)
        y = int(len(self.cells) / 2)
        self.set(x + 3, y + 2, ON_CELL)
        self.set(x + 3, y + 3, ON_CELL)
        self.set(x + 3, y + 4, ON_CELL)
        self.set(x + 4, y + 5, ON_CELL)
        self.set(x + 5, y + 5, ON_CELL)

    def __repr__(self) -> str:
        s = ""
        for row in range(len(self.cells)):
            for c in self.cells[row]:
                s += c
            s += "\n"
        return s


def get_terminal_dims() -> Tuple[int, int]:
    h, w = os.popen("stty size", "r").read().split()
    width = int(w) - 1
    height = int(h) - 2
    return width, height


if __name__ == "__main__":
    
    board = Board(*get_terminal_dims())
    board.process_step()
    os.system("clear")

    for i in range(500):
        board.process_step()
        print("\033[H")
        print(board, end="", flush=True)
        time.sleep(0.1)
    print(board)
