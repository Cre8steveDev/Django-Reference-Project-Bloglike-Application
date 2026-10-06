from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def home_view(request):
    posts = list(Post.objects.select_related("author")[:3])
    featured_post = posts[0] if posts else None
    return render(
        request,
        "main/home.html",
        {
            "featured_post": featured_post,
            "latest_posts": posts,
        },
    )


def all_posts(request):
    posts = Post.objects.select_related("author")
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
            | Q(author__name__icontains=query)
        )

    if category:
        posts = posts.filter(category=category)

    return render(
        request,
        "posts/posts.html",
        {
            "posts": posts,
            "query": query,
            "selected_category": category,
            "categories": Post.CATEGORY_CHOICES,
        },
    )


@login_required(login_url="login")
def create_new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post has been published.")
        return redirect(post.get_absolute_url())

    return render(request, "posts/create_post.html", {"form": form})


def view_post_detail(request, post_slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=post_slug)
    related_posts = (
        Post.objects.select_related("author")
        .filter(category=post.category)
        .exclude(pk=post.pk)[:2]
    )

    return render(
        request,
        "posts/post_detail.html",
        {
            "post": post,
            "related_posts": related_posts,
        },
    )
