from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    # Приховані поля для Ref-ідентифікаторів
    city_ref = forms.CharField(widget=forms.HiddenInput(), required=True)
    warehouse_ref = forms.CharField(widget=forms.HiddenInput(), required=True)

    # Поля для відображення та введення (AJAX)
    city_name = forms.CharField(
        label="Місто",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Почніть вводити назву міста...',
            'id': 'id_city_name',
            'autocomplete': 'off'
        })
    )

    warehouse_name = forms.CharField(
        label="Відділення Нової Пошти",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Спочатку оберіть місто...',
            'id': 'id_warehouse_name',
            'autocomplete': 'off',
            'disabled': 'disabled'
        })
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city_ref', 'warehouse_ref', 'city_name', 'warehouse_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['city_ref', 'warehouse_ref']:
                field.widget.attrs.update({'class': 'form-control'})