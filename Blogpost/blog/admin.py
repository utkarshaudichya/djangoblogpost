from django.contrib import admin
from blog.models import Post, Comment, UserProfile

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ('status', 'publish', 'created')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'body', 'created', 'updated', 'active']
    list_filter = ('active', 'created', 'updated')
    search_fields = ['name', 'email', 'body']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'dob', 'photo']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
