from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)    # e.g., 'login', 'logout', 'course_view'
    timestamp = models.DateTimeField(auto_now_add=True)
    page_visited = models.CharField(max_length=255, blank=True, null=True)  # e.g., 'course_page', 'profile_page'

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'


    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


    


