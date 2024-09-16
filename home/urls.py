from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from facedetector import settings
from .views import home,basic_info,other_details,biometric

urlpatterns = [
    path('', home, name='home'),
    path('api/basicinfo', basic_info, name='basicinfo'),
    path('api/otherdetails', other_details, name='otherdetails'),
    path('api/biometric', biometric, name='biometric'),
    # path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)