from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.core.paginator import Paginator
from django.conf import settings


@login_required(login_url='/auth/login', redirect_field_name='next')
def expenses(request):
    expenses = Expense.objects.filter(owner=request.user)
    page_number = request.GET.get('page')
    paginator = Paginator(expenses, 2)
    page = paginator.get_page( page_number)
    context = {
        'expenses':expenses,
        'page':page
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
        print(f"values are amount-{amount}, description-{description}, category-{category}, date-{date} ")
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
        print(pk)
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
        print(expense.id,expense.description)
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


