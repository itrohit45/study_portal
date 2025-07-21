from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.



def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        user = User.objects.create_user(username= username, email= email,password= password)
        user.save()

        subject = '🎓 Welcome to Student Study Portal, {username}!' 
        message = f'hi {username},\n\nthank you for registering at student study portal'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            messages.error(request, 'Registration successful, but email sending failed.')

        messages.success(request, 'You have registered successfully')
        return redirect('login')
            
    return render(request, 'users/signup.html')





class Login(View):
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate return username if credintials are correct else it return none
        user = authenticate(request,username = username,password = password)
        print(user)

        if user is not None:
            login(request,user)
            request.session['username'] = username
            return redirect('home')
        else:
            return HttpResponse('invalid username or password')
            

def logout_user(request):
    logout(request)
    return redirect('login')


class Myprofile(View):
    def get(self,request):
        user = request.user
        context = {
            'username': user.username, 
            'email': user.email,         
    }
        return render(request, 'users/myprofile.html', context)        





