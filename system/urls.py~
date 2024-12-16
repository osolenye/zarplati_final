from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Регистрация и другие кастомные пути
    path('register/company/', views.register_company, name='register_company'),
    path('register/manager/', views.register_manager, name='register_manager'),
    path('register/worker/', views.register_worker, name='register_worker'),

    # Вход и выход
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]