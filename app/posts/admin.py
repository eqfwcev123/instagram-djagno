from django.contrib import admin

# Register your models here.
from posts.models import PostComment, Post, PostImage, PostLike, Tag


class PostImageInline(admin.TabularInline):
    # model 이라는 것은 원래 가지고 있는 키워드 이다
    model = PostImage
    extra = 1


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1


# register(): used to register ModelAdmin classes.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created')
    list_display_links = ('author', 'content')
    inlines = [
        PostImageInline,
        PostCommentInline
    ]
    readonly_fields = ('tags',)


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
