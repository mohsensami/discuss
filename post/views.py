from django.shortcuts import render
from django.views import View
from .models import Post


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'post/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'post/detail.html', {'post': post})
