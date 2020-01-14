from django.db import models
from django.utils import timezone
import re

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
    TAG_PATTERN = re.compile(r'#(\w+)')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_user = models.ManyToManyField(User, through='PostLike', related_name='like_post_set')
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", verbose_name="해시태그 목록",
                                  related_name="posts", blank=True)  # 포스트 한개에 여러개의 해쉬태그를 갖을 수 있고 그반대가 될 수 있다

    def __str__(self):
        return f'author : {self.author}, content: {self.content}, like_user : {self.like_user}, created: {self.created}'

    def __save__(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tag_name_list = re.findall(self.TAG_PATTERN, self.content)

        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_name_list]
        self.tags.set(tags)


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


# Fk, MTM, OTO 를 할때 해당 필드가 어디에 있는지 생각해보자
# author 는 사용자이면 user 테이블에 있을것이다.
# post는 post 테이블에 있을 것이고 user 는 user 테이블에 있을 것이다.
# 얀걀하고자 하는 데이터가 어디있을지 만 생각하면 쉽게 연결할 수 있다.

class Tag(models.Model):
    """
    Hash태그의 태그를 담당
    Post 입장에서 post.tags.all()로 연결된 전체 TAG를 불러올 수 있어야 한다
    Tag 입장에서 tag.post.all()로 연결된 전체 POST를 불러와야 한다

    Django admin 에서 결과를 볼 수 있도록 admin.py 를 설정
    """
    name = models.CharField('태그명', max_length=150)

    def __str__(self):
        return self.name
