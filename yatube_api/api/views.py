# TODO:  Напишите свой вариант
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from posts.models import Post, Group, Follow
from .serializers import PostSerializer, CommentSerializer
from .serializers import GroupSerializer, FollowSerializer
from .permissions import IsAuthorOrReadOnly

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import filters
from rest_framework.exceptions import ValidationError


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound()
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = []


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        following_user = serializer.validated_data['following']
        if Follow.objects.filter(user=user, following=following_user).exists():
            raise ValidationError("You are already following this user.")
        if user == following_user:
            raise ValidationError()
        serializer.save(user=user)
