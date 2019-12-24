from django.contrib import admin

# Register your models here.
from posts.models import PostComment, Post, PostImage, PostLike


class PostImageInline(admin.TabularInline):
    # model 이라는 것은 원래 가지고 있는 키워드 이다
    model = PostImage


class PostCommentInline(admin.TabularInline):
    model = PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created')
    inlines = [
        PostImageInline,
        PostCommentInline
    ]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    """
    작성자, 글, 작성시간
    """
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLike(admin.ModelAdmin):
    pass
