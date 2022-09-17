from weakref import ref
from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from account.models import Relation
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SearchView(View):
    def get(self, request):
        posts = Post.objects.filter(body__icontains = request.GET['search'])
        return render(request, 'post/search.html', {'posts': posts})


class PostListView(View):
    form_class = PostCreateUpdateForm
    def get(self, request):
        form = self.form_class()
        users = User.objects.all()
        relations = Relation.objects.all()
        if request.user.is_authenticated:
            followed_people = Relation.objects.filter(from_user=request.user).values('to_user')
            posts = Post.objects.filter(
                user__in=followed_people
            ) | Post.objects.filter(user=request.user)
        else:
            posts = Post.objects.all()
        return render(request, 'post/index.html', {'posts': posts, 'users': users, 'relations': relations, 'form': form})

    @method_decorator(login_required)
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
    form_class = CommentCreateForm
    reply_form = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        if request.user.is_authenticated:
            vote = Vote.objects.filter(user=request.user, post=self.post_instance)
            if vote.exists():
                is_liked = True
            else:
                is_liked = False
        else:
            is_liked = True
        return render(request, 'post/detail.html', {'post': self.post_instance, 'comments': comments, 'form': self.form_class, 'reply':self.reply_form, 'is_liked':is_liked})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect('post:detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('post:index')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
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

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('post:detail', new_post.id, new_post.slug)



class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
        return redirect('post:detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post', 'success')
        return redirect('post:detail', post.id, post.slug)