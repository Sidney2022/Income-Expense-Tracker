from django.shortcuts import render, redirect
from expense.models import Expense, Category
from income.models import UserIncome, Source
import datetime
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.conf import settings
from django.views import View
import json

def home(request):
    return render(request, 'landing.html')


@login_required(login_url='login')
def dashboard_overview(request):
    expenses = Expense.objects.filter(owner=request.user)
    income = UserIncome.objects.filter(owner=request.user)
    categories = Category.objects.all()
    
    def get_current_month_data(table): 
        date_today = datetime.date.today()
        current_month = date_today-datetime.timedelta(days=30)
        queryset_this_month=table.objects.filter(owner=request.user,  date__gte=current_month, date__lte=date_today)
        previous_month = date_today-datetime.timedelta(days=60)
        queryset_last_month=table.objects.filter(owner=request.user,  date__gte=previous_month, date__lte=current_month)
        cur_month_amt = 0
        last_month_amt = 0
        for obj in queryset_this_month:
            cur_month_amt += obj.amount
        for obj in queryset_last_month:
            last_month_amt += obj.amount
        
        return {"cur_month_amt":cur_month_amt, "last_month_amt":last_month_amt}

    def income_percentage():
        values = get_current_month_data(UserIncome)
        cur_month_amt = values['cur_month_amt']
        last_month_amt = values['last_month_amt']
        n = cur_month_amt-last_month_amt
        if  last_month_amt == 0:
            percent_change = cur_month_amt
        else:
            percent_change = (100*n)/last_month_amt
        if cur_month_amt < last_month_amt:
            context['income_icon_class'] = 'danger'
            context['income_icon'] = 'down'
            context['income_percent_change'] = -percent_change
        elif cur_month_amt > last_month_amt:
            context['income_icon_class'] = 'success'
            context['income_icon'] = 'up'
            context['income_percent_change'] = percent_change
        else:
            context['icon_class'] = 'success'
            
    def expense_percentage():
        values = get_current_month_data(Expense)
        cur_month_amt = values['cur_month_amt']
        last_month_amt = values['last_month_amt']
        n = cur_month_amt-last_month_amt
        if  last_month_amt == 0:
            percent_change = cur_month_amt
        else:
            percent_change = (100*n)/last_month_amt
        if cur_month_amt > last_month_amt:
            context['expense_icon_class'] = 'danger'
            context['expense_icon'] = 'down'
            context['expense_percent_change'] = -percent_change
        elif cur_month_amt < last_month_amt:
            context['expense_icon_class'] = 'success'
            context['expense_icon'] = 'up'
            context['expense_percent_change'] = percent_change
        else:
            context['icon_class'] = 'success'

    total_income = 0
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount
    for item in income:
        total_income += item.amount
    context = {
        'total_expenses':total_expenses,
        'total_income':total_income,
    }
    income_percentage()
    expense_percentage()
    return render(request, 'dashboard.html', context)


class ExpenseSummary(View):
    def get(self, request, *args, **kwargs):
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
    
    def post(self, request, *args, **kwargs):
        date_today = datetime.date.today()
        data=json.loads(request.body)
        user_time_pref = int(data['time_range'])
        date_filter_range = date_today-datetime.timedelta(days=user_time_pref)
        expenses = Expense.objects.filter(owner=request.user, date__gte=date_filter_range, date__lte=date_today)
        
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


class IncomeSummary(View):
    def get(self, request, *args, **kwargs):
        
        date_today = datetime.date.today()
        no_nonths=6
        time_range = date_today-datetime.timedelta(days=30*no_nonths)
        income = UserIncome.objects.filter(owner=request.user, date__gte=time_range, date__lte=date_today)
        
        final_rep = {}
        def get_source(income):
            return income.source
        def get_income_category_amount(source):
            amount = 0
            filtered_by_source=income.filter(source=source)
            for item in filtered_by_source:
                amount += item.amount 
            return amount

        source_list = list(set(map(get_source, income)))
        
        for x in income:
            for y in source_list:
                final_rep[y]=get_income_category_amount(y)    
        return JsonResponse({'final_data':final_rep, })
    
    def post(self, request, *args, **kwargs):
        
        date_today = datetime.date.today()
        data=json.loads(request.body)
        user_time_pref = int(data['time_range'])
        
        date_filter_range = date_today-datetime.timedelta(days=user_time_pref)
        income = UserIncome.objects.filter(owner=request.user, date__gte=date_filter_range, date__lte=date_today)
        
        final_rep = {}
        def get_source(income):
            return income.source
        def get_income_category_amount(source):
            amount = 0
            filtered_by_source=income.filter(source=source)
            for item in filtered_by_source:
                amount += item.amount 
            return amount

        source_list = list(set(map(get_source, income)))
        
        for x in income:
            for y in source_list:
                final_rep[y]=get_income_category_amount(y)    
        print("som")
        return JsonResponse({'final_data':final_rep, })
    

def terms(request):
    return render(request, 'terms.html')


def policy(request):
    return render(request, 'policy.html')


def error_404(request, exception):
    return render(request, '404.html')


def contact(request):
    
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        email_subj = request.POST['subject']
        msg = request.POST['message']
        message = f"""
            name : {name}
            msg : {msg}
            email : {email}
            subj : {email_subj}
        """
        try:
            send_mail(email_subj, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False,)
        except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return redirect ("/")
    return JsonResponse({"json":"this page only allows post requests"})
                
        