from django.contrib import admin
from .models import Post, Comment, Category, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "category", "author", "publish", "status"]
    list_filter = ["status", "created","category", "publish", "author", "user_visit"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created", "updated"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["created", "updated"]
    search_fields = ["title"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]
    search_fields = ["user"]