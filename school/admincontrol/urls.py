from django.urls import path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
app_name = 'admincontrol'

urlpatterns = [
    # G1 accounts
    path('', RegStaffView.as_view(), name='reg_staff'),
 


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)