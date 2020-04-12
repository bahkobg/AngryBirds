import pygame
import pymunk
import math


class Polygon:
    def __init__(self, img: object, pos: tuple, space: object, mass=5.0) -> None:
        self.image = img
        self.width = img.get_rect().width
        self.height = img.get_rect().height

        # Pymunk properties
        moment = 2000
        body = pymunk.Body(mass, moment)
        body.position = pymunk.Vec2d(pos)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.color = (0, 0, 255)
        shape.friction = 0.6
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape

    @staticmethod
    def to_pygame(p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y + 600)

    def draw(self, screen):
        """Draw beams and columns"""
        poly = self.shape
        p = poly.body.position
        p = pymunk.Vec2d(self.to_pygame(p))
        offset = pymunk.Vec2d(self.image.get_size()) / 2.
        p = p - offset
        np = p
        screen.blit(self.image, (np.x, np.y))


class Bird:
    def __init__(self, img, distance, angle, x, y, space):
        self.life = 20
        self.image = img
        mass = 5
        radius = 12
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        power = distance * 40
        impulse = power * pymunk.Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def draw(self, screen):
        p = self.to_pygame(self.shape.body.position)
        x, y = p
        x -= 22
        y -= 20
        screen.blit(self.image, (x, y))

    @staticmethod
    def to_pygame(p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y + 600)
