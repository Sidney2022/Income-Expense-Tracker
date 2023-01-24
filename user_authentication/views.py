from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
# from django.core.mail import send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.template.loader import render_to_string
# # from .utils import account_activation_token
# from django.urls import reverse
from django.contrib import auth
from user_preferences.models import UserPreferences
from django.http import HttpResponse

class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        redirect_to= request.POST.get('next')
        usr = User.objects.filter(username=username)
        if not usr.exists():
            messages.error(request, 'invalid login credentials')
            return render(request, 'auth/login.html', {'redirect_to':redirect_to})

        usr = User.objects.get(username=username)
        if not usr.is_active:
            return HttpResponse('<h1>User is not active</h1>')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Welcome {username}. You are now logged in')
            if not redirect_to == 'None':
                return redirect(redirect_to)
            else:
                return redirect('/')
        else:
            messages.error(request, 'invalid login credentials')
            return render(request, 'auth/login.html', {'redirect_to':redirect_to})
    
    def get(self, request):
        redirect_to= request.GET.get('next')
        if request.user.is_authenticated :
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
        else:
            return render(request, 'auth/login.html', {'redirect_to':redirect_to})


class RegisterView(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues':request.POST
        }
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. try another')
            return render(request, 'auth/signup.html', context)
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'auth/signup.html', context)
        elif len(password) <  8 :
            messages.error(request, 'password must be a minimum of 8 characters ')
            return render(request, 'auth/signup.html', context)
        new_user = User.objects.create_user(username=username, email=email, password=password)
        # new_user.save()
#         new_user.is_active = False
        new_user.save()
        new_user_pref_object = UserPreferences.objects.create(user=new_user)
        new_user_pref_object.save()
        new_user_model=User.objects.get(username=username)
        auth.login(request, new_user_model)
        messages.error(request, 'Account created successfuly ')
        return redirect( '/')

    
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'user already has an account and is logged in')
            return redirect('/')
        return render(request, 'auth/signup.html')


@login_required(login_url='/auth/login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')


class VerificationView(View):
    pass
    # def get(self, request, uidb64, token):

    #     try:
    #         id = force_text(urlsafe_base64_decode(uidb64))
    #         user = User.objects.get(pk=id)

    #         if not account_activation_token.check_token(user, token):
    #             return redirect('login'+'?message='+'User already activated')

    #         if user.is_active:
    #             return redirect('login')
    #         user.is_active = True
    #         user.save()

    #         messages.success(request, 'Account activated successfully')
    #         return redirect('login')

    #     except Exception as ex:
    #         pass

    #     return redirect('login')

