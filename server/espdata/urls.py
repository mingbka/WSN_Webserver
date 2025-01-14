from django.urls import path
from . import views

urlpatterns = [
    path('api/receive-data/', views.receive_data, name='receive_data'),
    path('display-data/', views.display_data, name='display_data'),
    path('daily_report/', views.daily_report, name='daily_report'),
]
