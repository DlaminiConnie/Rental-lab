"""
URL configuration for RentalApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant/', include('tenant.urls')),
    path('landlord/', include('landlord.urls')), 
    path('rooms/', include('rooms.urls')),
]

# Serve images from the landlord templates folder
urlpatterns += [
    path('landlord/templates/landlord/images/<path:path>', serve, {'document_root': 'landlord/templates/landlord/images'}),
]