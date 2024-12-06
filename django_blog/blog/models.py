from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager  # Import TaggableManager

#Post Model.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()  # TaggableManager to manage tags

    def __str__(self):
        return self.title

#Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # Many-to-one relationship with Pos
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Many-to-one relationship with User
    content = models.TextField()       # The text content of the comment
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the comment was last updated

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
