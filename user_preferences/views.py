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
from django.views import View



@login_required(login_url='login')
def edit_preferences(request):
    user_pref = UserPreferences.objects.get(user=request.user)
    
    if request.method == 'POST':
        currency = request.POST['currency']
        email_sub = request.POST.get('email-subscription', False)
        sms = request.POST.get('sms-notification', False)
        user_pref = UserPreferences.objects.get(user=request.user)
     
        if sms == 'on' or sms == 'True' or sms == 'true':
            user_pref.sms_notification = True
        else:
            user_pref.sms_notification = False
        if email_sub == 'on' or email_sub == 'True' or email_sub == 'true':
            user_pref.email_subscription = True
        else:
            user_pref.email_subscription = False
     
        
        user_pref.currency=currency
        user_pref.save()
        messages.success(request, 'user preference changed succesfully')
        return redirect('edit-settings')
      
        
        
    f = os.path.join(settings.BASE_DIR, 'currency.json')
    with open(f, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]
               
        context = {
            'currencies':data,
            'user_pref':user_pref
        }
            
    return render(request, 'prefs/edit-preferences.html', context)


@login_required(login_url='login')
def user_settings(request):
    user = User.objects.get(username=request.user)
    user_prefs = UserPreferences.objects.get(user=request.user)
    context = {
        'user':user,
        'user_prefs':user_prefs
        
    }
    return render(request, 'prefs/user-prefs.html', context)


class ProfileSettings(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        user_prefs = UserPreferences.objects.get(user=request.user)
        context = {
            'user':user,
            'user_prefs':user_prefs
            
        }
        return render(request, 'prefs/edit-profile.html', context)
    
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        image=request.FILES.get('image')
        if not len(username) > 3:
            messages.error(request, 'username muset be contain at least 3 characters')
            return redirect('edit-profile')
        elif not username:
            messages.error(request, 'username cannot be empty')
            return redirect('edit-profile')
        elif not email:
            messages.error(request, 'email cannot be empty')
            return redirect('edit-profile')
        user = User.objects.filter(username=request.user)
        user_prefs=UserPreferences.objects.filter(user=request.user)
        
        if user.exists() and user_prefs.exists():
            user = User.objects.get(username=request.user)
            user_prefs=UserPreferences.objects.get(user=request.user)
            user.username = username
            user.email=email
            if image:
                user_prefs.image=image
                user_prefs.save()
            user.save()
            messages.success(request, 'profile has been updated')
            return redirect('account-info')
        return render(request, 'prefs/edit-profile.html')
