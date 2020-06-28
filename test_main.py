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
        self.enemy.shoot()


if __name__ == '__main__':
    unittest.main()

