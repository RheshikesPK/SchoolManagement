from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,Group,Permission

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    
    CLASS_CHOICES = [
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10'),
        ('Class +1', 'Class +1'),
        ('Class +2', 'Class +2'),
    ]
    
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(validators=[EmailValidator()])  # EmailField ensures correct email format
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)  # Password will be masked in the form
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    issued_date = models.DateField()

    def __str__(self):
        return self.name
    

class LibraryMember(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)  # Each student can be a member only once
    member_since = models.DateField(auto_now_add=True)  # The date the student became a library member
    membership_status = models.CharField(
        max_length=10,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ],
        default='Active'
    )
    books_issued = models.PositiveIntegerField(default=0)  # Track how many books the member has issued

    def __str__(self):
        return f'{self.student.name} - Library Member'
    

class BorrowedBook(models.Model):
    STATUS_CHOICES = [
        ('overdue', 'Overdue'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Links to the Book model
    borrowed_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    returned_date = models.DateField(null=True, blank=True)  # Allow null/blank if not returned yet
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='overdue')

    def __str__(self):
        return f"{self.borrowed_by.name} - {self.book.name}"


class Fees(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # Foreign key to Student model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    def __str__(self):
        return f'{self.student.name} - {self.status}'