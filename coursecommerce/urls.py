"""
URL configuration for coursecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from courses.views import home, get_available_slots, save_appointment, save_info_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('get-available-slots/', get_available_slots, name='get_available_slots'),
    path('save-appointment/', save_appointment, name='save_appointment'),
    path('save-info-request/', save_info_request, name='save_info_request'),
]
