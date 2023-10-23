import time
import os


class Board:
    def __init__(self, width, height) -> None:
        self.cells = [[" " for x in range(width)] for y in range(height)]
        self.populate_tetronimo()

    def get(self, x, y):
        return self.cells[y % len(self.cells)][x % len(self.cells[y % len(self.cells)])]

    def set(self, x, y, val):
        try:
            self.cells[y % len(self.cells)][
                x % len(self.cells[y % len(self.cells)])
            ] = val
        except:
            raise Exception(f"cell {x}, {y} was not a valid board position")

    def num_surrounding(self, x, y):
        count = 0
        for i in [y - 1, y, y + 1]:
            for j in [x - 1, x, x + 1]:
                if i == y and j == x:
                    continue
                elif self.get(j, i) == "O":
                    count += 1
        return count

    def process_step(self):
        new_cells = []
        for row in self.cells:
            new_cells.append(row.copy())
        for y in range(len(new_cells)):
            for x in range(len(new_cells[y])):
                if self.get(x, y) == "O":
                    surrounding = self.num_surrounding(x, y)
                    valid = [2, 3]
                    if surrounding not in valid:
                        new_cells[y][x] = " "
                    else:
                        new_cells[y][x] = "O"
                if self.get(x, y) == " ":
                    surrounding = self.num_surrounding(x, y)
                    if surrounding in [3]:
                        new_cells[y][x] = "O"
                    else:
                        new_cells[y][x] = " "

        self.cells = new_cells

    def populate_tetronimo(self):
        x = int(len(self.cells[0]) / 2)
        y = int(len(self.cells) / 2)
        self.set(x + 3, y + 2, "O")
        self.set(x + 3, y + 3, "O")
        self.set(x + 3, y + 4, "O")
        self.set(x + 4, y + 5, "O")
        self.set(x + 5, y + 5, "O")

    def __repr__(self):
        s = ""
        for row in range(len(self.cells)):
            for c in self.cells[row]:
                s += c
            s += "\n"
        return s


if __name__ == "__main__":
    height, width = os.popen("stty size", "r").read().split()
    width = int(width) - 1
    height = int(height) - 2

    board = Board(width, height)
    board.process_step()
    os.system("clear")

    for i in range(500):
        board.process_step()
        print("\033[H")
        print(board, end="", flush=True)
        time.sleep(0.1)
    print(board)
