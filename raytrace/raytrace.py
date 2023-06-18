import pygame
import math

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


class Plane:
    def __init__(self, position, normal, color):
        self.position = position
        self.normal = normal
        self.color = color
    
    def intersect(self, ray):
        d = self.normal.dot(self.position)
        if self.normal.dot(ray.direction) == 0:
            return False
        t = (d - self.normal.dot(ray.origin)) / self.normal.dot(ray.direction)
        if t < 0:
            return False
        return t
    
    def get_normal(self, point):
        return self.normal



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
        return min(near_intersect, far_intersect)
    

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



def get_direction_to(pixel, from_position, image_width, image_height, fov=math.pi/3):
    aspect_ratio = image_width / image_height
    x, y = pixel
    u = (2 * (x + 0.5) / image_width - 1) * aspect_ratio
    v = 1 - 2 * (y + 0.5) / image_height
    d = 1 / math.tan(fov / 2)
    direction = Vector3(u, v, -d)
    return direction


if __name__ == "__main__":
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 640
    MAX_DEPTH = 5
    
    camera_position = Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 1000)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raytracer")

    screen.fill((0, 0, 0))

    sphere1 = Sphere(Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, -1200), 350, (255, 0, 0))
    sphere2 = Sphere(Vector3(-300, 200, -1700), 800, (100, 0, 100))
    light = Light(Vector3(SCREEN_WIDTH, 0, -1000), 300, (200, 200, 200))

    back_wall = Plane(Vector3(0, 0, -2000), Vector3(0, 0, 1), (0, 255, 0))
    left_wall = Plane(Vector3(-800, 0, 0), Vector3(1, 0, 0), (0, 0, 255))
    bottom_wall = Plane(Vector3(0, SCREEN_HEIGHT + 800, 0), Vector3(0, -1, 0), (255, 255, 0))
    top_wall = Plane(Vector3(0, -800, 0), Vector3(0, 1, 0), (255, 255, 255))
    right_wall = Plane(Vector3(SCREEN_WIDTH + 800, 0, 0), Vector3(-1, 0, 0), (255, 0, 255))

    objects = [sphere1, sphere2, light, back_wall, left_wall, bottom_wall, top_wall, right_wall]

    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            intersects = []
            normals = []
            objs = []
            color = (0, 0, 0)
            ray_direction = get_direction_to((x, y), camera_position, SCREEN_WIDTH, SCREEN_HEIGHT)
            for obj in objects:
                intersect = obj.intersect(Ray(camera_position, ray_direction))
                if intersect:
                    intersects.append(intersect)
                    normals.append(obj.get_normal(Ray(camera_position, ray_direction).get_point(intersect)))
                    objs.append(obj)
            
            if len(intersects) > 0:
                index = intersects.index(min(intersects))
                intersect = intersects[index]
                normal = normals[index]
                point = Ray(camera_position, ray_direction).get_point(intersect)
                color = objs[index].color
            
            screen.set_at((x, y), color)

            # result_colors = []
            # for i in range(4):
            #     pixel = (x, y)
            #     jostled_pixel = (x + i / 4, y + i / 4)
            #     direction = get_direction_to(pixel, camera_position)
            #     ray = Ray(camera_position, direction)
            #     intersect = sphere.intersect(ray)
            #     if intersect:
            #         t = intersect
            #         point = ray.get_point(t)
            #         result_colors.append(sphere.color)
            #         # color = sphere.color
            #         # screen.set_at(pixel, color)
            #         normal = sphere.get_normal(point)
            #         reflected_ray = ray.reflected_ray(point, normal)
            #         reflected_intersect = light.intersect(reflected_ray)
            #         if reflected_intersect:
            #             color = light.color
            #             rgb = result_colors[-1]
            #             result_colors.append(color)
                        

            
            # if len(result_colors) > 0:
            #     r = 0
            #     g = 0
            #     b = 0
            #     for color in result_colors:
            #         r += color[0]
            #         g += color[1]
            #         b += color[2]
            #     r /= len(result_colors)
            #     g /= len(result_colors)
            #     b /= len(result_colors)
            #     r = int(r)
            #     g = int(g)
            #     b = int(b)
            #     r = r if r < 255 else 255
            #     g = g if g < 255 else 255
            #     b = b if b < 255 else 255
            #     color = (r, g, b)
            #     screen.set_at(pixel, color)
                    

            
    
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
    pygame.quit()
            