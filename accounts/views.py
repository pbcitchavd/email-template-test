from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model


# Create your views here.
def login_to_dashboard(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Willkommen {user.username} zurück.")
            return HttpResponseRedirect(reverse('app_phishing:employees'))
        else:
            messages.error(request, "Username und/oder Passwort nicht richtig.")
            ...

    return render(request, 'accounts/login_hacker.html')