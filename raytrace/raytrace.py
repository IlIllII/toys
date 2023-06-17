import pygame

import pygame

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def normalized(self):
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def mult(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)


class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color


    def intersect(self, ray):
        line_to_sphere = self.center - ray.origin
        dp = line_to_sphere.dot(ray.direction)
        if dp < 0: # Ray points away from sphere
            return False
        d_squared = line_to_sphere.dot(line_to_sphere) - dp * dp
        if d_squared > self.radius * self.radius:
            return False
        d = (self.radius * self.radius - d_squared) ** 0.5
        near_intersect = dp - d
        far_intersect = dp + d
        return near_intersect, far_intersect
    

    def get_normal(self, point):
        return Vector3(point.x - self.center.x, point.y - self.center.y, point.z - self.center.z).normalized()

class Light(Sphere):
    def __init__(self, center, radius, color):
        super().__init__(center, radius, color)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
    
    def get_point(self, t):
        x = self.origin.x + self.direction.x * t
        y = self.origin.y + self.direction.y * t
        z = self.origin.z + self.direction.z * t
        return Vector3(x, y, z)

    def reflected_ray(self, point, normal):
        d = self.direction
        n = normal
        n = n.mult(d.dot(n) * 2)
        return Ray(point, Vector3(d.x - n.x, d.y - n.y, d.z - n.z))
    

def get_direction_to(pixel, from_position):
    x, y = pixel
    direction = Vector3(x - from_position.x, y - from_position.y, 0 - from_position.z)
    return direction




if __name__ == "__main__":
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    MAX_DEPTH = 5
    
    camera_position = Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, -100)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raytracer")

    screen.fill((0, 0, 0))

    sphere = Sphere(Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 100), 100, (255, 0, 0))
    light = Light(Vector3(SCREEN_WIDTH, 0, 100), 200, (255, 255, 255))

    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            result_colors = []
            for i in range(4):
                pixel = (x, y)
                jostled_pixel = (x + i / 4, y + i / 4)
                direction = get_direction_to(pixel, camera_position)
                ray = Ray(camera_position, direction)
                intersects = sphere.intersect(ray)
                if intersects:
                    t0, t1 = intersects
                    t = min(t0, t1)
                    point = ray.get_point(t)
                    result_colors.append(sphere.color)
                    # color = sphere.color
                    # screen.set_at(pixel, color)
                    normal = sphere.get_normal(point)
                    reflected_ray = ray.reflected_ray(point, normal)
                    reflected_intersects = light.intersect(reflected_ray)
                    if reflected_intersects:
                        color = light.color
                        rgb = result_colors[-1]
                        result_colors.append(color)
                        

            
            if len(result_colors) > 0:
                r = 0
                g = 0
                b = 0
                for color in result_colors:
                    r += color[0]
                    g += color[1]
                    b += color[2]
                r /= len(result_colors)
                g /= len(result_colors)
                b /= len(result_colors)
                r = int(r)
                g = int(g)
                b = int(b)
                r = r if r < 255 else 255
                g = g if g < 255 else 255
                b = b if b < 255 else 255
                color = (r, g, b)
                screen.set_at(pixel, color)
                    

            
    
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
    pygame.quit()
            