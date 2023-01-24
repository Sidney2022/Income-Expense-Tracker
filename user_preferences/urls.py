
from django.urls import path
from . import views
from .views import ProfileSettings
from django.contrib.auth.decorators import login_required
from django.views import View

urlpatterns = [
    path('settings', views.edit_preferences, name='edit-settings' ),
    path('', views.user_settings, name='account-info'),
    path('profile', login_required(ProfileSettings.as_view()), name='edit-profile'),
]