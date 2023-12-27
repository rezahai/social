from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.body[:20]}-{self.user}'

    def get_absolute_url(self):
        return reverse('home:detail', args=(self.id, self.slug))

    def like_count(self):
        return self.post_votes.count()

    def user_can_like(self, user):
        user_like = user.user_votes.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} -- {self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_votes')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'

