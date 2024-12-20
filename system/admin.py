from django.contrib import admin
from .models import Company, CustomUser, WorkerProfile, RegistrationRequest, Payment


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_count')  # Какие поля отображать
    search_fields = ('name',)  # Поля для поиска

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_manager', 'is_worker', 'company')  # Какие поля отображать
    search_fields = ('username', 'company__name')  # Поля для поиска
    list_filter = ('is_manager', 'is_worker')  # Фильтры по полям

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'salary', 'phone_number', 'position', 'user')  # Какие поля отображать
    search_fields = ('first_name', 'last_name', 'phone_number')  # Поля для поиска
    list_filter = ('position',)  # Фильтры по должности


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company')
    search_fields = ('first_name', 'last_name', 'company__name')
    list_filter = ('company',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'worker', 'amount')  # Поля для отображения
    search_fields = ('worker__first_name', 'worker__last_name')  # Поля для поиска
    list_filter = ('date',)  # Возможность фильтрации по дате