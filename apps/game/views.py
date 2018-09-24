from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Game
from .serializers import GameSerializer, AttackSerializer


class GameView(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    allowed_methods = ['GET', 'OPTIONS', 'POST']

    @action(methods=['post'], detail=True)
    def attack(self, request, pk=None):
        '''
        Attack action for game
        '''
        game = self.get_object()

        data = request.data
        data['game'] = game.pk

        serializer = AttackSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
