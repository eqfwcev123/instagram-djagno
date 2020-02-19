from django.shortcuts import render, redirect

# Create your views here.
from posts.forms import PostCreateForm, PostCommentCreateForm
from posts.models import Post, PostLike, PostImage


def post_list(request, tag=None):
    form = PostCommentCreateForm()
    posts = Post.objects.all().order_by('-pk')
    context = {
        'commentform': form,
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


def post_list_by_tag(request, tag):
    # URL:/explore/tags/<tag문자열>/
    # TEMPLATE: /posts/post-list.html
    # <tag문자열>인 Tag를 자신 (post).tags에 가지고 있는 경우인 post목록만 돌려줘야 한다.
    # 이 내용 이외에는 위의 Post_list 내용과 동일

    post = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')
    form = PostCommentCreateForm()
    context = {
        'commentform': form,
        'posts': post
    }
    return render(request, 'posts/post-list.html', context)


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


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        user = request.user
        # content = request.POST['content']
        form = PostCommentCreateForm(data=request.POST)
        if form.is_valid():
            # content = form.cleaned_data['content']
            # PostComment.objects.create(author=user, content=content, post=post)
            # 위 코드와 동일
            form.save(post=post, author=user)
        return redirect('posts:post-list')


def comment_list(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = post.postcomment_set.all()
    context = {
        'comments': comments
    }
    return render(request, 'posts/comment-list.html', context)
