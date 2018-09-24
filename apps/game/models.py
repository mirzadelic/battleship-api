from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    '''
    Game model
    '''

    name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    @property
    def finished_game(self):
        '''
        Returns boolean if game is finished
        '''
        attacks = Attack.objects.filter(game=self, hit=True).count()
        points = ShipPoint.objects.filter(ship__game=self).count()
        return attacks == points

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'
        ordering = ('-created_at',)


class Ship(models.Model):
    '''
    Ship model related to Game
    '''

    game = models.ForeignKey(
        Game, related_name='ships', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'ship'
        verbose_name_plural = 'ships'


class ShipPoint(models.Model):
    '''
    ShipPoint model related to Ship with x, y
    '''

    ship = models.ForeignKey(
        Ship, related_name='points', on_delete=models.CASCADE)
    x = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    y = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str('%s x %s' % (self.x, self.y))

    class Meta:
        verbose_name = 'ship point'
        verbose_name_plural = 'ship points'


class Attack(models.Model):
    '''
    Attack model related to Game with x, y and hit boolean
    '''

    game = models.ForeignKey(
        Game, related_name='attacks', on_delete=models.CASCADE)
    x = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    y = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    hit = models.BooleanField(default=False)

    def __str__(self):
        return str('%s - %s x %s' % (self.game.name, self.x, self.y))

    class Meta:
        verbose_name = 'attack'
        verbose_name_plural = 'attacks'
