from django.db import models
from django.utils import timezone

# Create your models here.

# Enums that are used within the classes are here.


class MeasurementUnit(models.IntegerChoices):
    PIECE = 0
    PLATE = 1
    GLASS = 2
    SPOON = 3
    CUP = 4
    SLICE = 5


class Mood(models.IntegerChoices):
    HORRIBLE = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3
    GREAT = 4


#  The independent domain classes are written here.

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    calories_goal = models.IntegerField()
    gl_goal = models.IntegerField()
    activity_goal = models.IntegerField()
    bucket_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Food(models.Model):
    name = models.CharField(max_length=50)
    calories_per_100 = models.IntegerField()
    gl_index = models.IntegerField()
    mass_per_descriptive_unit = models.IntegerField()
    unit = models.IntegerField(choices=MeasurementUnit.choices, default=MeasurementUnit.PIECE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=50)
    calories_burn_per_min = models.IntegerField()

    def __str__(self):
        return self.name


class DailyPlan(models.Model):
    date = models.DateField()
    weight = models.IntegerField()
    waist = models.IntegerField()
    chest = models.IntegerField()
    thighs = models.IntegerField()
    mood = models.IntegerField(choices=Mood, default=Mood.NEUTRAL)
    success = models.BooleanField()

    def __str__(self):
        return f"Daily plan on day {self.date}"


class Flower(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1024)
    water_required = models.IntegerField()

    def __str__(self):
        return self.name


# The dependent domain classes are written here.

class Meal(models.Model):
    daily_plan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.daily_plan} - {self.name}"


class Medicine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Down below, the associative classes are written


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.meal.name}: {self.food.name}"


class DailyPlanActivity(models.Model):
    daily_plan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    time = models.TimeField(default=timezone.now)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.daily_plan}: {self.activity}"


class DailyPlanMedicine(models.Model):
    daily_plan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.daily_plan}: {self.medicine}"


class UserFlower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    unlocked = models.BooleanField()

    def __str__(self):
        return f"{self.user}: {self.flower}"

