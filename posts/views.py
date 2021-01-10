from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


def index(request):
    post_list = Post.objects.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
                 request,
                 'index.html',
                 {'page': page,
                  'paginator': paginator
                  }
                  )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group,
         'posts': posts,
         'paginator': paginator,
         'page': page
         }
        )


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'post_new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'profile.html',
                  {'page': page,
                   'author': author,
                   'paginator': paginator}
                  )


def post_view(request, username, post_id):
    author = User.objects.get(username=username)
    text = Post._meta.get_field("text")
    post = get_object_or_404(Post, id=post_id, author=author)
    count = Post.objects.filter(author=author).select_related('author').count()
    return render(request, 'post.html', {
        'post': post,
        'author': author,
        'count': count,
        'post_id': post_id,
        'text': text
        }
        )


@login_required
def post_edit(request, username, post_id):
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author=author, id=post_id)
    form = PostForm(instance=post)
    if request.user == author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.save()
                return redirect("post", username=username, post_id=post_id)
        return render(
            request,
            'post_new.html',
            {'form': form, 'post': post, 'is_edit': True}
        )
    return redirect("post", username=username, post_id=post_id)
