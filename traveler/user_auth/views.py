from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required


def home_page(request):
    return render(request, 'main.html')


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'log_in.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account has created for {user}')
                return redirect('log_in')
        context = {'form': form}
        return render(request, 'register.html', context)


def log_out(request):
    logout(request)
    return redirect('home')


def user_page(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        form = request.user
        print(type(form))
        context = {'form': form}
        return render(request, 'user.html', context)
