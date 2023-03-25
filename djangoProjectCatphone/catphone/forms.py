from django import forms
from .models import Catsphone, Supplier, Order, Pos_order, Chegue
import re
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CatphoneForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        min_length=2,
        strip=True,
        label='Название фрукта')
    description = forms.CharField(
        max_length=150,
        min_length=2,
        strip=True,
        label='Описание фрукта',
        initial="Описание",
        widget=forms.Textarea)
    price = forms.FloatField(
        min_value=1,
        # step_size=10,
        label='Цена фрукта',
        initial=40)
    date_update = forms.DateField(
        label='Дата обновления',
        # widget=forms.SelectDateWidget,
        help_text='Укажите дату обновления')
    photo = forms.ImageField(
        required=False,
        label='Фотография котофона')

    # required=True - обязательное поле
    # max_length - Максимальная длина текста
    # min_length - Минимальная длина текста
    # max_value - Максимальное значение числа
    # min_value - Минимальное значение числа
    # step_size - Шаг при установки числового значения

    # Стили
    # label - Вывод названия
    # widget - Указание типа поля
    # initial - Значение по умолчанию
    # help_text - Подсказка под полем


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        # fields = '__all__' # Использование всех полей (не рекомендуется)
        fields = ['title', 'agent_name', 'agent_firstname', 'agent_patronymic', 'exist']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'floatingInput',
                    'placeholder': 'Название'
                }
            ),
            'agent_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя'
                }
            ),
            'agent_firstname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия'
                }
            ),
            'agent_patronymic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество'
                }
            ),
            'exist': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Поле не должно начинаться с цифры')
        return title


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control', },
        )
    )
    content = forms.CharField(
        label='Тело письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 11, },
        )
    )

