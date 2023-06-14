class Event:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


class SiteEvent(Event):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __repr__(self):
        return f"SiteEvent({self.x}, {self.y})"


class CircleEvent(Event):
    def __init__(self, x, y, radius, arc_node, points, arcs):
        super().__init__(x, y)
        self.radius = radius
        self.arc_node = arc_node
        self.points = points
        self.arcs = arcs

    def __repr__(self):
        return f"CircleEvent({self.x}, {self.y}, {self.p}, {self.ycenter})"

    def get_triangle(self):
        return (
            self.points[0].position(),
            self.points[1].position(),
            self.points[2].position(),
        )


def create_circle_event(left, middle, right, sweep_line):
    if not left or not right or not middle:
        return None

    p0, p1, p2 = left.value().p, middle.value().p, right.value().p
    circle = circumcircle(p0, p1, p2)
    if not circle or circle[1] + circle[2] < sweep_line:
        return None
    x, y, radius = circle
    return CircleEvent(
        x,
        y,
        radius,
        middle,
        [p0, p1, p2],
        [left.value(), middle.value(), right.value()],
    )


def circumcircle(p0, p1, p2):
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2
    print(d)
    if d == 0:
        return None
    x = (
        (ax**2 + ay**2) * (by - cy)
        + (bx**2 + by**2) * (cy - ay)
        + (cx**2 + cy**2) * (ay - by)
    ) / d
    y = (
        (ax**2 + ay**2) * (cx - bx)
        + (bx**2 + by**2) * (ax - cx)
        + (cx**2 + cy**2) * (bx - ax)
    ) / d
    radius = ((ax - x) ** 2 + (ay - y) ** 2) ** (1 / 2)
    return x, y, radius
