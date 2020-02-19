from rest_framework import generics

from posts.models import Post
from posts.serializers import PostSerializer, PostCreateSerializer

"""
# 다음 메서드들을 사용하는 이유는 사용자가 어떤 값을 돌려줄지에 대한 조건을 걸 수 있기 때문이다.
- get_queryset(): list views 에서 사용할 쿼리셋을 항상 반환해야하고, 이 쿼리셋은 항상 detail view 의 lookup
에 사용된다.
- get_object(): detail views에서 사용하기 위한 객체 인스턴스를 반환. 기본적으로 lookup_field를 이용해서
base 쿼리셋을 필터
- get_serializer_class(self): 사용자의 조건에 맞게 적절한 serializer_class를 반환


mixin class 에서 제공 해주는 메소드
- perform_create(self.serializer): 새로운 객체를 생성할 때 CreateModelMixin 에 의해 호출 
- perform_update(self.serializer): 기존에 있던 객체를 업데이트 할때 UpdateModelMixin 에 의해 호출
- perform_delete(self.serializer): 기존에 있던 객체를 삭제할 때 DestroyModelMixin 에 의해 호출

"""


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        else:
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    """
    def create(self, request, *args, **kwargs):
        # get_serializer() 는 시리얼라이저 인스턴스를 반환한다.
        serializer = self.get_serializer(data=request.data) ---> 인스턴스의 시리얼라이저에 request.data를 넣어서 보낸다
        serializer.is_valid(raise_exception=True) ---> serializer 가 유요한지 확인. Is_valid() 와 동일
        self.perform_create(serializer) ---> serializer.save() 와 실제로 동일
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) ---> serializer 반환
    """


class PostImageCreateAPIView(generics.CreateAPIView):

    def get_queryset(self, *args):
        post = Post.objects.get(pk=args)
        return post

    def perform_create(self, serializer):
        for image in request.data.getlist('image'):
            post.postimage_set.create(image=image)

    # post = Post.objects.getpk=ㅁ
    # for image in request.data.getlist('image'):
    #     post.postimage_set.create(image=image)
    #
    # serializer = PostCreateSerializer(post)
    # return Response(serializer.data)
