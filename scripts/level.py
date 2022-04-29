from scripts.config import *
import csv


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.tileImage = image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.map = None


class Level:

    def __init__(self, group, tileList, interactList):
        super().__init__()
        self.tileList = tileList
        self.interactList = interactList
        self.levels = {0: {'name': 'tutorial', 'playerPosX': 100, 'playerPosY': 800},
                       1: {'name': 'level2', 'playerPosX': 0, 'playerPosY': 0}}
        self.group = group
        self.map = None

    # gameSprites.change_layer(self, 1)

    def loadMap(self):
        import main
        print(main.currentLevel)
        level = self.levels[main.currentLevel].get('name')
        with open(f'scripts/{level}.csv', newline='') as f:
            reader = csv.reader(f)
            self.map = list(reader)

    def render(self):
        tileSize = bottom.get_height()

        for y, row in enumerate(self.map):
            for x, column in enumerate(row):
                if column == '21':
                    tile = Tile(topLeft, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '22':
                    tile = Tile(top, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '23':
                    tile = Tile(topRight, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '25':
                    tile = Tile(door, x * tileSize, y * tileSize)
                    self.interactList.add(tile)
                    self.group.add(tile)

                if column == '31':
                    tile = Tile(left, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '32':
                    tile = Tile(middle, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '33':
                    tile = Tile(right, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '35':
                    tile = Tile(flat, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '41':
                    tile = Tile(bottomLeft, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '42':
                    tile = Tile(bottom, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                if column == '43':
                    tile = Tile(bottomRight, x * tileSize, y * tileSize)
                    self.tileList.add(tile)
                    self.group.add(tile)
                # group.add(self.tileList)