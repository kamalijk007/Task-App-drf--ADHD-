from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class HabitModel(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, max_length=999)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class DailyRecordModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(HabitModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'record', 'date'],
                name='unique_user_habit_daily'
            )
        ]

    def __str__(self):
        return f'{self.record.name} - {self.date}'