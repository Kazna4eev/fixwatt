from django import forms


class CartAddProductForm(forms.Form):
    # Поле для введення кількості
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
    )

    # Прапорець для позначення, чи потрібно перезаписати кількість (для використання у самому кошику)
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )