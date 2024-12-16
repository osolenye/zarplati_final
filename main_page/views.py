from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('general_info')  # Или на страницу с общей информацией, если авторизован
    else:
        # Для неавторизованных пользователей показываем страницу с выбором действия
        return render(request, 'home.html')