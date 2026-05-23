# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
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
            # HASH the password before saving
            "password": make_password(data["password"]),
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


@csrf_exempt
def login(request):
    data = json.loads(request.body)

    identifier = data["identifier"]  # username or email
    password = data["password"]

    try:
        # Find user by username OR email
        user = User.objects.get(
            Q(username=identifier) | Q(email=identifier)
        )

        # Compare raw password with hashed password
        if check_password(password, user.password):

            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "calories_goal": user.calories_goal,
                "gl_goal": user.gl_goal,
                "activity_goal": user.activity_goal,
                "bucket_balance": user.bucket_balance
            })

        return JsonResponse({
            "error": "Invalid credentials"
        }, status=401)

    except User.DoesNotExist:
        return JsonResponse({
            "error": "Invalid credentials"}, status=401)



