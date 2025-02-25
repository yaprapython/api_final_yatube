from posts.models import Comment, Post, Group, Follow
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Follow
        fields = ['user', 'following']

    def validate(self, attrs):
        user = attrs.get('user')
        following = attrs.get('following')
        if user == following:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs
