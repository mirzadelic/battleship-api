from django.urls import reverse

from rest_framework.test import APITestCase

from apps.game.models import Game, ShipPoint, Attack
from apps.game.services import RandomShips
from apps.game.utils import SHIP_TYPES


class GameAPITests(APITestCase):

    def setUp(self):
        self.url = reverse('api:game:game-list')

    def test__create_ship(self):
        '''
        Create game with random ships
        '''

        data = {
            'name': 'Game 1'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])

        self.assertEqual(Game.objects.count(), 1)

        game = Game.objects.first()
        self.assertEqual(game.name, data['name'])
        self.assertEqual(game.ships.count(), 5)
        self.assertEqual(
            ShipPoint.objects.filter(ship__game=game).count(),
            sum(ship.size for ship in SHIP_TYPES)
        )

    def test__attack__success(self):
        '''
        Attack ship, success
        '''

        game = Game.objects.create(name='Game 1')
        RandomShips(game).create()
        ship_point = ShipPoint.objects.first()

        url = '%s%s/attack/' % (self.url, game.pk)
        data = {
            'x': ship_point.x,
            'y': ship_point.y,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['x'], data['x'])
        self.assertEqual(response.data['y'], data['y'])
        self.assertEqual(response.data['hit'], True)
        self.assertEqual(response.data['finished_game'], False)

    def test__attack__already_has_been_hit(self):
        '''
        Attack ship, already has been hit
        '''

        game = Game.objects.create(name='Game 1')
        RandomShips(game).create()
        attack = Attack.objects.create(game=game, x=5, y=6, hit=False)

        url = '%s%s/attack/' % (self.url, game.pk)
        data = {
            'x': attack.x,
            'y': attack.y,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data[0], 'The field has already been attacked.')

    def test__attack__missed(self):
        '''
        Attack ship, missed
        '''

        game = Game.objects.create(name='Game 1')
        RandomShips(game).create()

        url = '%s%s/attack/' % (self.url, game.pk)
        data = {
            'x': 10,
            'y': 10,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['x'], data['x'])
        self.assertEqual(response.data['y'], data['y'])
        self.assertEqual(response.data['hit'], False)
        self.assertEqual(response.data['finished_game'], False)

    def test__attack__game_finished(self):
        '''
        Attack ship, game finished
        '''

        game = Game.objects.create(name='Game 1')
        RandomShips(game).create()

        for sp in ShipPoint.objects.filter(ship__game=game):
            Attack.objects.create(game=game, x=sp.x, y=sp.y, hit=True)

        url = '%s%s/attack/' % (self.url, game.pk)
        data = {
            'x': 5,
            'y': 3,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data[0], 'The game is finished.')
