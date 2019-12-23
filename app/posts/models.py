from django.db import models
from django.utils import timezone

# Create your models here.
from members.models import User


class Post(models.Model):
    """
    인스타그램 포스트
    """
    # author 와 like_user 를 이용해서 User를 접근하는 것은 상관이 없는데, User에서 역방향으로 접근할 때 문제가 생긴다(구분을 할 수가 없다)
    # 그렇기 때문에 두 필드를 구분해줘야 한다.
    # 쉽게 말하면 User.post_set.메소드() 를 하면 author를 의미하는건지, like_user를 의미하는건지 알 수 없다. 그렇기 때문에 related_name
    # 을 적어줘야햔다.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_user = models.ManyToManyField(User, through='PostLike', related_name='like_post_set')
    created = models.DateTimeField(auto_now_add=True)


class PostImage(models.Model):
    """
    각 포스트의 사진
    """
    # Post 가 사라지면 이미지도 사라져야 하기 때문에 User 가 아닌 Post 랑 연결 해야한다.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 파일을 업로드 하면 자동으로 해당 경로로 파일을 업로드 하게 만들기.
    image = models.ImageField(upload_to='posts/images')

    # 정적 파일은 두종류가 있는데, 소스코드에 사용될 파일이랑 소스코드에 사용되지 않을 파일 두가지이다.
    # 소스코드에 사용되지 않을 정적파일 같은 경우 다른곳에다가 저장을 해야한다.
    # 소스코드에 사용될 정적 파일 : static
    # 소스코드에 사용되지 않을 정적 파일 : Media(git 에 올라가지 않을 파일을 만들어 두고 gitignore에 설정)

class PostComment(models.Model):
    """
    각 포스트의 댓글(Many To One)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    """
    사용자가 좋아요를 누른 Post 를 저장.
    Many-To-Many 필드를 중간 모델(Intermediate model)을 거쳐 사용.
    언제 생성 되었는지를 extra field 로 지정
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
