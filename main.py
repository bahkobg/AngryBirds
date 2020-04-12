import pygame
import pymunk
from sprites import Polygon
from sprites import Bird
import math

WIN_WIDTH = 1280
WIN_HEIGHT = 720


class Runtime:
    def __init__(self):
        pygame.display.set_caption('Angry Birds by Ivan Ivanov')
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bird_being_dragged = False

        self.mouse_x = 0
        self.mouse_y = 0

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -700.0)

        # Loading images
        self.img_landing = pygame.image.load('assets/images/landing_img.png')
        self.img_background_1 = pygame.transform.scale(pygame.image.load('assets/images/background1.jpg'), (WIN_WIDTH, WIN_HEIGHT))
        self.img_sling = pygame.transform.scale(pygame.image.load('assets/images/sling.png').convert_alpha(), (150, 150))
        self.img_buttons = pygame.image.load('assets/images/buttons.png')
        self.img_button_play = self.img_buttons.subsurface(pygame.Rect(965, 32, 238, 150)).copy()
        self.img_button_restart = self.img_buttons.subsurface(pygame.Rect(1324, 940, 155, 142)).copy()
        self.img_sling_1 = self.img_sling.subsurface(pygame.Rect(0, 0, 35, 65)).copy()
        self.img_sling_2 = self.img_sling.subsurface(pygame.Rect(40, 0, 110, 150)).copy()
        self.img_crate_box = pygame.transform.scale(pygame.image.load('assets/images/crate_box.png'), (32, 32))
        self.img_pig = pygame.image.load('assets/images/pig.png')
        self.img_angry_bird = pygame.transform.scale(pygame.image.load('assets/images/angry_bird.png'), (48, 48))

        # Load the image sets
        beams = pygame.image.load("assets/images/beams.png").convert_alpha()
        columns = pygame.image.load("assets/images/columns.png").convert_alpha()

        # Subtract the images from the image set
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = beams.subsurface(rect).copy()

        rect = pygame.Rect(16, 252, 22, 86)
        self.column_image = columns.subsurface(rect).copy()

        self.game_state = None
        self.static_lines = []

        # Sprite lists
        self.buttons = pygame.sprite.Group()
        self.boxes = []
        self.pigs = []
        self.birds = []

    def setup(self):
        # Static floor
        static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.static_lines = [pymunk.Segment(static_body, (0.0, -24.0), (1280.0, -24.0), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3

        self.space.add(self.static_lines)
        self.game_state = 1

        self.boxes.extend(
            [Polygon(self.beam_image, (1000, 11), self.space),
             Polygon(self.column_image, (971, 64), self.space),
             Polygon(self.column_image, (1029, 64), self.space),
             Polygon(self.beam_image, (1000, 118), self.space),
             Polygon(self.beam_image, (1086, 11), self.space),
             Polygon(self.column_image, (1057, 64), self.space),
             Polygon(self.column_image, (1115, 64), self.space),
             Polygon(self.beam_image, (1086, 116), self.space),
             Polygon(self.column_image, (1000, 127), self.space),
             Polygon(self.column_image, (1086, 127), self.space),
             Polygon(self.beam_image, (1042, 181), self.space),
             Polygon(self.img_pig, (1042, 250), self.space),
             ]
        )

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        running = True
        while running:

            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.game_state == 1:
                        self.game_state = 2

                    elif self.game_state == 2:
                        pos = pygame.mouse.get_pos()
                        print(pos)
                        if 200 < pos[0] < 240 and 515 < pos[1] < 565:
                            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            self.bird_being_dragged = True
                        else:
                            self.bird_being_dragged = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.bird_being_dragged:
                        self.bird_being_dragged = False
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        # Angle of impulse
                        dy = y - 514
                        dx = x - 214
                        if dx == 0:
                            dx = 0.00000000000001
                        angle = math.atan((float(dy)) / dx)

                        # Distance of impulse
                        distance = ((self.mouse_x - x) ** 2 + (self.mouse_y - y) ** 2) ** 0.5

                        self.birds.append(
                            Bird(self.img_angry_bird, distance, angle, x, 600 - y, self.space)
                        )

            # Drawing
            self.draw(self.screen)

            # Pygame display update
            pygame.display.update()

            # Game FPS
            self.space.step(1.0 / 50.0)
            clock.tick(50)
        pygame.quit()

    def draw(self, surface: object) -> None:

        if self.game_state == 1:
            # Landing page drawing goes here
            surface.blit(self.img_landing, (0, 0))

        elif self.game_state == 2:  # In-game drawing goes here
            # Background
            surface.blit(self.img_background_1, (0, 0))

            # Sling long
            surface.blit(self.img_sling_2, (200, 515))

            # Draw static lines
            for line in self.static_lines:
                body = line.body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = self.to_pygame(pv1)
                p2 = self.to_pygame(pv2)
                pygame.draw.lines(self.screen, (150, 150, 150), False, [p1, p2])

            # Draw boxes
            for box in self.boxes:
                box.draw(self.screen)

            # Draw pigs
            for pig in self.pigs:
                pig.draw(self.screen)

            # Draw birds
            for bird in self.birds:
                bird.draw(self.screen)

            if self.bird_being_dragged:
                surface.blit(self.img_angry_bird, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 30))
                pygame.draw.line(surface, (0, 0, 0), pygame.mouse.get_pos(), (225, 536), width=5)
                pygame.draw.line(surface, (0, 0, 0), pygame.mouse.get_pos(), (203, 537), width=5)

            # Sling short
            surface.blit(self.img_sling_1, (188, 515))

        elif self.game_state == 3:
            pass
            # You-lose drawing goes here
        elif self.game_state == 4:
            # You-win drawing goes here
            pass

    @staticmethod
    def to_pygame(p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y + 600)


if __name__ == '__main__':
    g = Runtime()
    g.setup()
    g.run()
