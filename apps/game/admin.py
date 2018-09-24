from django.contrib import admin

from .models import Game, Ship, ShipPoint, Attack


class ShipInline(admin.TabularInline):
    model = Ship
    extra = 0


class ShipPointInline(admin.TabularInline):
    model = ShipPoint
    extra = 0


class AttackInline(admin.TabularInline):
    model = Attack
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = readonly_fields = ('created_at',)
    list_display = list_display_links = ('id', 'name', 'created_at')
    inlines = (ShipInline, AttackInline)


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('game',)
    list_display = list_display_links = ('id', 'game', 'name')
    inlines = (ShipPointInline,)


@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    list_filter = ('game',)
    list_display = list_display_links = ('id', 'game', 'x', 'y', 'hit')
