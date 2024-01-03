from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

class Home(models.Model):
    activity = models.CharField(max_length=100)
    startTime = models.TimeField()
    endTime = models.TimeField()

    def __str__(self):
        return f'{self.startTime} - {self.endTime}: {self.activity}'

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High'),
    ]

    category = models.CharField(max_length=255)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    duration = models.DurationField(default=timedelta(minutes=30))  # Adjust the default value as needed

    def get_absolute_url(self):
        return reverse('task', args=(str(self.id)))

class Session(models.Model):
	hourTimer= models.IntegerField()
	minuteTimer= models.IntegerField()

class Planner(models.Model):
	timeSlot= models.IntegerField()

class CalendarRow(models.Model):
    pass

class CalendarDay(models.Model):
    day_of_week = models.CharField(max_length=20)
    amount = models.IntegerField()
    row = models.ForeignKey(CalendarRow, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day_of_week} - {self.amount}"