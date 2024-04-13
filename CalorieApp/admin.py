from django.contrib import admin
#from .models import Item, Transaction, Recipe, Ingredient
from .models import Player, FarmingSkill, PlayerSkill, Field, Seed, Planting, Crop

#admin.site.register(Item)
#admin.site.register(Transaction)
#admin.site.register(Recipe)
#admin.site.register(Ingredient)

admin.site.register(Player)
admin.site.register(FarmingSkill)

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner')

@admin.register(PlayerSkill)
class PlayerSkillAdmin(admin.ModelAdmin):
    list_display = ('player', 'skill', 'level', 'xp')

@admin.register(Seed)
class SeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'seed_count')

@admin.register(Planting)
class PlantingAdmin(admin.ModelAdmin):
    list_display = ('seed', 'player', 'planting_date')

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'variety', 'days_til_harvest')