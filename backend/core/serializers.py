# core/serializers.py
from rest_framework import serializers
from .models import DailyPlan, Meal, DailyPlanActivity, DailyPlanMedicine

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class DailyPlanActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPlanActivity
        fields = "__all__"


class DailyPlanMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPlanMedicine
        fields = "__all__"


class DailyPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(source="meal_set", many=True, read_only=True)
    activities = DailyPlanActivitySerializer(source="dailyplanactivity_set", many=True, read_only=True)
    medicines = DailyPlanMedicineSerializer(source="dailyplanmedicine_set", many=True, read_only=True)

    class Meta:
        model = DailyPlan
        fields = "__all__"