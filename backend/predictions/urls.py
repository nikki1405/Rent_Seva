from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_rent, name='predict_rent'),
    path('history/', views.get_history, name='get_predictions_history'),
]