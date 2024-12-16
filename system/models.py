from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании")
    employee_count = models.PositiveIntegerField(default=0, verbose_name="Количество сотрудников")

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_worker = models.BooleanField(default=False, verbose_name="Рабочий")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Компания")

class WorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    position = models.CharField(max_length=255, verbose_name="Должность")


class RegistrationRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='registration_requests')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company.name}"


class Payment(models.Model):
    date = models.DateField(default=now)  # Дата выдачи
    worker = models.ForeignKey('WorkerProfile', on_delete=models.CASCADE, related_name='payments')  # Ссылка на работника
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма выплаты

    def save(self, *args, **kwargs):
        # Заполняем сумму зарплатой из профиля работника
        if not self.amount:
            self.amount = self.worker.salary
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.worker.first_name} {self.worker.last_name} - {self.amount} ({self.date})"