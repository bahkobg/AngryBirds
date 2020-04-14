import pygame
import pymunk
import math


class Polygon:
    def __init__(self, img: object, pos: tuple, space: object, mass=3.0) -> None:
        self.image = img
        self.width = img.get_rect().width
        self.height = img.get_rect().height

        # Pymunk properties
        moment = 1500
        body = pymunk.Body(mass, moment)
        body.position = pymunk.Vec2d(pos)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.elasticity = 0.45
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
        angle_degrees = math.degrees(poly.body.angle) + 180
        rotated_img = pygame.transform.rotozoom(self.image,
                                                angle_degrees, 1)
        offset = pymunk.Vec2d(self.image.get_size()) / 2.
        p = p - offset
        np = p
        screen.blit(rotated_img, (np.x, np.y))


class Pig:
    def __init__(self, img: object, pos: tuple, space: object, mass=3.0) -> None:
        self.image = img
        self.width = img.get_rect().width
        self.height = img.get_rect().height
        self.health = 100
        self.img_pigs = pygame.image.load('assets/images/pigs.png')
        self.img_pig1 = self.img_pigs.subsurface(pygame.Rect(0, 0, 129, 120)).copy()
        self.img_pig2 = self.img_pigs.subsurface(pygame.Rect(129, 0, 129, 120)).copy()
        self.img_pig3 = self.img_pigs.subsurface(pygame.Rect(258, 0, 129, 120)).copy()
        self.img_pig4 = self.img_pigs.subsurface(pygame.Rect(0, 124, 129, 120)).copy()
        self.img_pig5 = self.img_pigs.subsurface(pygame.Rect(129, 124, 129, 120)).copy()
        self.img_pig6 = self.img_pigs.subsurface(pygame.Rect(258, 124, 129, 120)).copy()
        self.img_pig7 = self.img_pigs.subsurface(pygame.Rect(0, 248, 129, 120)).copy()
        self.img_pig8 = self.img_pigs.subsurface(pygame.Rect(129, 248, 129, 120)).copy()
        self.img_pig9 = self.img_pigs.subsurface(pygame.Rect(258, 248, 129, 120)).copy()

        # Pymunk properties
        moment = 1500
        body = pymunk.Body(mass, moment)
        body.position = pymunk.Vec2d(pos)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.color = (0, 0, 255)
        shape.friction = 1
        shape.elasticity = 0.5
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def take_damage(self, x):
        self.health -= x
        if self.health <= 10:
            self.image = self.img_pig9
        elif self.health <= 20:
            self.image = self.img_pig8
        elif self.health <= 30:
            self.image = self.img_pig7
        elif self.health <= 40:
            self.image = self.img_pig6
        elif self.health <= 50:
            self.image = self.img_pig5
        elif self.health <= 60:
            self.image = self.img_pig4
        elif self.health <= 70:
            self.image = self.img_pig3
        elif self.health <= 80:
            self.image = self.img_pig2
        elif self.health <= 90:
            self.image = self.img_pig1

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
        power = distance * 42
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
