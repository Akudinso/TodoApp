from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        task = request.POST['task']
        new_user = Todo(user=request.user, todo_name=task)
        new_user.save()
        
    all_todos = Todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 3:
            messages.error(request, 'Your password must be greater than 3')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'User with this username already exist!')
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User succesfully craeted, login now!')
        return redirect('login')
        
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'User does not exist!')
            return redirect('login')
        
        
    return render(request, 'todoapp/login.html', {})

@login_required
def deleteTask(request, name):
    get_todo = Todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def updateStatus(request, name):
    get_todo = Todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
