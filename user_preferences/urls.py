
from django.urls import path
from . import views



urlpatterns = [
    path('settings', views.edit_preferences, name='edit-settings' ),
    path('', views.user_settings, name='account-info')
]