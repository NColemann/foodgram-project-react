from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from djoser.views import UserViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import IsAuthorOrAdminPermission
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingList,
    IngredientRecipe,
)
from users.models import Follow
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    ShoppingListSerializer,
    FollowSerializer,
    UserFieldsSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserFieldsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(
                user=request.user,
                author_id=user_id,
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id,
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        following = Follow.objects.filter(
            user=request.user,
            author_id=user_id,
        )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListViewSet(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_object(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_object(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        object = get_object_or_404(model, user=user, recipe=recipe)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.create_object(
                request=request,
                pk=pk,
                serializers=FavoriteSerializer,
            )
        return self.delete_object(request=request, pk=pk, model=Favorite)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.create_object(
                request=request,
                pk=pk,
                serializers=ShoppingListSerializer,
            )
        return self.delete_object(request=request, pk=pk, model=ShoppingList)

    def __list_to_display(self, shopping_list):
        list_display = ([
            f"- {item}: {value['amount']} {value['measurement_unit']}\n"
            for item, value in shopping_list.items()
        ])
        return list_display

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__shop_list__user=request.user
        )
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            amount = ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                shopping_list[name]['amount'] += amount
        main_list = self.__list_to_display(shopping_list)
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="ShoppingList.txt"'
        )
        return response
