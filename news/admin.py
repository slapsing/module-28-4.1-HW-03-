from django.contrib import admin
from django.contrib.admin import TabularInline

from news.models import Post

# @admin.register()
# class PostInline(TabularInline):
#     model = Post
#     fields = ('author', 'title', 'content', 'category', 'timestamp')
