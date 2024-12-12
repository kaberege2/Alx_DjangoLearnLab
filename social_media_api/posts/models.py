from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Custom user model

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

#Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # Many-to-one relationship with Pos
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments") # Many-to-one relationship with User
    content = models.TextField()       # The text content of the comment
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the comment was last updated

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

# Like model to track which user liked which post
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']  # A user can like a post only once

    def __str__(self):
        return f'{self.user} likes {self.post.title}'