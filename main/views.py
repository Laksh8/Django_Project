from django.shortcuts import render,redirect # HTML Rendering Or Redirecting
from .models import Portfolio,Details # Calling Tables form DataBase
from django.contrib.auth.models import User # calling built in user model
from django.contrib.auth.views import login_required# Login Security
from django.contrib import auth # Importing Authentication....
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.method == 'POST':
        res = redirect('home')
        res.set_cookie('name',request.POST['name'])
        value = Portfolio.objects.all()
        return render(request, 'main/home.html', {"values": value, 'cookie': res.cookies['name']})

    value = Portfolio.objects.all()
    return render(request,'main/home.html',{"values":value})

def signup(request):
    if request.method == 'POST':
        user = auth.authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'main/signup.html',{'error':'Username or Password is InCorrect'})
    return render(request,'main/signup.html',None)

@login_required
def Courses(request):
    return render(request,'main/Courses.html')

def contact(request):
    name='Harkit'
    return render(request,'main/contact.html',{"value":name})

def registration(request):
    name='Harkit'
    return render(request,'main/registration.html',{"value":name})


def display(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        value = Details()
        value.name = request.POST['name']
        value.phone = request.POST['phone']
        value.email = request.POST['email']
        value.user = request.user
        value.save()
    q = Details.objects.filter(user= request.user)
    return render(request,'main/display.html',{'values':q})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def delete(request,id):
    q = Portfolio.objects.filter(user=request.user,id=id)
    q.delete()
    return redirect('home')

@login_required
def updateportfolio(request,id):
    value = Portfolio.objects.filter(user=request.user,id=id)
    if request.method == 'GET':
        return render(request,'main/updateportfolio.html',{'value':value})
    if value:
        q = Portfolio()
        q.id = id
        q.title = request.POST['title']
        q.summary = request.POST['summary']
        q.image = request.FILES['image']
        q.time = value.time
        q.user = request.user
        q.save()
    return redirect('home')



def updatedetail(request,id):
    value = Details.objects.get(user=request.user,id=id)
    if request.method == 'GET':
        return render(request, 'main/updatedisplay.html', {'value': value})
    if value:
        q = Details()
        q.id = id
        q.name = request.POST['name']
        q.phone = request.POST['phone']
        q.email = request.POST['email']
        q.time = value.time
        q.user = request.user
        q.save()

    return redirect('display')


def deletedetail(request,id):
    value = Details.objects.get(user=request.user,id=id)
    value.delete()
    return redirect('display')


def session(request):
    if request.method == 'POST':
        request.session['name'] = request.POST['name']
    return render(request,'main/session.html',{'session':request.session.get('name')})

def displayportfolio(request,id):
    q = Portfolio.objects.get(id=id)
    return render(request,'main/displayportfolio.html',{'value':q})

def abc(request):
    return render(request,'main/abc.html',None)