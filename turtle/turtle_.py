import turtle


def set_turtle_properties():
    turt.speed(0)
    turt.pencolor("gray")
    turt.pensize(2)
    turt.fillcolor("white")


def move_forward():
    turt.forward(5)


def move_backward():
    turt.backward(5)


def turn_left():
    turt.left(5)


def turn_right():
    turt.right(5)


def pen_toggle():
    if turt.isdown():
        turt.penup()
    else:
        turt.pendown()


def clear():
    ts.resetscreen()
    set_turtle_properties()


def print_instructions():
    print("Controls:")
    print("  Up: Move pen forward")
    print("  Down: Move pen backward")
    print("  Left: Rotate left 5 degrees")
    print("  Right: Rotate right 5 degrees")
    print("  C: Clear screen")
    print("  Space: Pick up/put down pen tip", flush=True)


if __name__ == "__main__":
    turt = turtle.Turtle()
    ts = turt.getscreen()
    ts.listen()

    # Register key listeners
    keys = ["Up", "Down", "Left", "Right", "space", "c"]
    funcs = [move_forward, move_backward, turn_left, turn_right, pen_toggle, clear]
    for i, key in enumerate(keys):
        ts.onkeypress(funcs[i], key)

    # Start program
    print_instructions()
    set_turtle_properties()
    turtle.mainloop()