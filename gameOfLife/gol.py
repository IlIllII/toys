import sys
import time


width = 90
height = 45
fps = 10
token = "."

if len(sys.argv) > 1:
    args = sys.argv[1:]
    if len(args[0]) == 1:
        token = args[0]

    for arg in args:
        if len(arg) > 1:
            try:
                flag, val = arg.split("=")
                if flag == "-height" and val.isdigit():
                    height = int(val)
                if flag == "-width" and val.isdigit():
                    width = int(val)
                if flag == "-fps" and val.isdigit():
                    fps = int(val)
                if flag == "-token" and len(val) == 1:
                    token = val
            except:
                print("Arguments should be of the form: '-flag=value'")
                exit(0)


class Board:
    def __init__(self) -> None:
        self.board = [[" " for _ in range(width)] for _ in range(height)]

        # Setting an "r" tetromino to start
        self.board[height // 2][width // 2] = token
        self.board[height // 2 - 1][width // 2 + 1] = token
        self.board[height // 2 - 1][width // 2 + 2] = token
        self.board[height // 2 + 1][width // 2] = token
        self.board[height // 2 + 2][width // 2] = token

    def create_new_board(self):
        new_board = [[" " for _ in range(width)] for _ in range(height)]
        return new_board

    def __repr__(self) -> str:
        s = ""
        for row in self.board:
            s = s + ("".join(row)) + "\n"
        return s

    def update(self):
        new_board = self.create_new_board()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.update_cell(i, j, new_board)

        self.board = new_board

    def update_cell(self, i, j, new_board):
        live = self.board[i][j] == token
        total = 0
        for k in range(-1, 2):
            for n in range(-1, 2):
                idx1 = (i + k) % height
                idx2 = (j + n) % width
                if self.board[idx1][idx2] == token and not (idx1 == i and idx2 == j):
                    total += 1

        if live:
            if total < 2:
                new_board[i][j] = " "
            elif total == 2 or total == 3:
                new_board[i][j] = token
            else:
                new_board[i][j] = " "
        elif total == 3:
            new_board[i][j] = token


if __name__ == "__main__":
    b = Board()
    print(f"\033[8;{height + 1};{width + 1}t")  # Resizing terminal window

    while True:
        print(b, end="\033[A" * height, flush=True)  # Move up to top after each print
        b.update()
        time.sleep(1 / fps)