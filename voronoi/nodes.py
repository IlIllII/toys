class Arc:
    def __init__(self, site, circle_event):
        self.site = site
        self.circle_event = circle_event


class BreakPoint:
    def __init__(self, left_point, right_point, edge):
        self.left_point = left_point
        self.right_point = right_point
        self.edge = edge

    def intersects(self):
        return (
            self.left_point != self.right_point and self.left_point < self.right_point
        )

    def intersection(self, sweep_line):
        result = [0, 0]
        p = self.left_point

        if self.left_poinnt[1] == self.right_point[1]:
            result[0] = (self.left_point[0] + self.right_point[0]) / 2
            if self.left_point[0] >= self.right_point[0]:
                result[1] = 0 # Should this be height of pygame?
        elif self.left_point[1] == sweep_line:
            result[0] = self.left_point[0]
            p = self.right_point
        elif self.right_point[1] == sweep_line:
            result[0] = self.right_point[0]
        else:
            # Compute intersection of parabolas
            # Thank you codex!
            a = 1 / (2 * (self.left_point[1] - sweep_line))
            b1 = -2 * self.left_point[0] / (2 * (self.left_point[1] - sweep_line))
            c1 = (self.left_point[0] ** 2 + self.left_point[1] ** 2 - sweep_line ** 2) / (
                2 * (self.left_point[1] - sweep_line)
            )
            b2 = -2 * self.right_point[0] / (2 * (self.right_point[1] - sweep_line))
            c2 = (
                self.right_point[0] ** 2
                + self.right_point[1] ** 2
                - sweep_line ** 2
            ) / (2 * (self.right_point[1] - sweep_line))
            result[0] = (c2 - c1) / (a - b1)
            result[1] = a * result[0] + c1
        
        return result
        a, b = p
        x = result[0]
        u = 2 * (b - 1)
        if u == 0:
            result[1] = 0
        else:
            result[1] = (x ** 2 + a ** 2 - 2 * a * x + b ** 2 - u * sweep_line) / u
        return result

