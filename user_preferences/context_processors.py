from .models import UserPreferences
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import os

def get_current_path(request):
    return {'current_path':request.path}


def get_user_preferences(request):
    if request.user.is_authenticated:
        user_preferences = UserPreferences.objects.get(user=request.user)
        context = {
        'user_prefs':user_preferences, 
        }
        f = os.path.join(settings.BASE_DIR, 'currency.json')
        with open(f, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]
            
        for currency in data:
            if currency['name'] == user_preferences.currency:
                symbol = currency['symbol']
                context['symbol']= symbol
        return context
    else:
        return {'context':'None'}
    


