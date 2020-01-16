import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from posts.models import Post, PostComment, Tag


class Command(BaseCommand):
    help = "Display current Post, Comments and Tags"

    def handle(self, *args, **options):
        now = timezone.now()
        # post = Post.objects.count()
        # comment = PostComment.objects.count()
        # tag = Tag.objects.count()

        # instagram/.media/now.txt 에 기록
        # 파일이 있다면 다음줄에 기록
        # 파일이 없다면 생성하고 기록

        with open(os.path.join(settings.MEDIA_ROOT, 'now.txt'), 'at') as f:
            time_str = f'Now: {timezone.localtime(now).strftime("%Y-%m-%d %H:%M:%S")}\n'
            f.write(time_str)

        # cron을 사용하면 자동으로 특정 행동을 실행해준다.(업무 자동화)
        # 크론은 어떤 파일에 있는 어떤 파이썬 버전을 사용해야 하는지 모른다. 그렇기 때문에 우리가 설정을 해줘야 한다.
