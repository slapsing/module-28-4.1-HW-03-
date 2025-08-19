from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.template.loader import render_to_string
from django.urls import reverse

from DjangoProjectNewsPortal import settings
from django.core.cache import cache

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='author_profile'
    )
    rating = models.FloatField(default=0)
    subscribers = models.ManyToManyField(User, related_name='author_subscribers', blank=True)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating = self.posts.aggregate(pr=Sum('rating'))['pr'] or 0
        post_rating *= 3
        comment_rating = self.user.comments.aggregate(cr=Sum('rating'))['cr'] or 0
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating'))['pcr'] or 0
        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='category_subscribers')

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey('Author',
                               on_delete=models.CASCADE,
                               related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.FloatField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:150]}..." if len(self.content) > 150 else self.content

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        cache.delete(f'post-{self.pk}')



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')

    class Meta:
        unique_together = ('post', 'category')

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f'Комментарий от {self.user.username}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
