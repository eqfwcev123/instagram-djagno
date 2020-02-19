from rest_framework import serializers

from members.serializers import UserSerializer
from posts.models import Post, PostImage, PostComment


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            "pk",
            "author",
            "content",
            "postimage_set"
        )


class PostCreateSerializer(serializers.ModelSerializer):
    # ListField : A Field class that validates a List of objects.
    # ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)
    # FieldInstance 는 serializers.필드명()
    images = serializers.ListField(
        child=serializers.ImageField()
    )

    class Meta:
        model = Post
        fields = (
            'images',
            'content',
        )

    def create(self, validated_data):
        # images가 없기 때문에 우리가 수동으로 빼줘야 한다
        images = validated_data.pop('images')
        post = super().create(validated_data)
        for image in images:
            serializer = PostImageCreateSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save(post=post)
        return post

    def to_representation(self, instance):
        return PostSerializer(instance).data


class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )

    def create(self, validated_data):
        return super().create(validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        # 클라이언트가 필요한 데이터를 줘야하면 된다.
        fields = (
            'pk',
            'content',
        )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'content',  # request.data 에서온다

            # 이 둘은 필요없기 때문에 안보내 줘도 된다 ==> Url 에서 정보를 받을 수 있기 때문에
            # 'author',  # request.user 에서온다
            # 'post'  # post의 정보는 url 에서온다
        )
