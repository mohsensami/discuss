from turtle import pos
from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify


class PostListView(View):
    form_class = PostCreateUpdateForm
    def get(self, request):
        form = self.form_class()
        posts = Post.objects.all()
        return render(request, 'post/index.html', {'posts': posts, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('post:index')


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'post/detail.html', {'post': post})


class PostDeleteView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('post:index')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('post:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'post/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post updated successfully', 'success')
            return redirect('post:detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    from_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.from_class()
        return render(request, 'post/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('post:detail', new_post.id, new_post.slug)
