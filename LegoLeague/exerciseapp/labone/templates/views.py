from django.http import HttpResponse
import re
from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('dashboard')  # Assuming 'dashboard' is the URL name for the dashboard page
    else:
        form = ExerciseForm()
    return render(request, 'addexercise.html', {'form': form})

@login_required
def workout_history(request):
    return render(request, 'workouthistory.html')