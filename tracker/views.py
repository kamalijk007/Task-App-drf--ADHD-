from django.shortcuts import render
from .serializers import HabitSerializer,DailyRecordSerializer

from .models import HabitModel,DailyRecordModel
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated 
# Create your views here.

class HabitView(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return HabitModel.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class DailyRecordView(viewsets.ModelViewSet):
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return DailyRecordModel.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

def indexview(request):
    return render(request, 'tracker/index.html')