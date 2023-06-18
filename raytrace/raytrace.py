import pygame
import math
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
MAX_DEPTH = 5


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

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
        if dp < 0:  # Ray points away from sphere
            return False
        d_squared = line_to_sphere.dot(line_to_sphere) - dp * dp
        if d_squared > self.radius * self.radius:
            return False
        d = (self.radius * self.radius - d_squared) ** 0.5
        near_intersect = dp - d
        far_intersect = dp + d
        return min(near_intersect, far_intersect)

    def get_normal(self, point):
        return (point - self.center).normalized()


class Light(Sphere):
    def __init__(self, center, radius, color):
        super().__init__(center, radius, color)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin + direction.normalized().mult(0.001)
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
        # n = n + Vector3(
        #     random.random() * 0.1, random.random() * 0.1, random.random() * 0.1
        # )
        return Ray(point, Vector3(d.x - n.x, d.y - n.y, d.z - n.z))


def get_direction_to(pixel, from_position, image_width, image_height, fov=math.pi / 3):
    aspect_ratio = image_width / image_height
    x, y = pixel
    u = (2 * (x + 0.5) / image_width - 1) * aspect_ratio
    v = 1 - 2 * (y + 0.5) / image_height
    d = 1 / math.tan(fov / 2)
    direction = Vector3(u, v, -d)
    return direction


def get_color(pixel, objects, camera_position, max_depth, light):
    if max_depth <= 0:
        return (0, 0, 0)
    intersects = []
    normals = []
    objs = []
    color = (0, 0, 0)
    ray_direction = get_direction_to(
        pixel, camera_position, SCREEN_WIDTH, SCREEN_HEIGHT
    )
    for obj in objects:
        intersect = obj.intersect(Ray(camera_position, ray_direction))
        if intersect:
            intersects.append(intersect)
            normals.append(
                obj.get_normal(Ray(camera_position, ray_direction).get_point(intersect))
            )
            objs.append(obj)

    if len(intersects) > 0:
        index = intersects.index(min(intersects))
        intersect = intersects[index]
        normal = normals[index]
        point = Ray(camera_position, ray_direction).get_point(intersect)
        color = objs[index].color

        vec_to_light = Vector3(
            light.center.x - point.x, light.center.y - point.y, light.center.z - point.z
        ).normalized()

        light_intersects = []
        light_normals = []
        light_objs = []

        for obj in objects:
            intersect = obj.intersect(Ray(point, vec_to_light))
            if intersect:
                light_intersects.append(intersect)
                light_normals.append(
                    obj.get_normal(Ray(point, vec_to_light).get_point(intersect))
                )
                light_objs.append(obj)

        if len(light_intersects) > 0:
            light_index = light_intersects.index(min(light_intersects))
            o = light_objs[light_index]
            if isinstance(o, Light):
                diffuse = max(0, vec_to_light.dot(normal))
                factor = max(diffuse, 0.1)
                color = (color[0] * factor, color[1] * factor, color[2] * factor)
            else:
                color = (color[0] * 0.1, color[1] * 0.1, color[2] * 0.1)

        if isinstance(objs[index], Light):
            return objs[index].color

        reflected_ray = Ray(
            Vector3(
                point.x + normals[index].x,
                point.y + normals[index].y,
                point.z + normals[index].z,
            ),
            ray_direction,
        ).reflected_ray(point, normal)
        if max_depth > 0:
            reflection_color = get_color(
                pixel,
                objects,
                reflected_ray.origin + reflected_ray.direction.normalized().mult(0.001),
                max_depth - 1,
                light,
            )
            
            reflection_color = Vector3(
                reflection_color[0], reflection_color[1], reflection_color[2]
            )
            color = Vector3(color[0], color[1], color[2])
            reflection_coefficient = 0.8
            color = color.mult(1 - reflection_coefficient) + reflection_color.mult(
                reflection_coefficient
            )
            color = (int(color.x), int(color.y), int(color.z))

    return color


def color_combine(color1, color2, depth=1):
    return (
        int((color1[0] + color2[0]) / 2),
        int((color1[1] + color2[1]) / 2),
        int((color1[2] + color2[2]) / 2),
    )


if __name__ == "__main__":
    camera_position = Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 1000)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raytracer")

    screen.fill((0, 0, 0))

    sphere1 = Sphere(
        Vector3(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, -1200), 350, (255, 0, 0)
    )
    sphere2 = Sphere(Vector3(-300, 200, -1700), 800, (100, 0, 100))
    light = Light(Vector3(SCREEN_WIDTH, 0, -500), 300, (255, 255, 255))

    back_wall = Plane(Vector3(0, 0, -2000), Vector3(0, 0, 1), (255, 255, 255))
    left_wall = Plane(Vector3(-800, 0, 0), Vector3(1, 0, 0), (0, 0, 255))
    bottom_wall = Plane(
        Vector3(0, SCREEN_HEIGHT + 800, 0), Vector3(0, -1, 0), (255, 255, 255)
    )
    top_wall = Plane(Vector3(0, -800, 0), Vector3(0, 1, 0), (255, 255, 255))
    right_wall = Plane(
        Vector3(SCREEN_WIDTH + 800, 0, 0), Vector3(-1, 0, 0), (255, 0, 0)
    )

    objects = [
        sphere1,
        sphere2,
        light,
        back_wall,
        left_wall,
        bottom_wall,
        top_wall,
        right_wall,
    ]

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(SCREEN_HEIGHT):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            pygame.display.flip()
            for x in range(SCREEN_WIDTH):
                color = get_color((x, y), objects, camera_position, MAX_DEPTH, light)
                screen.set_at((x, y), color)

    pygame.quit()
