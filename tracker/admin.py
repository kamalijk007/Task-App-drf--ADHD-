from django.contrib import admin
from .models import HabitModel,DailyRecordModel
# Register your models here.


admin.site.register(HabitModel)
admin.site.register(DailyRecordModel)