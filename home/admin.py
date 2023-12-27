from django.contrib import admin
from .models import Post, Comment, Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote)
