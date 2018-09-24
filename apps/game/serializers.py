from rest_framework import serializers

from .models import Game, Attack, ShipPoint
from .services import RandomShips


class AttackSerializer(serializers.ModelSerializer):
    finished_game = serializers.BooleanField(
        source='game.finished_game', default=False, read_only=True)

    class Meta:
        model = Attack
        fields = ('game', 'x', 'y', 'hit', 'finished_game')
        extra_kwargs = {'game': {'write_only': True}}

    def create(self, validated_data):
        game = validated_data['game']

        if game.finished_game:
            raise serializers.ValidationError('The game is finished.')

        attack_exist = Attack.objects.filter(**validated_data).exists()
        if attack_exist:
            raise serializers.ValidationError(
                'The field has already been attacked.')

        validated_data['hit'] = ShipPoint.objects.filter(
            ship__game=game,
            x=validated_data['x'],
            y=validated_data['y']
        ).exists()

        attack = super(AttackSerializer, self).create(validated_data)

        return attack


class GameSerializer(serializers.ModelSerializer):
    attacks = AttackSerializer(many=True, read_only=True)
    # boolean field shows if game is finished or not
    finished_game = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'created_at', 'finished_game', 'attacks')

    def create(self, validated_data):
        game = super(GameSerializer, self).create(validated_data)

        RandomShips(game).create()

        return game
