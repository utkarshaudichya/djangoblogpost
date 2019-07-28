from blog.models import Post
from django import template
register = template.Library()
from django.db.models import Count

@register.simple_tag(name='mytag')
def total_posts():
    post = Post.objects.filter(status='published')
    return post.count()

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=15):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
