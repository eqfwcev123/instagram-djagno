from rest_framework import serializers

from members.serializers import UserSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = ("pk", "content", "author")
