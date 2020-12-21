from django.contrib import messages
from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth 

# Create your views here.
def register(request):
    if request.method == 'POST' :
        fname = request.POST['f_name']
        lname = request.POST['l_name']
        username = request.POST['username']
        pswd = request.POST['pswd']
        pswd2 = request.POST['pswd2']
        email = request.POST['email']
        
        if pswd == pswd2:
            if User.objects.filter(username=username).exists():
                messages.info(request , 'Username taken')
                return redirect('register') 
            elif User.objects.filter(email=email).exists():
                print('email has taken')
                return redirect('register') 
            else:
                user = User.objects.create_user(username=username, password=pswd , email=email , first_name = fname , last_name =lname)
                user.save();
                print('user created')
                return redirect('login')

        else:
            print('password not matching')
        return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        pswd = request.POST['pswd']

        user = auth.authenticate(username=username , password=pswd)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request , 'invalid credentials')
            return redirect('login')


    else:
        return render(request, 'login.html')

