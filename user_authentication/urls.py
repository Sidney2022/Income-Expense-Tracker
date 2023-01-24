from django.urls import path
from .views import LoginView, RegisterView, VerificationView
from . import views


urlpatterns = [
        path('login/', LoginView.as_view(), name='login'),
        path('signup', RegisterView.as_view(), name='signup'),
        path('logout', views.logout, name='logout'),
        path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
]