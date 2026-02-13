from rest_framework import serializers
from .models import HabitModel , DailyRecordModel
from datetime import date

class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = HabitModel
        fields = ['owner','name','created','description']
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
        fields = ['record','date','completed','owner']
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