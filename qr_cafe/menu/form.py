from django import forms
from .models import Order, MenuItem

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('item', 'quantity', 'table_no')

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity
