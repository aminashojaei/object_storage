from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            token = default_token_generator.make_token(user)
            uid = user.pk
            verification_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')

            send_mail(
                'Account Activation',
                f'Click the link to activate your account: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect(f'{reverse("verify_account_sent")}?email={user.email}')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title': 'Registration'
    }
    return render(request, 'users/register.html', context)


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'verify_account_invalid.html')


def verify_account_sent(request):
    context = {
        'email': request.GET.get('email'),
        'title': 'Verify Account'
    }
    return render(request, 'users/verify_account_sent.html', context)
