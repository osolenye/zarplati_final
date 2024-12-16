from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Company, WorkerProfile, RegistrationRequest, Payment
from .forms import CompanyForm, ManagerRegistrationForm, WorkerRegistrationForm, WorkerUserForm, RegistrationRequestForm


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
    # if not request.user.is_manager:
    #     return redirect('home')  # Только менеджер может регистрировать работников

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


def create_registration_request(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем на главную после подачи запроса
    else:
        form = RegistrationRequestForm()

    return render(request, 'create_registration_request.html', {'form': form})

@login_required
def view_registration_requests(request):
    # if not request.user.is_manager:
    #     return redirect('home')  # Ограничиваем доступ только для менеджеров

    requests = RegistrationRequest.objects.all()
    return render(request, 'view_registration_requests.html', {'requests': requests})


@login_required
def company_workers(request):
    # if not request.user.is_manager:
    #     return redirect('home')  # Только менеджер может просматривать работников

    workers = WorkerProfile.objects.filter(user__company=request.user.company)

    # Обрабатываем запрос на выплату зарплаты
    if request.method == "POST":
        worker_id = request.POST.get('worker_id')  # Получаем ID работника
        worker = get_object_or_404(WorkerProfile, id=worker_id)

        # Создаем запись о выплате
        payment = Payment(worker=worker, amount=worker.salary)
        payment.save()

        return redirect('company_workers')  # Перезагружаем страницу с актуальными данными

    return render(request, 'company_workers.html', {'workers': workers})


@login_required
def view_payments(request):
    # if not request.user.is_manager:
    #     return redirect('home')  # Только менеджер может просматривать выплаты

    payments = Payment.objects.filter(worker__user__company=request.user.company)
    return render(request, 'view_payments.html', {'payments': payments})


@login_required
def general_info(request):
    # Получаем компанию, к которой привязан пользователь (администратор или работник)
    company = request.user.company

    # Получаем информацию о компании
    company_info = {
        'name': company.name,
        'employee_count': company.employee_count,
    }

    # Получаем все выплаты для работников этой компании, если пользователь - работник
    payments = []
    if not request.user.is_manager:  # Если не администратор
        payments = Payment.objects.filter(worker__user=request.user)

    context = {
        'company_info': company_info,
        'payments': payments,
        'is_manager': request.user.is_manager,  # Проверяем, админ ли пользователь
    }

    return render(request, 'general_info.html', context)