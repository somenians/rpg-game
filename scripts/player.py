import math

from scripts.inventory import Item, Inventory
from scripts.config import *

# import time
# import operator

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    layer = 2

    def __init__(self, pos, group, tileList, interactList):
        super().__init__(group)
        # player animations
        self.frame = 0
        self.animation = playerIdle
        # player properties
        self.image = playerIdle[self.frame]
        self.originalImage = self.image
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.airTimer = 0
        self.speed = 6
        self.gravity = 0
        self.tileList = tileList
        self.interactList = interactList
        self.direction = {'left': False, 'right': True}
        self.health = 50

        # player mechanics
        self.attacking = False
        self.attackCooldown = 600
        self.attackTime = None
        self.canDash = True
        self.dashCooldown = 5000
        self.dashTime = 0
        self.interacting = False
        self.interactCooldown = 400
        self.interactTime = 0
        self.primarySelected = False
        self.secondarySelected = False
        self.swapping = False
        self.swapCooldown = 100
        self.swapTime = 0

        # player inventory
        self.inventory = Inventory(self)
        self.belt = ['stick', 'stone_sword']
        self.selected = self.belt[0]
        self.item = Item(group, self, self.selected)
        self.item.kill()

        self.group = group
        group.add(self, layer=self.layer)

    def movement(self, dt):

        self.velocity = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity[0] += self.speed
            if not self.primarySelected:
                self.direction['right'], self.direction['left'] = True, False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity[0] -= self.speed
            if not self.primarySelected:
                self.direction['left'], self.direction['right'] = True, False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.airTimer < 3:
                self.gravity = -16

        if keys[pygame.K_SPACE] and self.canDash:
            if self.direction['right']:
                # self.rect.x += 200
                self.velocity[0] += 200
            else:
                self.velocity[0] -= 200
                # self.rect.x -= 200
            self.canDash = False
            self.dashTime = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()
            print("attack")
        if keys[pygame.K_1] and not self.swapping:
            if self.primarySelected:
                self.primarySelected = False
                print('stashed 1')
            # print(self.inventory.selected)
            elif not self.primarySelected:
                self.primarySelected = True
                self.secondarySelected = False
                self.selected = self.belt[0]
                print('selected 1')
            self.swapping = True
            self.swapTime = pygame.time.get_ticks()
        if keys[pygame.K_2] and not self.swapping:
            if self.secondarySelected:
                self.secondarySelected = False
                print('stashed 2')
            # print(self.inventory.selected)
            elif not self.secondarySelected:
                self.secondarySelected = True
                self.primarySelected = False
                self.selected = self.belt[1]
                print('selected 2')
            self.swapping = True
            self.swapTime = pygame.time.get_ticks()
            print("unselected")
        if keys[pygame.K_e] and not self.interacting:
            self.interacting = True
            self.interactTime = pygame.time.get_ticks()
            print('interacting')
        if keys[pygame.K_r]:
            self.rect = self.image.get_rect(center=(0, 0))

        self.gravity += 0.8 * dt
        self.velocity[1] += self.gravity
        if self.velocity[1] > 20:
            self.velocity[1] = 20

    def collision(self, dt):
        # horizontal collision

        self.rect.x += self.velocity[0] * dt
        tileList = self.tileList
        interactList = self.interactList
        for tile in tileList:
            if self.rect.colliderect(tile.rect):
                if self.velocity[0] < 0:
                    self.rect.left = tile.rect.right
                elif self.velocity[0] > 0:
                    self.rect.right = tile.rect.left
        # vertical collision
        self.rect.y += self.velocity[1] * dt
        for tile in tileList:
            if self.rect.colliderect(tile.rect):
                if self.velocity[1] > 0:
                    self.rect.bottom = tile.rect.top
                    self.airTimer = 0
                    self.gravity = 0
                elif self.velocity[1] < 0:
                    self.rect.top = tile.rect.bottom
                    self.gravity = 0
        for tile in interactList:
            if self.rect.colliderect(tile.rect) and self.interacting:
                import main
                main.nextLevel = True

    def animate(self, weaponAngle, dx, dy):
        # keyboard controlled animation
        if self.velocity[0] == 0:
            self.animation = playerIdle
            self.frame += 0.04
        if self.velocity[0] != 0:
            self.animation = playerRun
            self.frame += 0.14
        if self.frame >= len(self.animation):
            self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.originalImage = self.image

        # mouse controlled animation
        if weaponAngle < 270 and self.primarySelected:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction['left'], self.direction['right'] = True, False
        elif self.direction['left'] and not self.primarySelected:
            self.image = pygame.transform.flip(self.image, True, False)

        if 450 > weaponAngle > 270 and self.primarySelected:
            self.image = self.originalImage
            self.direction['right'], self.direction['left'] = True, False
        if self.direction['right'] and not self.primarySelected:
            self.image = self.originalImage

        if self.attacking:
            if self.direction['right']:
                self.item.rect.x += 15
                self.item.rect.y += round(15 * math.sin(weaponAngle))
            if self.direction['left']:
                self.item.rect.x -= 15
                self.item.rect.y += round(15 * math.sin(weaponAngle))

    def cooldown(self):
        currentTick = pygame.time.get_ticks()
        if not self.canDash:
            if currentTick - self.dashTime >= self.dashCooldown:
                self.canDash = True
        if self.attacking:
            if currentTick - self.attackTime >= self.attackCooldown:
                self.attacking = False
        if self.swapping:
            if currentTick - self.swapTime >= self.swapCooldown:
                self.swapping = False
        if self.interacting:
            if currentTick - self.interactTime >= self.interactCooldown:
                self.interacting = False

    def update(self, dt, dx, dy, weaponAngle):
        self.airTimer += 1
        self.inventory.update(weaponAngle), self.cooldown(), self.animate(weaponAngle, dx, dy), self.movement(
            dt), self.collision(dt)