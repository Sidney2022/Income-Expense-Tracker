from django.urls import path
from . import views
from .views import IncomeSummary, ExpenseSummary
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.home, name='home-page'),
    path('dashboard', views.dashboard_overview, name='dashboard'),
    path('expense/stats', csrf_exempt(views.ExpenseSummary.as_view()), name='expense-stats'),
    path('terms-of-service', views.terms, name='terms'), 
    path('privacy-policy', views.policy, name='policy'), 
    path('contact', views.contact, name='contact'),
    path('income/stats', csrf_exempt(views.IncomeSummary.as_view()), name ='income-stats'),

]