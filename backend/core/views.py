from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .models import User, DailyPlan, Food, Activity, Meal, MealFood, DailyPlanActivity, DailyPlanMedicine
from .serializers import DailyPlanSerializer, FoodSerializer, ActivitySerializer
from datetime import date, timedelta
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
            "bucket_balance": user.bucket_balance,
            "daily_plan_generated": user.daily_plan_generated
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
            "bucket_balance": user.bucket_balance,
            "daily_plan_generated": user.daily_plan_generated
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)


# =========================
# GENERATE DAILY PLAN
# =========================

@csrf_exempt
def generate_daily_plan(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User not found"},
            status=404
        )

    today = date.today()

    # Prevent duplicates for the same day
    if DailyPlan.objects.filter(user=user, date=today).exists():
        return JsonResponse(
            {"error": "Daily plan for today already exists"},
            status=400
        )

    yesterday = today - timedelta(days=1)

    previous_plan = DailyPlan.objects.filter(
        user=user,
        date=yesterday
    ).first()

    if previous_plan:
        weight = previous_plan.weight
        waist = previous_plan.waist
        chest = previous_plan.chest
        thighs = previous_plan.thighs
    else:
        # Choose appropriate defaults
        weight = 0
        waist = 0
        chest = 0
        thighs = 0

    daily_plan = DailyPlan.objects.create(
        user=user,
        date=today,
        weight=weight,
        waist=waist,
        chest=chest,
        thighs=thighs,
    )

    return JsonResponse({
        "message": "Daily plan created",
        "daily_plan_id": daily_plan.id
    })

# =========================
# SHOW THE CURRENT DAILY PLAN
# =========================
@api_view(["GET"])
def show_current_daily_plan(request, user_id):
    try:
        daily_plan = DailyPlan.objects.get(
            user_id=user_id,
            date=date.today()
        )
    except DailyPlan.DoesNotExist:
        return Response(
            {"error": "Daily plan not found"},
            status=404
        )

    serializer = DailyPlanSerializer(daily_plan)
    return Response(serializer.data)

# =========================
# FETCH ALL FOODS
# =========================

@api_view(["GET"])
def fetch_all_foods(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


# =========================
# FETCH ALL ACTIVITIES
# =========================

@api_view(["GET"])
def fetch_all_activities(request):
    activities = Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


# =========================
# ADD MEALS TO A DAILY PLAN
# =========================

@api_view(["POST"])
def add_meals(request, daily_plan_id):
    data = request.data

    meal = Meal.objects.create(
        daily_plan_id=daily_plan_id,
        name=data["name"],
        time=data["time"]
    )

    save_meal_foods(meal, data["meal_foods"])

    return Response({"id": meal.id})

@api_view(["PUT"])
def update_meal(request, meal_id):
    data = request.data

    meal = Meal.objects.get(id=meal_id)

    meal.name = data["name"]
    meal.time = data["time"]
    meal.save()

    MealFood.objects.filter(meal=meal).delete()

    save_meal_foods(meal, data["meal_foods"])

    return Response({"id": meal.id})

@api_view(["DELETE"])
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    # also deletes MealFood automatically if FK is CASCADE
    meal.delete()

    return Response(
        {"message": "Meal deleted successfully"},
        status=status.HTTP_200_OK
    )

def save_meal_foods(meal, meal_foods):
    for item in meal_foods:
        MealFood.objects.create(
            meal=meal,
            food_id=item["food_id"],
            quantity=item["quantity"]
        )

# =========================
# ADD ACTIVITIES TO A DAILY PLAN
# =========================

@api_view(["POST"])
def add_activities(request, daily_plan_id):
    data = request.data

    activity = DailyPlanActivity.objects.create(
        daily_plan_id=daily_plan_id,
        activity_id=data["activity_id"],
        time=data["time"],
        duration=data["duration"]
    )

    return Response(
        {
            "id": activity.id,
            "message": "Activity created successfully"
        },
        status=status.HTTP_201_CREATED
    )

@api_view(["PUT"])
def update_activity(request, daily_plan_activity_id):
    data = request.data

    activity = get_object_or_404(
        DailyPlanActivity,
        id=daily_plan_activity_id
    )

    activity.activity_id = data["activity_id"]
    activity.time = data["time"]
    activity.duration = data["duration"]

    activity.save()

    return Response(
        {
            "id": activity.id,
            "message": "Activity updated successfully"
        }
    )

@api_view(["DELETE"])
def delete_activity(request, daily_plan_activity_id):
    activity = get_object_or_404(DailyPlanActivity, id=daily_plan_activity_id)

    activity.delete()

    return Response(
        {"message": "Activity deleted successfully"},
        status=status.HTTP_200_OK
    )
# =========================
# ADD MEDICATION INTAKES TO A DAILY PLAN
# =========================

@api_view(["POST"])
def add_medicine_intakes(request, daily_plan_id):
    data = request.data

    medicine = DailyPlanMedicine.objects.create(
        daily_plan_id=daily_plan_id,
        medicine_id=data["medicine_id"],
        time=data["time"]
    )

    return Response(
        {
            "id": medicine.id,
            "message": "Medicine intake created successfully"
        },
        status=status.HTTP_201_CREATED
    )

@api_view(["DELETE"])
def delete_medicine_intake(request, medicine_intake_id):
    medicine = get_object_or_404(DailyPlanMedicine, id=medicine_intake_id)

    medicine.delete()

    return Response(
        {"message": "Medicine intake deleted successfully"},
        status=status.HTTP_200_OK
    )