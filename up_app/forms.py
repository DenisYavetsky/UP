from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # поля для заполнения
        fields = ('name', 'email', 'tel', 'address', 'comment', 'delivery')
        # псевдонимы полей для заполнения
        labels = {'name': 'Имя',
                  'email': 'e-mail',
                  'tel': 'Телефон',
                  'address': 'Адрес',
                  'comment': 'Коментарий',
                  'delivery': 'Доставка'}

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'cart-order-item-input'})
        self.fields['email'].widget.attrs.update({'class': 'cart-order-item-input'})
        self.fields['tel'].widget.attrs.update({'class': 'cart-order-item-input'})
        self.fields['address'].widget.attrs.update({'class': 'cart-order-item-textarea'})
        self.fields['comment'].widget.attrs.update({'class': 'cart-order-item-textarea'})
        self.fields['delivery'].widget.attrs.update({'class': 'cart-order-item-select'})
