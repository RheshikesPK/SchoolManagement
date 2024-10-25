from django import forms
from .models import Student,Book,BorrowedBook,Fees
from .models import User
from django.contrib.auth.models import Group, Permission

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'class_name', 'gender', 'email', 'phone', 'password', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'class_name': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
        }


    # Ensures email is validated properly
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Enter a valid email address.")
        return email


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'role', 'gender', 'email', 'phone', 'password', 'groups', 'user_permissions']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'issued_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'borrowed_by', 'borrowed_date', 'returned_date', 'status']
        widgets = {
            'borrowed_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'returned_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }


class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['student', 'amount', 'status', 'payment_date', 'due_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }