from django.urls import path
from . import views

app_name = 'landlord'

urlpatterns = [
    # Registration and Login
    path('register/', views.register_landlord, name='register'),
    path('login/', views.login_landlord, name='login'),
    path('dashboard/', views.landlord_dashboard, name='dashboard'),
    path('logout/', views.logout_landlord, name='logout'),
    path('rooms/post/' , views.post_room, name= 'post_room'),
]