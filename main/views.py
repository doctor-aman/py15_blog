from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from main.models import Category, Post, Comment, Favorites
from main.permissions import IsAuthor
from main.serializers import CategorySerializer, PostSerializer, PostListSerializer, CommentSerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Фильтрация и поиск:
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'text']
    filter_fields = ['category', 'tags']

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'list':
            serializer_class = PostListSerializer
        return serializer_class

    def get_permissions(self):
        # создавать может пост авторизованный пользователь
        if self.action in ['create', 'add_to_favorites', 'remove_from_favorites']:
            return [IsAuthenticated()]
        # изменять и удалять модет только автор поста
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        # просмотр поста доступен всем
        return []

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk=None):
        post = self.get_object()
        if request.user.liked.filter(post=post).exists():
            return Response('Уже добавлено в избранное')
        Favorites.objects.create(post=post, user=request.user)
        return Response('Добавлено в избранное')

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk=None):
        post = self.get_object()
        if not request.user.liked.filter(post=post).exists():
            return Response('Пост не находится в списке избранных')
        request.user.liked.filter(post=post).delete()
        return Response('Пост удален из избранных')



class CommentViewSet(CreateModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        # создавать может пост авторизованный пользователь
        if self.action == 'create':
            return [IsAuthenticated()]
        # изменять и удалять может только автор поста
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]

# TODO:избранное, лайки
# TODO:Swagger
