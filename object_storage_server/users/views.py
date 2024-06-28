from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        print(form.error_messages)
        print(form.errors)
        print(form.fields)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your account has been registred, Now you can log in!')
            return render("success")
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title': 'Registration'
    }
    return render(request, 'users/register.html', context)
