from django.shortcuts import render, redirect

# Create your views here.
from members.forms import SignupForm


def index(request):
    if request.user.is_authenticated:
        return redirect('posts:post-list')
    else:
        signupform = SignupForm()
        context = {
            'signupform': signupform
        }
        return render(request, 'index.html', context)
