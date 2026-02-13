from django.urls import path , include
from .views import DailyRecordView , HabitView , indexview
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r'habits', HabitView , basename='habit')
routers.register(r'records', DailyRecordView , basename='records')


urlpatterns = [
    path('', include(routers.urls)),
    path('index/', indexview , name='index')
]