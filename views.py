from rest_framework import viewsets 
from .models import UserActivity
from .serializers import UserActivitySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json 


# Create your views here.

class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer

def user_activities_view(request):
    list(UserActivity.objects.all()).values()
    return JsonResponse(activities, safe=False)


@csrf_exempt
@require_POST
def log_user_activity(request):
    data = json.loads(request.body)  # for now, just return what was sent 
    return JsonResponse({"status": "success", "data": data})

@csrf_exempt
@require_POST
def activity_summary(request):
    data = json.loads(request.body)  # for now, just return what was sent 
    return JsonResponse({"status": "success", "data": data})



# This view will be used to display the home page of the analytics dashboard.
def home_view(request):
    return HttpResponse("Welcome to the Analytics Dashboard!")