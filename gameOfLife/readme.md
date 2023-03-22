# Game of Life

This is game of life in the terminal starting with the `r` tetromino.

![GoL](https://user-images.githubusercontent.com/78166995/157757765-e4fc8eea-511f-4f47-a7fa-e2348f597c29.PNG)

## Getting started

To play the game, run the script:

```bash
py gol.py
```

That should start the game.

You can also pass some command line arguments to change the game. For example to change the cells to `O`s:

```bash
py gol.py O
```

If you want to use tokens that are terminal commands, you can either use quotes like `"&"` or pass the flag `-token=&`.

Additional flags:

```bash
py gol.py -height=50 -width=100 -fps=10
```