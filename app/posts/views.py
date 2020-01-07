from django.shortcuts import render


# Create your views here.
from posts.models import Post


def post_list(request):
    posts = Post.objects.all().order_by('-pk')
    context = {
        'posts': posts
    }
    return render(request, 'posts/post-list.html',context)
