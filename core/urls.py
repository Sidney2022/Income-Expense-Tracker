from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('dashboard', views.dashboard_overview, name='dashboard'),
    path('stats', views.expense_category_summary, name='stats'),
    path('terms-of-service', views.terms, name='terms'), 
    path('privacy-policy', views.policy, name='policy'), 
    
]