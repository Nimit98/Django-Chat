from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserForm
from chat.models import UserList


def index(request):
    return render(request, 'login/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            username = user_form.save()
            username.set_password(username.password)
            username.save()

            # EXTRA

            user = User.objects.get(username=username.username)
            new_user = UserList(user=user, display_name=username.username)
            new_user.save()

            # TILL HERE
            registered = True
            login(request, user)
            return HttpResponseRedirect('/chat/')
        else:
            print(user_form.errors)
            return render(request, 'login/register.html', {'registered': registered, 'user_form': user_form})
    else:
        user_form = UserForm()
        return render(request, 'login/register.html', {'registered': registered, 'user_form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Acc not active')

        else:
            print("Someone tries to login and failed")
            return HttpResponse('invalid login details')

    else:
        return render(request, 'login/login.html', {})
