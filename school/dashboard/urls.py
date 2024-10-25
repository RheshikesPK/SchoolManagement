from django.urls import path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
app_name = 'dashboard'

urlpatterns = [
    # G1 accounts
    path('dash/', AdmindashboardView.as_view(), name='admindash'),  # Note the parentheses after `as_view`
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('add_staff/', AddStaffView.as_view(), name='add_staff'),
    path('manage_library/', ManageLibraryView.as_view(), name='manage_library'),
    path('library/', LibraryView.as_view(), name='library'),
    path('student/', StudentView.as_view(), name='student'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('add-to-library/<int:student_id>/', AddToLibraryView.as_view(), name='add_to_library'),
    path('student_details/<int:id>/', StudentDetailsView.as_view(), name='student_details'),
    path('edit_student/<int:student_id>/', AddStudentView.as_view(), name='edit_student'),
    path('students/<int:student_id>/delete/', DeleteStudentView.as_view(), name='delete_student'),
    path('members/<int:member_id>/delete/', DeleteLibraryMemberView.as_view(), name='delete_member'),
    path('book/<int:book_id>/delete/', DeleteLibraryBookView.as_view(), name='delete_book'),
    path('edit_book/<int:book_id>/', UpdateBookView.as_view(), name='edit_book'),
    path('fees/', FeesView.as_view(), name='fees'),
    path('add_fees/', AddFeesView.as_view(), name='add_fees'),
    path('edit_fees/<int:fees_id>/', UpdateFeesView.as_view(), name='edit_fees'),
    path('fees/<int:fees_id>/delete/', DeleteFeesView.as_view(), name='delete_fees'),
    path('', LoginView.as_view(), name='log'),
    path('logout/', LogoutView.as_view(), name='logout'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)