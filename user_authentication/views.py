from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        redirect_to= request.POST.get('next')
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
        if request.user.is_authenticated:
            return redirect('/')
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
        new_user.save()
        auth.login(request, new_user)
        messages.error(request, 'Account created successfuly ')
        return redirect(request, '/')

    
    def get(self, request):
        return render(request, 'auth/signup.html')


@login_required(login_url='/auth/login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')