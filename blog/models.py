from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    tag = models.ForeignKey(Category, related_name='posts')
    text_body = models.TextField(max_length=100000)
    post_date = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User, related_name='posts')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.text_body, safe_mode='escape'))

class Comment(models.Model):
    message = models.CharField(max_length=10000)
    create_by = models.ForeignKey(User, related_name='comments')
    create_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments')

    def __str__(self):
        return self.message
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
    
