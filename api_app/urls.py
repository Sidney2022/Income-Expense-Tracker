from django.urls import path
from . import views
from .views import IncomeView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.api_docs_home, name='api-landing'),
    path('income/', IncomeView.as_view(), name='user-income'),
    path('get-token', obtain_auth_token, name='get-token'),
    path('docs', views.api_docs, name='api-docs'),
]