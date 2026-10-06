from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "body", "author__email", "author__name")
    prepopulated_fields = {"slug": ("title",)}
