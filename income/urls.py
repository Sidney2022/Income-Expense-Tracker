from django.urls import path
from .import views
from .views import AddUserIncomeView, IncomeEdit
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.all_income, name='all-income'),
    path('add', login_required(AddUserIncomeView.as_view()), name='add-income'),
    path('<int:pk>/detail', views.income_detail, name='income-detail'),
    path('<int:pk>/edit', IncomeEdit.as_view(), name='edit-income'),
    path('delete', views.delete_income, name='delete-income'),
    path('export-income-data-csv', views.export_csv, name='income-data-csv'),
    path('sources', views.add_sources, name='sources'),
    path('chart', views.income_chart_data, name='chart',),
    
]