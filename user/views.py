from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'user/BASE.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Log the user in and redirect to the homepage
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Something went wrong during authentication')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'user/register.html')


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # print(self.request.POST)  # Print the POST data for debugging
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')