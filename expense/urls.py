from django.urls import path
from .import views
from .views import AddExpenseView, ExpenseEdit
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.expenses, name='all-expenses'),
    path('add', login_required(AddExpenseView.as_view()), name='add-expense'),
    path('<int:pk>/detail', views.expense_detail, name='expense-detail'),
    path('<int:pk>/edit', ExpenseEdit.as_view(), name='edit-expense'),
    path('delete', views.delete_expense, name='delete-expense'),
    path('export-data-csv', views.export_csv, name='export-data-csv'),
    
]