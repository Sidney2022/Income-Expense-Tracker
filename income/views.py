from django.shortcuts import render, redirect
from .models import UserIncome, Source
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from user_preferences.models import UserPreferences
from django.http import HttpResponse
import csv
import datetime
from django.http import JsonResponse


@login_required(login_url='/auth/login', redirect_field_name='next')
def all_income(request):
    income = UserIncome.objects.filter(owner=request.user)
    user_prefs = UserPreferences.objects.get(user=request.user)
    page_number = request.GET.get('page')
    paginator = Paginator(income, 2)
    page = paginator.get_page( page_number)
    context = {
        'all-income':income,
        'page':page,
        'user_prefs':user_prefs
    }
    return render(request, 'income/index-income.html', context)


class AddUserIncomeView(View):
    def get(self, request):
        sources = Source.objects.filter(user=request.user)
        
        return render(request, 'income/add-income.html', {'sources':sources})
    
    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        sources = Source.objects.all()
        context = {
            'fieldValues':request.POST ,
            'sources' :sources,
        }        
        if not amount or not description or not source :
            messages.error(request, 'fields cannot be blank')
            return render(request, 'income/add-income.html', context)
        if not date:
            income = UserIncome.objects.create(owner=request.user, amount=amount, source=source, description=description)
        else:
            income = UserIncome.objects.create(owner=request.user, amount=amount, source=source, description=description,date=date)
        income.save()
        messages.success(request, 'New Income object saved successfully')
        return redirect('add-income')


@login_required(login_url='/auth/login')
def income_detail(request, pk):
    income = UserIncome.objects.filter(owner=request.user, id=pk)
    if not income.exists():
        messages.error(request, 'income object not found')
        return redirect('/')
    income = UserIncome.objects.get(owner=request.user, id=pk)
    context = {
        'income':income
    }
    return render(request, 'income/income-detail.html', context)
  

class IncomeEdit(View):

    def get(self, request, pk):
        income = UserIncome.objects.filter(owner=request.user, id=pk)
        sources = Source.objects.all()
        if not income.exists():
            messages.error(request, 'income object not found')
            return redirect('/')
        income = UserIncome.objects.get(owner=request.user, id=pk)
        context = {
            'income':income,
            'sources':sources
        }
        return render(request, 'income/edit-income.html', context)
    
    def post(self, request, pk):
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        income= UserIncome.objects.filter(owner=request.user, id=pk)
        
        sources = Source.objects.all()
        if not income.exists():
            # return 404 page
            messages.error(request, 'income object not found')
            return redirect('/')
        else:
            income = UserIncome.objects.get(owner=request.user, id=pk)
        context = {
            'income':income,
            'sources':sources
        }
        if not amount or not description or not source :
            messages.error(request, 'fields cannot be blank')
            return render(request, 'income/add-income.html', context)
    
        income.amount=amount
        income.description=description
        income.source=source
        income.date=date
        income.save()
        messages.success(request, 'New income object saved successfully')
        return redirect(f'income-detail', pk=pk)
    
 
@login_required(login_url='/auth/login')   
def delete_income(request):
    pk = request.GET.get('id')
    income = UserIncome.objects.filter(owner=request.user, id=pk)
    if not income.exists():
        # return 404 page
        messages.error(request, 'you cannot delete requested data')
    income = UserIncome.objects.get(owner=request.user, id=pk)
    msg=income.description
    income.delete()
    messages.success(request, f'You have successfully deleted "{msg}" ')
    return redirect('all-income')


@login_required(login_url='/auth/login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']=f'attachment;filename=Income{datetime.datetime.now()}.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])
    user_income = UserIncome.objects.filter(owner=request.user)
    for income in user_income:
        writer.writerow([income.amount, income.description, income.source, f'{income.date}'])
    return response


@login_required(login_url='/auth/login')
def income_chart_data(request):
    date_today = datetime.date.today()
    no_nonths=6
    if request.method == 'POST':
        date_range_req = request.POST['date_range']
        print(date_range_req)
        if date_range_req == 'week':
            date_range = date_today-datetime.timedelta(days=7)
        elif date_range_req == 'month' :
            date_range =  date_today-datetime.timedelta(days=30)
        elif date_range_req == 'today':
            date_range = date_today-datetime.timedelta(days=1)
        elif  date_range_req ==  'year':
            date_range = date_today-datetime.timedelta(days=365)
        else:
            date_range = date_today-datetime.timedelta(days=30*no_nonths)
            
    # date_range = date_today-datetime.timedelta(days=30*no_nonths)
        
    income = UserIncome.objects.filter(owner=request.user)
    
    final_rep = {}
    def get_category(income):
        return income.source
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source=income.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount 
        return amount

    sources_list = list(set(map(get_category, income)))
    for x in income:
        for y in sources_list:
            final_rep[y]=get_income_source_amount(y) 
    labels=[k for k,v in final_rep.items()]
    data = [v for k,v in final_rep.items()]
    context = {
        'labels': labels,
        'data':data
    }
    return render (request, 'income/i-chart.html', context)


@login_required(login_url='/auth/login')
def add_sources(request):
    user=request.user
    sources = Source.objects.filter(user=user)
    if request.method == 'POST':
        source = request.POST['source']
        if Source.objects.filter(user=user, name=source).exists():
            messages.error(request, 'source already exists')
            return redirect('sources')
        source = Source.objects.create(user=user, name=source)
        source.save()
        messages.success(request, 'source added successfully')
        return redirect('add-income')
    return render(request, 'income/add-source.html', {'sources': sources})




