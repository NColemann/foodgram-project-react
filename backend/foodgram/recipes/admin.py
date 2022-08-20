from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    Favorite,
    ShoppingList,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites',
                    'tags', 'ingredients')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def tags(obj):
        return list(obj.tags.all())
    tags.short_description = 'Теги'

    @staticmethod
    def ingredients(obj):
        return list(obj.ingredients.all())
    ingredients.short_description = 'Ингредиенты'


@admin.register(IngredientRecipe)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'
