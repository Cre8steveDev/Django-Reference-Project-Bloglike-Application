from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "gender")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "name",
                    "birthday",
                    "location",
                    "bio",
                    "avatar",
                    "gender",
                    "portfolio_url",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
