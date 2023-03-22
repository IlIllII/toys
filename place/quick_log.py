debug = False

def log(s) -> None:
    """Print a message to stdout if quicklog.debug is true."""
    if debug:
        print(s, flush=True)