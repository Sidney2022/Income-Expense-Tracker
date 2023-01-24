from django.shortcuts import render
from expense.models import Expense, Category
from income.models import UserIncome, Source
import datetime
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'landing.html')


@login_required(login_url='login')
def dashboard_overview(request):
    expenses = Expense.objects.filter(owner=request.user)
    income = UserIncome.objects.filter(owner=request.user)
    categories = Category.objects.all()
    
    total_income = 0
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount
    for item in income:
        total_income += item.amount
    date_today = datetime.date.today()
    no_nonths=2
    six_months_ago = date_today-datetime.timedelta(days=2)
    expense_this_month=Expense.objects.filter(owner=request.user,  date__gte=six_months_ago, date__lte=date_today)
    context = {
        'total_expenses':total_expenses,
        'total_income':total_income
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def expense_category_summary(request):
    date_today = datetime.date.today()
    no_nonths=6
    six_months_ago = date_today-datetime.timedelta(days=30*no_nonths)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=date_today)
    
    final_rep = {}
    def get_category(expense):
        return expense.category
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category=expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount 
        return amount

    category_list = list(set(map(get_category, expenses)))
    
    for x in expenses:
        for y in category_list:
            final_rep[y]=get_expense_category_amount(y)    
    return JsonResponse({'final_data':final_rep, })


def terms(request):
    return render(request, 'terms.html')


def policy(request):
    return render(request, 'policy.html')