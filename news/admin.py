from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.get_fields()]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
