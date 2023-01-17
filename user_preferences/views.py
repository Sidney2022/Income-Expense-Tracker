from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import UserPreferences
import os, json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from expense.models import Expense
import requests
from django.contrib.auth.models import User


@login_required(login_url='login')
def edit_preferences(request):
    user_pref = UserPreferences.objects.filter(user=request.user)
    if user_pref.exists():
            user_pref = UserPreferences.objects.get(user=request.user)
    else:
            user_pref= UserPreferences.objects.create(user=request.user)
            user_pref.save()
            
    if request.method == 'POST':
        currency = request.POST['currency']
        
        expense=Expense.objects.filter(owner=request.user)
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency}&from={user_pref.currency}&amount=1"
        api_key=''
        payload = {}
        headers= {
        "apikey": api_key
        }
        response = requests.request("GET", url, headers=headers, data = payload)

        status_code = response.status_code
        result = response.text
        result=json.loads(result)
        if expense.exists():
            for obj in expense:
                amt = result['result'] * float(obj.amount)
                obj.amount=round(amt, 3)
                obj.save()
            
        
        user_pref.currency=currency
        user_pref.save()
        messages.success(request, 'user preference changed succesfully')
        return redirect('edit-currency')
        # return render(request, 'prefs/index.html', {'user_pref':user_pref})
        
        
    f = os.path.join(settings.BASE_DIR, 'currency.json')
    with open(f, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]
               
        context = {
            'currencies':data,
            'user_pref':user_pref
        }
    
            
    return render(request, 'prefs/edit-preferences.html', context)


def apitest(request):
    import requests
    api_key=settings.FOREX_API_KEY
    url = "https://api.apilayer.com/exchangerates_data/symbols"

    payload = {}
    headers= {
    "apikey": api_key
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text
    result=json.loads(result)
    data = [({'name':k,'value':v}) for k,v in result['symbols'].items()]
    
    # return JsonResponse(result['symbols'])
    # return JsonResponse(result)
    return HttpResponse(data) 



def user_settings(request):
    user = User.objects.get(username=request.user)
    user_prefs = UserPreferences.objects.filter(user=request.user)
    context = {
        'user':user,
        'user_prefs':user_prefs
        
    }
    return render(request, 'prefs/user-prefs.html', context)

