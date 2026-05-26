from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .models import User
import json


# =========================
# REGISTER USER
# =========================
@csrf_exempt
def create_user(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Only POST method allowed"
        }, status=405)

    try:
        data = json.loads(request.body)

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        calories_goal = data.get("calories_goal")
        gl_goal = data.get("gl_goal")
        activity_goal = data.get("activity_goal")

        # =========================
        # VALIDATION
        # =========================

        if not username:
            return JsonResponse({
                "error": "Username is required"
            }, status=400)

        if not email:
            return JsonResponse({
                "error": "Email is required"
            }, status=400)

        if not password:
            return JsonResponse({
                "error": "Password is required"
            }, status=400)

        if len(password) < 6:
            return JsonResponse({
                "error": "Password must be at least 6 characters"
            }, status=400)

        # Username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "error": "Username already exists"
            }, status=400)

        # Email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "error": "Email already exists"
            }, status=400)

        # Numeric validation
        try:
            calories_goal = int(calories_goal)
            gl_goal = int(gl_goal)
            activity_goal = int(activity_goal)
        except:
            return JsonResponse({
                "error": "Goals must be numeric"
            }, status=400)

        # =========================
        # CREATE USER
        # =========================

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            calories_goal=calories_goal,
            gl_goal=gl_goal,
            activity_goal=activity_goal,
            bucket_balance=0
        )

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "message": "User created successfully"
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)


# =========================
# LOGIN
# =========================
@csrf_exempt
def login(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Only POST method allowed"
        }, status=405)

    try:
        data = json.loads(request.body)

        identifier = data.get("identifier", "").strip()
        password = data.get("password", "")

        if not identifier or not password:
            return JsonResponse({
                "error": "Identifier and password are required"
            }, status=400)

        try:
            user = User.objects.get(
                Q(username=identifier) | Q(email=identifier)
            )

        except User.DoesNotExist:
            return JsonResponse({
                "error": "Invalid credentials"
            }, status=401)

        if not check_password(password, user.password):
            return JsonResponse({
                "error": "Invalid credentials"
            }, status=401)

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "calories_goal": user.calories_goal,
            "gl_goal": user.gl_goal,
            "activity_goal": user.activity_goal,
            "bucket_balance": user.bucket_balance
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)


# =========================
# UPDATE USER
# =========================
@csrf_exempt
def update_user(request, user_id):

    if request.method != "PUT":
        return JsonResponse({
            "error": "Only PUT method allowed"
        }, status=405)

    try:
        data = json.loads(request.body)

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return JsonResponse({
                "error": "User not found"
            }, status=404)

        # Only numerical fields can be updated
        calories_goal = data.get("calories_goal", user.calories_goal)
        gl_goal = data.get("gl_goal", user.gl_goal)
        activity_goal = data.get("activity_goal", user.activity_goal)
        bucket_balance = data.get("bucket_balance", user.bucket_balance)

        # Validation
        try:
            calories_goal = int(calories_goal)
            gl_goal = int(gl_goal)
            activity_goal = int(activity_goal)
            bucket_balance = int(bucket_balance)
        except:
            return JsonResponse({
                "error": "Numeric fields must contain numbers"
            }, status=400)

        user.calories_goal = calories_goal
        user.gl_goal = gl_goal
        user.activity_goal = activity_goal
        user.bucket_balance = bucket_balance

        user.save()

        return JsonResponse({
            "message": "User updated successfully",
            "id": user.id,
            "calories_goal": user.calories_goal,
            "gl_goal": user.gl_goal,
            "activity_goal": user.activity_goal,
            "bucket_balance": user.bucket_balance
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)