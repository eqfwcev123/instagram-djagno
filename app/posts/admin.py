from django.contrib import admin

# Register your models here.
from posts.models import PostComment, Post, PostImage, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLike(admin.ModelAdmin):
    pass
