from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment, Vote
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PostSearchForm


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        form = self.form_class()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': form})


class PostDetailView(LoginRequiredMixin, View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.post_comments.filter(is_reply=False)
        form = self.form_class()
        form_reply = self.form_class_reply()
        can_like = False
        if request.user.is_authenticated and post.user_can_like(request.user):
            can_like = True
        return render(request, 'home/post_detail.html', {'post': post,
                                                         'comments': comments, 'form': form, 'form_reply': form_reply,
                                                         'can_like': can_like})

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        post = self.post_instance
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'your comment has been added!', 'success')
            return redirect('home:detail', post.id, post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'your post deleted successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'you can not delete this post', 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'you can not update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            return redirect('home:detail', post.id, post.slug)


class CreatePostView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/create_post.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'your post has been created', 'success')
            return redirect('home:detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.reply = comment
            reply.user = request.user
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply has been sent', 'success')
        return redirect('home:detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'liked this post', 'success')
        return redirect('home:detail', post.id, post.slug)
