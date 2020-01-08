from django.shortcuts import render, redirect

# Create your views here.
from posts.forms import PostCreateForm
from posts.models import Post, PostLike, PostImage


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


def post_create(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.getlist('image')
        text = request.POST['text']
        post = Post.objects.create(author=user, content=text)
        # post.postimage_set.create(image=image)
        # PostImage.objects.create(post=post, image=image)
        for f in image:
            PostImage.objects.create(post=post, image=f)
        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'forms': form
        }
        return render(request, 'posts/post-create.html', context)
