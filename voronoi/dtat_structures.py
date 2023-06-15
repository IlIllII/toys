from queue import PriorityQueue
from events import SiteEvent, CircleEvent

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Voronoi Diagram")

points = [(300, 300), (600, 600), (600, 200), (120, 100)]

sweep_line = 0

cells = dict()
event_queue = PriorityQueue()
for p in points:
    event_queue.put((p[1], SiteEvent(p[0], p[1])))

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return f"Vertex({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y
    

class Edge:
    def __init__(self):
        self.left_site = None
        self.right_site = None
        self.start = None
        self.end = None


class Cell:
    def __init__(self):
        self.site = None
        self.half_edges = []

for p in points:
    cells[p] = set()


class HalfEdge:
    def __init__(self):
        self.site = None
        self.edge = None
    
    def get_start(self):
        return self.edge.start
    
    def get_end(self):
        return self.edge.end


class Node:
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None
        self.parent = None
    
    def get_x(self):
        return self.value.x

class Arc(Node):
    def __init__(self, site):
        super().__init__()
        self.site = site
        self.circle_events = []

class BreakPoint(Node):
    def __init__(self, edge=None):
        super().__init__()
        self.edge = edge
        self.left_site = None
        self.right_site = None
    
    def get_x(self):
        # solve parabola intersection for left_site and right_site
        # use directrix formula
        # y = 1 / (2 * (yf - yd)) * (x - xf)^2 + (yf + yd) / 2
        return self.get_intersection()[0]

    def get_intersection(self):
        result = [0, 0]
        p = self.left_site

        if self.left_site[1] == self.right_site[1]:
            result[0] = (self.left_site[0] + self.right_site[0]) / 2
            if self.left_site[0] >= self.right_site[0]:
                result[1] = 0 # Should this be height of pygame?
        elif self.left_site[1] == sweep_line:
            result[0] = self.left_site[0]
            p = self.right_site
        elif self.right_site[1] == sweep_line:
            result[0] = self.right_site[0]
        else:
            # Compute intersection of parabolas
            # Thank you codex!
            a = 1 / (2 * (self.left_site[1] - sweep_line))
            b1 = -2 * self.left_site[0] / (2 * (self.left_site[1] - sweep_line))
            c1 = (self.left_site[0] ** 2 + self.left_site[1] ** 2 - sweep_line ** 2) / (
                2 * (self.left_site[1] - sweep_line)
            )
            b2 = -2 * self.right_site[0] / (2 * (self.right_site[1] - sweep_line))
            c2 = (
                self.right_site[0] ** 2
                + self.right_site[1] ** 2
                - sweep_line ** 2
            ) / (2 * (self.right_site[1] - sweep_line))
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
        

class BinaryTree:
    def __init__(self):
        self.root = None

    def find_arc(self, x):
        node = self.root
        while node.__class__ == BreakPoint:
            if x < node.get_x():
                node = node.left
            else:
                node = node.right
        return node

    def split_arc(self, arc, new_site):
        if arc.site[0] <= new_site[0]:
            breakpoint = BreakPoint()
            breakpoint.left_site = arc.site
            breakpoint.right_site = new_site
            if not arc.parent:
                breakpoint.parent = arc.parent
            elif arc.parent.left == arc:
                breakpoint.parent = arc.parent
                arc.parent.left = breakpoint
            else:
                breakpoint.parent = arc.parent
                arc.parent.right = breakpoint
            arc.parent = breakpoint
            breakpoint.left = arc
            sub_breakpoint = BreakPoint()
            sub_breakpoint.left_site = new_site
            sub_breakpoint.right_site = arc.site
            sub_breakpoint.parent = breakpoint
            breakpoint.right = sub_breakpoint
            left_arc = Arc(new_site)
            left_arc.parent = sub_breakpoint
            sub_breakpoint.left = left_arc
            right_arc = Arc(arc.site)
            right_arc.parent = sub_breakpoint
            sub_breakpoint.right = right_arc
        else:
            breakpoint = BreakPoint()
            breakpoint.left_site = new_site
            breakpoint.right_site = arc.site
            if not arc.parent:
                breakpoint.parent = arc.parent
            elif arc.parent.left == arc:
                breakpoint.parent = arc.parent
                arc.parent.left = breakpoint
            else:
                breakpoint.parent = arc.parent
                arc.parent.right = breakpoint
            arc.parent = breakpoint
            breakpoint.left = arc
            sub_breakpoint = BreakPoint()
            sub_breakpoint.left_site = arc.site
            sub_breakpoint.right_site = new_site
            sub_breakpoint.parent = breakpoint
            breakpoint.right = sub_breakpoint
            left_arc = Arc(arc.site)
            left_arc.parent = sub_breakpoint
            sub_breakpoint.left = left_arc
            right_arc = Arc(new_site)
            right_arc.parent = sub_breakpoint
            sub_breakpoint.right = right_arc
        
        assert breakpoint.left.parent == breakpoint
        assert breakpoint.right.parent == breakpoint
        assert sub_breakpoint.left.parent == sub_breakpoint
        assert sub_breakpoint.right.parent == sub_breakpoint

        if breakpoint.parent:
            assert breakpoint.parent.left == breakpoint or breakpoint.parent.right == breakpoint

        if breakpoint.parent == None:
            self.root = breakpoint
        
        current = breakpoint
        while current.parent:
            current = current.parent
            
        # Add edge starts to cell table and vertex table? Could also do this when we finish...
        breakpoint.edge = HalfEdge()
        breakpoint.edge.start = [arc.site[0] + new_site[0] / 2, arc.site[1] + new_site[1] / 2]
        sub_breakpoint.edge = HalfEdge()
        sub_breakpoint.edge.start = [arc.site[0] + new_site[0] / 2, arc.site[1] + new_site[1] / 2]
        self.scan_for_circle_events()
    
    def get_arcs(self):
        arcs = []
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            if node.__class__ == Arc:
                arcs.append(node)
            else:
                queue.insert(0, node.left)
                queue.append(node.right)
        return arcs

    def scan_for_circle_events(self):
        arcs = self.get_arcs()
        for i, arc in enumerate(arcs):
            try:
                left_arc = arcs[i - 1]
                middle_arc = arc
                right_arc = arcs[i + 1]
            except IndexError:
                continue
            if middle_arc.site[1] >= left_arc.site[1] and middle_arc.site[1] >= right_arc.site[1]:
                continue
            else:
                event = create_circle_event(left_arc, middle_arc, right_arc)
                for arc in [left_arc, middle_arc, right_arc]:
                    if len(arc.circle_events) == 0:
                        arc.circle_events = []
                    arc.circle_events.append(event)
                if event:
                    pygame.draw.circle(screen, (255, 255, 255), (int(event.x), int(event.y)), int(event.radius), 1)
                    pygame.draw.circle(screen, (255, 255, 255), (int(event.x), int(event.y)), 1)
                    # pygame.draw.triangle(screen, (255, 255, 255), event.get_triangle())
                    pygame.draw.lines(screen, (255, 255, 255), True, event.get_triangle())
                    for i, point in enumerate(event.points):
                        pygame.draw.line(
                            screen, (255, 255, 255),
                            (int(event.x), int(event.y)),
                            (int((point[0] + points[(i+1)%len(points)][0]) / 2), int((point[1] + points[(i+1)%len(points)][1]) / 2))
                        )

                    get_event_queue().put((event.get_tangent_point()[1], event))
    
    def remove_arc(self, x):
        arc = self.find_arc(x)
        parent = arc.parent
        if parent.left == arc:
            sibling = parent.right
        else:
            sibling = parent.left

        new_breakpoint = BreakPoint()
        grandparent = parent.parent
        great_grandparent = grandparent.parent
        if great_grandparent:
            if great_grandparent.left == grandparent:
                great_grandparent.left = new_breakpoint
            else:
                great_grandparent.right = new_breakpoint
        new_breakpoint.parent = great_grandparent

        if grandparent.left == parent:
            new_breakpoint.left = sibling
            sibling.parent = new_breakpoint
            new_breakpoint.right = grandparent.right
            grandparent.right.parent = new_breakpoint
        else:
            new_breakpoint.right = sibling
            sibling.parent = new_breakpoint
            new_breakpoint.left = grandparent.left
            grandparent.left.parent = new_breakpoint
        
        left_child = new_breakpoint.left
        right_child = new_breakpoint.right
        if left_child.__class__ == Arc:
            new_breakpoint.left_site = left_child.site
        else:
            new_breakpoint.left_site = left_child.right_site
        if right_child.__class__ == Arc:
            new_breakpoint.right_site = right_child.site
        else:
            new_breakpoint.right_site = right_child.left_site
    
    def print_tree(self, node, indent=0):
        if node:
            print(" " * indent + str(node))
            self.print_tree(node.left, indent + 2)
            self.print_tree(node.right, indent + 2)
        

        





class CellTable:
    def __init__(self):
        self.cells = {}
    
    def add_cell(self, site, half_edge):
        self.cells[site] = half_edge
    
    def get_cell(self, site):
        return self.cells[site]

class VertextTable:
    def __init__(self):
        self.vertices = {}
    
    def add_half_edge(self, vertex, half_edge):
        if vertex in self.vertices:
            self.vertices[vertex].append(half_edge)
        else:
            self.vertices[vertex] = [half_edge]
    
    def get_half_edges(self, vertex):
        return self.vertices[vertex]

class EdgeNode:
    def __init__(self):
        self.start = None
        self.end = None
        self.prev_half_edge = None
        self.next_half_edge = None
        self.twin = None
        self.cell = None


def get_sweep_line():
    return sweep_line

def get_event_queue():
    return event_queue

def create_circle_event(left, middle, right):
    if not left or not right or not middle:
        return None

    p0, p1, p2 = left.site, middle.site, right.site
    circle = circumcircle(p0, p1, p2)
    if not circle or circle[1] + circle[2] < get_sweep_line():
        return None
    x, y, radius = circle
    return CircleEvent(
        x,
        y,
        radius,
        middle,
        [p0, p1, p2],
        [left, middle, right],
    )


def circumcircle(p0, p1, p2):
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2
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

def scan_and_remove_circle_events(event_queue, site_position):
    for i, event in enumerate(event_queue.queue):
        event = event[1]
        if event.__class__ == CircleEvent:
            circle_center = (event.x, event.y)
            circle_radius = event.radius
            distance = ((site_position[0] - circle_center[0]) ** 2 + (site_position[1] - circle_center[1]) ** 2) ** (1 / 2)
            if distance < circle_radius:
                event_queue.queue.pop(i)

voronoi_vertices = []

def process_site_event(event, binary_tree: BinaryTree):
    # Find arc above site
    arc = binary_tree.find_arc(event.x)
    cells[(arc.site[0], arc.site[1])].add((event.x + arc.site[0] / 2, event.y + arc.site[1] / 2))
    # Split arc
    binary_tree.split_arc(arc, event.site)
    # Scan for circle events
    scan_and_remove_circle_events(get_event_queue(), (event.x, event.y))

def process_circle_event(event, binary_tree):
    event_pos = event.get_tangent_point()
    pygame.draw.circle(screen, (255, 255, 255), (event.x, event.y), int(event.radius), 1)
    voronoi_vertices.append(event_pos)
    binary_tree.remove_arc(event.arc_node.site[0])


# points = [(0, 0), (1, 1), (2, 2), (3, 3)]


# for p in points:
#     event_queue.put(SiteEvent(p[0], p[1]))

binary_tree = BinaryTree()



while event_queue.qsize() > 0:
    event = event_queue.get()
    event = event[1]
    sweep_line = event.y
    if event.__class__ == SiteEvent:
        if binary_tree.root is None:
            binary_tree.root = Arc(event.site)
        else:
            process_site_event(event, binary_tree)
    elif event.__class__ == CircleEvent:
        process_circle_event(event, binary_tree)

sorted_arcs = sorted(binary_tree.get_arcs(), key=lambda arc: arc.site[0])

if __name__ == "__main__":

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for vertex in voronoi_vertices:
            v = (int(vertex[0]), int(vertex[1]))
            pygame.draw.circle(screen, (0, 255, 0), v, 5)
        for p in points:
            pp = (int(p[0]), int(p[1]))
            pygame.draw.circle(screen, (255, 0, 0), pp, 5)
        
        for points_ in cells.values():
            for p in points_:
                pygame.draw.circle(screen, (50, 50, 255), (int(p[0]), int(p[1])), 3)
        pygame.display.flip()