from collections import Counter

from django.test import TestCase

from apps.game.models import Game, ShipPoint
from apps.game.services import RandomShips
from apps.game.utils import SHIP_TYPES


class RandomShipsTest(TestCase):

    def setUp(self):
        self.game = Game.objects.create(name='Game 1')
        self.random_game = RandomShips(self.game)

    def test__create_ship(self):
        '''
        Create one ship
        '''
        ship_type = SHIP_TYPES[4]
        self.random_game.create_ship(ship_type)

        ship = self.game.ships.first()

        self.assertEqual(self.game.ships.count(), 1)
        self.assertEqual(ship.name, ship_type.name)
        self.assertEqual(
            ShipPoint.objects.filter(ship__game=self.game).count(),
            ship_type.size
        )

    def test__create_ships(self):
        '''
        Create all ships
        '''
        self.random_game.create()

        self.assertEqual(self.game.ships.count(), len(SHIP_TYPES))
        self.assertEqual(
            ShipPoint.objects.filter(ship__game=self.game).count(),
            sum(ship.size for ship in SHIP_TYPES)
        )
