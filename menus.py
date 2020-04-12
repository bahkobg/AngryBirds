import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, img: object, x: int, y: int, width: int, height: int, button_id: str) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.image = pygame.transform.scale(img, (width, height))
        self.button_id = button_id

    def draw(self, surface: object) -> None:
        surface.blit(self.image, self.rect)

    @property
    def get_button_id(self):
        return self.button_id
