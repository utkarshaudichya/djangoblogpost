from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# class CustomManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status='published')

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (('draft','Draft'), ('published','Published'))
    title = models.CharField(max_length=264)
    slug = models.SlugField(max_length=264, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='draft')
    # objects = CustomManager()
    tags = TaggableManager()
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id,
                                            self.publish.year,
                                            self.publish.strftime('%m'),
                                            self.publish.strftime('%d'),
                                            self.slug])
    def get_post_id(self):
        return reverse('like_post', args=[self.id])

# Models related to comments section
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=32)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'Commented by {} on {}'.format(self.name, self.post)

# Model related to User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Profile', null=True, blank=True)
    sex = models.CharField(max_length=6, verbose_name='Sex', default='male')
    phone = models.BigIntegerField(verbose_name='Mobile', null=True)
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    def __str__(self):
        return 'Profile of user {}'.format(self.user.username)
