import random
from collections import namedtuple

from .models import ShipPoint, Ship
from .utils import SHIP_TYPES


class RandomShips(object):
    '''Service for initial creating ships with points
    '''

    def __init__(self, game):
        self.game = game

    def create(self):
        '''Create all ships for new game
        '''

        for ship_type in SHIP_TYPES:
            self.create_ship(ship_type)

    def create_ship(self, ship_type):
        '''Create ship for ship_type
        '''
        ship = Ship.objects.create(game=self.game, name=ship_type.name)
        points = self.get_ship_points(ship, ship_type)

        ShipPoint.objects.bulk_create(
            [ShipPoint(ship=ship, x=point.x, y=point.y) for point in points])

        return ship

    def get_ship_points(self, ship, ship_type):
        '''Generate start and end from ship_type, needs to be betweek 1 and 10
        '''

        ShipObj = namedtuple('ShipObj', ['x', 'y'])

        created_points = ShipPoint.objects.filter(
            ship__game=self.game).values_list('x', 'y')

        while True:
            # random from boolean list, True = horizontal, Flase = vertical
            horizontal_dir = random.choice([True, False])

            start = random.randint(1, 10)
            end = start + ship_type.size

            if end <= 11:
                points = [
                    ShipObj(i, start) if horizontal_dir else ShipObj(start, i)
                    for i in range(start, end)
                ]

                # get common items between queryset and new points
                # if there is no common items, it should create points
                common_points = set(created_points) & set(points)
                if not common_points:
                    break

        return points
