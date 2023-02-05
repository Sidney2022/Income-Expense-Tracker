from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.core.paginator import Paginator
from django.conf import settings
from user_preferences.models  import UserPreferences
from django.http import HttpResponse, JsonResponse
import csv
import datetime

@login_required(login_url='/auth/login', redirect_field_name='next')
def expenses(request):
    expenses = Expense.objects.filter(owner=request.user)
    user_prefs = UserPreferences.objects.get(user=request.user)

    page_number = request.GET.get('page')
    paginator = Paginator(expenses, 10)
    page = paginator.get_page( page_number)
    context = {
        'expenses':expenses,
        'page':page,
        'user_prefs':user_prefs,
    }

    return render(request, 'expenses/index-expense.html', context)


class AddExpenseView(View):
    def get(self, request):
        categories = Category.objects.all()
        
        return render(request, 'expenses/add-expenses.html', {'categories':categories})
    
    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        context = {
            'fieldValues':request.POST 
        }        
        if not amount or not description or not category :
            messages.error(request, 'fields cannot be blank')
            return render(request, 'expenses/add-expenses.html', context)
        if not date:
            expense = Expense.objects.create(owner=request.user, amount=amount, category=category, description=description)
        else:
            expense = Expense.objects.create(owner=request.user, amount=amount, category=category, description=description,date=date)
        expense.save()
        messages.success(request, 'New Expense object saved successfully')
        return redirect('add-expense')

@login_required(login_url='/auth/login', redirect_field_name='next')
def expense_detail(request, pk):
    expense = Expense.objects.filter(owner=request.user, id=pk)
    if not expense.exists():
        messages.error(request, 'expense object not found')
        return redirect('/')
    expense = Expense.objects.get(owner=request.user, id=pk)
    context = {
        'expense':expense
    }
    return render(request, 'expenses/expense-detail.html', context)


class ExpenseEdit(View):

    def get(self, request, pk):
        expense = Expense.objects.filter(owner=request.user, id=pk)
        categories = Category.objects.all()
        if not expense.exists():
            messages.error(request, 'expense object not found')
            return redirect('/')
        expense = Expense.objects.get(owner=request.user, id=pk)
        context = {
            'expense':expense,
            'categories':categories
        }
        return render(request, 'expenses/edit-expense.html', context)
    
    def post(self, request, pk):
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        expense= Expense.objects.filter(owner=request.user, id=pk)
        
        categories = Category.objects.all()
        if not expense.exists():
            # return 404 page
            messages.error(request, 'expense object not found')
            return redirect('/')
        else:
            expense = Expense.objects.get(owner=request.user, id=pk)
        context = {
            'expense':expense,
            'categories':categories
        }
        if not amount or not description or not category :
            messages.error(request, 'fields cannot be blank')
            return render(request, 'expenses/add-expenses.html', context)
    
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date
        expense.save()
        messages.success(request, 'New Expense object saved successfully')
        return redirect(f'expense-detail', pk=pk)
    
    
@login_required(login_url='/auth/login', redirect_field_name='next') 
def delete_expense(request):
    pk = request.GET.get('id')
    expense = Expense.objects.filter(owner=request.user, id=pk)
    if not expense.exists():
        # return 404 page
        messages.error(request, 'you cannot delete requested data')
    expense = Expense.objects.get(owner=request.user, id=pk)
    msg=expense.description
    expense.delete()
    messages.success(request, f'You have successfully deleted "{msg}" ')
    return redirect('all-expenses')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']=f'attachment;filename=Expenses{datetime.datetime.now()}.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses = Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, f'{expense.date}'])
    return response

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


def stats_view(request):
    return render(request, 'expenses/stats.html')



def add_category(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        new_category = request.POST['category']
        if Category.objects.filter(user=request.user, name=new_category).exists():
            messages.error(request, 'category already exists')
            return redirect('add-category')
        new_category = Category.objects.create(user=request.user, name=new_category)
        new_category.save()
        messages.success(request, 'new category added successfully')
        return redirect('add-expense')
    return render(request, 'expenses/add-category.html', {'categories':categories})