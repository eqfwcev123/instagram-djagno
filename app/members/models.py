from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    사용자 모델로 쓰인다
    """
    img_profile = models.ImageField('프로필 이미지', blank=True, upload_to='users/')
    name = models.CharField(max_length=50)
