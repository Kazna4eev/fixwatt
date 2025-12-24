from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")
    first_name = forms.CharField(required=True, label="Ім'я")
    last_name = forms.CharField(required=True, label="Прізвище")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # === МАГІЯ ТУТ: Додаємо стилі Bootstrap автоматично ===
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None  # (Опціонально) Прибираємо підказки, щоб не засмічувати дизайн


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Електронна пошта")
    first_name = forms.CharField(required=True, label="Ім'я")
    last_name = forms.CharField(required=True, label="Прізвище")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # === І ТУТ ТЕЖ: Щоб профіль теж був красивим ===
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'