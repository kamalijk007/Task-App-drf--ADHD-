from rest_framework import serializers
from .models import HabitModel , DailyRecordModel
from datetime import date

class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done_today = serializers.BooleanField(read_only=True)
    current_streak = serializers.IntegerField(read_only=True)
    last_7_days = serializers.ListField(child=serializers.BooleanField(),read_only=True)
    class Meta:
        model = HabitModel
        fields = ['id','owner','name','created','description','is_done_today', 'current_streak', 'last_7_days']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=HabitModel.objects.all(),
                fields=['owner','name'],
                message='You Already have a habit of this name!'
            )
        ]


class DailyRecordSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.DateField(read_only=True, default=serializers.CreateOnlyDefault(date.today))
    class Meta:
        read_only_fields = ['date']
        model = DailyRecordModel
        fields = ['id','record','date','completed','owner']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=DailyRecordModel.objects.all(),
                fields=['owner','record','date'],
                message='The record already exists'
            )
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['record'].queryset = HabitModel.objects.filter(owner=request.user)