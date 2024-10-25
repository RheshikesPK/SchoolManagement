from django.shortcuts import render
from django.contrib.auth.models import AbstractUser,Group,Permission
from .forms import UserForm
from dashboard.models import User
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.urls import reverse_lazy
# Create your views here.
class RegStaffView(FormView, ListView):
    model = User
    template_name = 'admin/register.html'
    form_class = UserForm
    context_object_name = 'user'
    success_url = reverse_lazy('dashboard:log')  # URL to redirect after successful form submission

    def form_valid(self, form):
        # Create a new user instance with the cleaned data
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            role=form.cleaned_data['role'],
            gender=form.cleaned_data['gender'],
            phone=form.cleaned_data['phone'],
        )
        
        # Set the password and save the user
        user.set_password(form.cleaned_data['password'])  # Securely set the password
        user.save()  # Save the user to the database
        
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path  # Redirect back to the same page after success
    
