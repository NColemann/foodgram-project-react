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


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'amount_favorites',
        'tags',
    )
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    inlines = (IngredientRecipeInline,)
    empty_value_display = '-пусто-'

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()
    amount_favorites.short_description = (
        'Число добавлений рецепта в избранное'
    )

    @staticmethod
    def tags(obj):
        return list(obj.tags.name())
    tags.short_description = 'Теги'


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
