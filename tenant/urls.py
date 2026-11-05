from django.urls import path
from . import views

app_name = 'tenant'

urlpatterns = [
    path('register/', views.register_tenant, name='register'),
    path('login/', views.login_tenant, name='login'),
    path('dashboard/', views.tenant_dashboard, name='dashboard'),
]