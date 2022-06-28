from venv import create
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'publish')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='uploads/', default='default.jpg', verbose_name='Image')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Active/DeActive')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Publish')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publish']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('post:detail', args=(self.id, self.slug))

    def like_count(self):
        return self.pvotes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'