import time
WIDTH = 50
HEIGHT = 50


class Board:

    def __init__(self) -> None:
        dims = (HEIGHT, WIDTH)
        self.cells = [[" " for x in range(WIDTH)] for y in range(HEIGHT)]
        self.set(3, 2, "O")
        self.set(3, 3, "O")
        self.set(3, 4, "O")
        # self.set(3, 5, "O")
        self.set(4, 5, "O")
        self.set(5, 5, "O")


    def get(self, x, y):
        return self.cells[y % len(self.cells)][x % len(self.cells[y % len(self.cells)])]


    def set(self, x, y, val):
        try:
            self.cells[y % len(self.cells)][x % len(self.cells[y % len(self.cells)])] = val
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

                # new_cells[y][x] = "O" if new_cells[y][(x+1) % len(new_cells[y])] == "O" else " "

        
        self.cells = new_cells


    def __repr__(self):
        s = ""
        for row in range(len(self.cells)):
            for c in self.cells[row]:
                s += c
            s += "\n"
        return s


if __name__ == "__main__":
    board = Board()
    board.process_step()

    for i in range(500):
        board.process_step()
        print(board)
        time.sleep(0.1)
    print(board)
