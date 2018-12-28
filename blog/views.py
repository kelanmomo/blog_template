from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from .forms import NewPostForm, CommentForm
from .models import Category, Post, Comment

# Create your views here.
def home(request):
    categorys = Category.objects.all()
    return render(request, 'home.html', {'categorys':categorys})

def category_list(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.all()
    queryset = category.posts.order_by('-post_date').annotate(replies=Count('title')-1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 15)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'category':category,'posts':posts, 'topics':topics})

# @login_required
def blog_posts(request, pk, blog_pk):
    blog = get_object_or_404(Post, tag__pk=pk, pk=blog_pk)
    session_key = 'viewed_topic_{}'.format(blog.pk)
    if not request.session.get(session_key, False):
        blog.views += 1
        blog.save()
        request.session[session_key] = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.message = form.cleaned_data.get('message')
            comment.create_by = request.user
            comment.post = blog
            comment.save()
            return render(request, 'blog_posts.html', {'blog':blog,'form':form})
    else:
        form = CommentForm()
    return render(request, 'blog_posts.html', {'blog':blog,'form':form})

def category_new(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method =='POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tag = category
            post.post_by = request.user
            post.text_body = form.cleaned_data.get('text_body')
            post.save()
            return redirect('category_list', pk=category.pk)
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'category':category, 'form':form})

def page_not_found(request):
    return render(request, 'page_not_found.html')