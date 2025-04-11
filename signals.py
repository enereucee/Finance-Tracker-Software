from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, action_type='login')

@receiver(user_logged_out)
def log_user_logged(sender, user, **kwargs):
    UserActivity.objects.create(user=user, action_type='logout')
