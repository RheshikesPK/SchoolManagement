from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from .forms import StudentForm,UserForm,BookForm,BorrowedBookForm,FeesForm,LoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from . models import User,Student,Book,LibraryMember,BorrowedBook,Fees
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

class AdmindashboardView(TemplateView):
    template_name = 'admin/admidashboard.html'

class AddStudentView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'admin/addstudentform.html'
    context_object_name = 'student'

    # If no student_id is passed, it's a new student, otherwise we're editing
    def get_object(self, queryset=None):
        student_id = self.kwargs.get('student_id', None)
        if student_id:
            return Student.objects.get(id=student_id)
        return None  # Return None for creating a new student
    
    def get_success_url(self):
        return self.request.path  # Redirect back to the same page after success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = self.get_object() is not None  # Determine if editing or adding
        return context

    
User = get_user_model()  # Reference to the custom User model

class AddStaffView(FormView, ListView):
    model = User
    template_name = 'admin/addteacher.html'
    form_class = UserForm
    context_object_name = 'user'
    success_url = reverse_lazy('dashboard:add_staff')  # URL to redirect after successful form submission

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
    


class ManageLibraryView(FormView):
    template_name = 'admin/library.html'
    form_class = BorrowedBookForm

    # Pass context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all BorrowedBook records and pass them to the template
        context['borrowed_books'] = BorrowedBook.objects.all()
        return context

    # Save the form data into the BorrowedBook model
    def form_valid(self, form):
        form.save()  # Save the form to the database
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.path  # Redirect back to the same page after success


class LibraryView(TemplateView):
    template_name = 'admin/library2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all books from the model
        context['books'] = Book.objects.all()
        context['library_members'] = LibraryMember.objects.all()
        return context

class StudentView(TemplateView):
    template_name = 'admin/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the selected class from GET request
        selected_class = self.request.GET.get('class_name')
        
        if selected_class:
            # Filter students by selected class
            context['students'] = Student.objects.filter(class_name=selected_class)
        else:
            # If no class is selected, display all students
            context['students'] = Student.objects.all()
        
        # Pass the selected class back to the template for re-rendering the dropdown
        context['selected_class'] = selected_class
        return context

class TeacherView(TemplateView):
    template_name = 'admin/teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all teachers from the database
        context['teachers'] = User.objects.all()
        return context

class AddBookView(CreateView):
    template_name = 'admin/addbook.html'
    form_class = BookForm
    success_url = reverse_lazy('dashboard:library')

    def form_valid(self, form):
        return super().form_valid(form)


class UpdateBookView(UpdateView):
    template_name = 'admin/addbook.html'
    form_class = BookForm
    success_url = reverse_lazy('dashboard:library')

    def get_object(self, **kwargs):
        book_id = self.kwargs.get('book_id')  # Fetch the 'book_id' from URL parameters
        return get_object_or_404(Book, id=book_id)

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        if book_id:
            book = self.get_object()  # Call get_object without parameters since it now uses self.kwargs
            form = self.form_class(instance=book)
        else:
            form = self.form_class()
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        # Check if we are editing an existing book
        book_id = self.kwargs.get('book_id')
        if book_id:
            book = self.get_object()  # Call get_object without parameters
            form = self.form_class(self.request.POST, instance=book)  # Bind the form to the existing book instance
            if form.is_valid():
                form.save()  # Save the edited book
        else:
            form.save()  # Create a new book
        return super().form_valid(form)
    
class AddToLibraryView(View):
    def get(self, request, student_id):
        # Get the student by ID or return 404 if not found
        student = get_object_or_404(Student, id=student_id)
        
        # Check if the student is already a library member
        if not LibraryMember.objects.filter(student=student).exists():
            # Create a new library member
            LibraryMember.objects.create(student=student)
            return HttpResponse(f'{student.name} is added a library member.')
        else:
            return HttpResponse(f'{student.name} is already a library member.')
        
    def get_success_url(self):
        return self.request.path  # Redirect back to the same page after success
    

class StudentDetailsView(TemplateView):
    template_name = 'admin/viewstudent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('id')  # Get the student ID from the URL
        student = get_object_or_404(Student, id=student_id)  # Fetch the student object from the database
        context['student'] = student  # Pass the student object to the template
        return context

class DeleteStudentView(View):
    def post(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        return redirect('dashboard:student')  
    

class DeleteLibraryMemberView(View):
    def post(self, request, member_id):
        member = get_object_or_404(LibraryMember, id=member_id)
        member.delete()
        return redirect('dashboard:library')  # Adjust as needed
    
class DeleteLibraryBookView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)  # Fetch the book using the book_id
        book.delete()  # Delete the book instance
        return redirect('dashboard:library')  # Redirect to the library page after deletion
    
class FeesView(TemplateView):
    template_name = 'admin/fees.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all fee records from the database
        context['fees_list'] = Fees.objects.all()
        return context

class AddFeesView(CreateView):
    model = Fees
    form_class = FeesForm
    template_name = 'admin/addfees.html'
    success_url = reverse_lazy('dashboard:fees')  # Redirect to the fees list page or any other page after success

    def form_valid(self, form):
        # Save the form data to the database
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle the case when the form is not valid
        return super().form_invalid(form)
    

class UpdateFeesView(UpdateView):
    template_name = 'admin/addfees.html'  # Change this to your desired template for updating fees
    form_class = FeesForm
    success_url = reverse_lazy('dashboard:fees')  # Redirect to the fees page after updating

    def get_object(self, **kwargs):
        fee_id = self.kwargs.get('fees_id')  # Fetch 'fees_id' from the URL
        return get_object_or_404(Fees, id=fee_id)

    def get(self, request, *args, **kwargs):
        fee_id = kwargs.get('fees_id')
        if fee_id:
            fee = self.get_object()  # Call get_object to retrieve the fee instance
            form = self.form_class(instance=fee)  # Bind the form to the existing fee instance
        else:
            form = self.form_class()  # Create a new form if no fee_id is provided
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        fee_id = self.kwargs.get('fees_id')  # Fetch 'fees_id' from the URL
        if fee_id:
            fee = self.get_object()  # Retrieve the existing fee instance
            form = self.form_class(self.request.POST, instance=fee)  # Bind the form to the existing fee instance
        else:
            form.save()  # Create a new fee if no fee_id is provided
        return super().form_valid(form)
    

class DeleteFeesView(View):
    def post(self, request, fees_id):
        fee = get_object_or_404(Fees, id=fees_id)  # Fetch the fees record using the fees_id
        fee.delete()  # Delete the fees instance
        return redirect('dashboard:fees')  # Redirect to the fees page after deletion
    

class LoginView(FormView):
    template_name = 'admin/login.html'  # Template for the login page
    form_class = LoginForm

    def form_valid(self, form):
        # Check if the user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('dashboard:admindash')  # Redirect to the dashboard if logged in

        # Get the cleaned data from the form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)  # Log the user in
            self.request.session['role'] = user.role  # Store the user's role in the session
            messages.success(self.request, 'Login successful!')
            return redirect('dashboard:admindash')  # Redirect to the dashboard or any other page
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Clear the session data
        messages.success(request, 'You have been logged out.')
        return redirect('dashboard:log')  # Redirect to the login page