from django.db import models
from user.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100,default='')
    content = models.CharField(max_length=500,default='')
    image = models.ImageField(upload_to='post_image/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author.username} likes {self.post.title}'