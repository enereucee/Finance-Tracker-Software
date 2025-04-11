from django.contrib import admin
from .models import UserActivity


# Register your models here.
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'page_visited')
    search_fields = ('user__username', 'activity_type', 'page_visited')
    list_filter = ('activity_type', 'timestamp')
