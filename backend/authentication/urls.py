from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refresh-token/', views.refresh_token, name='refresh_token'),
    path('profile/', views.get_user_profile, name='user_profile'),
    path('history/', views.get_estimates_history, name='estimates_history'),
]