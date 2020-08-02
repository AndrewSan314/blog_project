from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView)

from .forms import PostForm, CommentForm
from .models import Post, Comment


# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm


class PostDraftsList(LoginRequiredMixin, ListView):
    model = Post
    redirect_field_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('-create_date')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
