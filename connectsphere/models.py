from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class registration(models.Model):
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Example field
    address = models.TextField(null=True, blank=True)  # Example field
    bio = models.TextField(null=True, blank=True)  # Bio field
    # reset_token = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    class Meta:
        db_table = 'connectsphere_registration'  # Map to connectsphere_registration table

    def __str__(self):
        return self.username

#post
class Post(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'connectsphere_posts'

    def __str__(self):
        return f"{self.user.username} - {self.content[:30] if self.content else 'Media Post'}"

#like and comments

class Like(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'connectsphere_likes'
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.post.content[:20]}"

class Comment(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'connectsphere_comments'

    def __str__(self):
        return f"{self.user.username} commented: {self.content[:20]}"

#follow
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        db_table = 'connectsphere_follow'  # Custom table name
        unique_together = ('follower', 'followed')  # Ensure that a user can only follow another user once

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

#notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'connectsphere_notifications'  # Custom table name
        ordering = ['-created_at']  # Order notifications by creation time in descending order

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

class Message(models.Model):
    sender = models.ForeignKey(registration, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(registration, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'connectsphere_message'

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.content[:30]}"
    

