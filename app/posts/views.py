from django.shortcuts import render, redirect

# Create your views here.
from posts.models import Post, PostLike


def post_list(request):
    posts = Post.objects.all().order_by('-pk')
    context = {
        'posts': posts
    }
    return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    post_like_qs = PostLike.objects.filter(post=post, user=user)
    if post_like_qs.exists():
        post_like_qs.delete()
        return redirect('posts:post-list')
    else:
        PostLike.objects.create(post=post, user=user)
        return redirect('posts:post-list')
