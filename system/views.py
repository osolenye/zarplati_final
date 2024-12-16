from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Company, WorkerProfile
from .forms import CompanyForm, ManagerRegistrationForm, WorkerRegistrationForm, WorkerUserForm

def register_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CompanyForm()
    return render(request, 'register_company.html', {'form': form})

def register_manager(request):
    if request.method == "POST":
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = True
            user.save()
            return redirect('login')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'register_manager.html', {'form': form})

@login_required
def register_worker(request):
    if not request.user.is_manager:
        return redirect('home')  # Только менеджер может регистрировать работников

    if request.method == "POST":
        user_form = WorkerUserForm(request.POST)
        profile_form = WorkerRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_worker = True
            user.company = request.user.company
            user.save()

            worker_profile = profile_form.save(commit=False)
            worker_profile.user = user
            worker_profile.save()

            company = request.user.company
            company.employee_count += 1
            company.save()

            return redirect('home')
    else:
        user_form = WorkerUserForm()
        profile_form = WorkerRegistrationForm()

    return render(request, 'register_worker.html', {'user_form': user_form, 'profile_form': profile_form})
