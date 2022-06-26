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
        ordering = ['body']

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('post:detail', args=(self.id, self.slug))

