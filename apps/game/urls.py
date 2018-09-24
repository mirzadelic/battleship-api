from django.urls import path, include
from rest_framework import routers

from .views import GameView


router = routers.DefaultRouter()
router.register('game', GameView)
app_name = 'game'
urlpatterns = [
    path('', include(router.urls)),
]
