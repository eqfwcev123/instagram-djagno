from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer, PostCreateSerializer, PostImageCreateSerializer, PostCommentSerializer, \
    PostCommentCreateSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        else:
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostImageCreateAPIView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getlist('image'):
            data = {
                'image': image
            }
            serializer = PostImageCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post)

        serializer = PostCreateSerializer(post)
        return Response(serializer.data)


class PostCommentListCreateAPIView(APIView):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk) # 특정 포스트의 모든 comment 를 가져와야 하기 때문에 post 인스턴스를 받아와서 _set 사용
        comments = post.postcomment_set.all()
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk) # 사용자가 보낸 url의 pk 를 이용해서 post 를 받아옴
        serializer = PostCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
