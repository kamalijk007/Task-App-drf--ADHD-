from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta
# Create your models here.

class HabitModel(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, max_length=999)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def is_done_today(self):
        return self.dailyrecordmodel_set.filter(date=timezone.now().date()).exists()

    def __str__(self):
        return self.name

    @property
    def current_streak(self):
        today = timezone.now().date()
        # FIX: Changed order_messages to order_by
        records = self.dailyrecordmodel_set.filter(completed=True).order_by("-date")
        records_date = set(r.date for r in records)

        if not records_date:
            return 0

        # Logic: If not done today, start checking from yesterday
        check_date = today if today in records_date else today - timedelta(days=1)
        
        streak = 0
        while check_date in records_date:
            streak += 1
            check_date -= timedelta(days=1)

        return streak
    
    @property  # FIX: Added this missing property decorator
    def last_7_days(self):
        today = timezone.now().date()
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        record_dates = set(
            self.dailyrecordmodel_set.filter(
                date__in=days,
                completed=True
            ).values_list("date", flat=True)
        )
        return [day in record_dates for day in days]

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