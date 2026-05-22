# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
import json

# Create your views here.

# Here are written all the operations related to users


@csrf_exempt
def create_user(request):
    data = json.loads(request.body)

    user, created = User.objects.update_or_create(
        username=data["username"],
        defaults={
            "email": data["email"],
            "password": data["password"],
            "calories_goal": data["calories_goal"],
            "gl_goal": data["gl_goal"],
            "activity_goal": data["activity_goal"],
            "bucket_balance": 0
        }
    )

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "created": created
    })