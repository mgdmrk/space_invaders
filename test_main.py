import unittest
import pygame

import main
import assets

class EnemyTest(unittest.TestCase):

    def setUp(self):
        self.enemy = main.Enemy(200, 300, "pink")
        assets.Assets.load()

    def test_move(self):
        self.enemy.move(5)
        self.assertEqual(self.enemy.y, 300 + 5)

    def test_shoot(self):
        self.bullet_x =  self.enemy.x - 20
        self.bullet_y = self.enemy.y
        self.bullet_image = self.enemy.bullet_image
        self.enemy.bullets.clear()
        self.enemy.shoot()
        self.assertEqual(1, len(self.enemy.bullets))


if __name__ == '__main__':
    unittest.main()

