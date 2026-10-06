from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("posts/", views.all_posts, name="all-posts"),
    path("posts/create/", views.create_new_post, name="create-post"),
    path("posts/<slug:post_slug>/", views.view_post_detail, name="post-detail"),
]
