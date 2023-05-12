import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils import timezone

from online_store_app.models import User, Product, Purchase, Return


class UserForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    class Meta:
        model = User
        fields = ("username", "wallet",)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()

        return user


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'img', 'stock_availability']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError('Amount must be greater than 0')
        return amount


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        if 'product_id' in kwargs:
            self.product_id = kwargs.pop('product_id')

        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        try:
            product = Product.objects.get(pk=self.product_id)
            self.product = product
            if self.request.user.wallet < amount * product.price:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Not enough money')

            if amount > product.stock_availability:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Not enough goods')

        except Product.DoesNotExist:
            self.add_error(None, "Error")
            messages.error(self.request, 'product is not found')


class ReturnForm(ModelForm):
    class Meta:
        model = Return
        fields = []

    def __init__(self, *args, **kwargs):
        if 'purchase_id' in kwargs:
            self.purchase_id = kwargs.pop('purchase_id')

        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        try:
            purchase = Purchase.objects.get(pk=self.purchase_id)
            buy_at = purchase.buy_at.astimezone(timezone.utc)
            time_now = timezone.now().astimezone(timezone.utc)
            correct_time = datetime.timedelta(minutes=3)
            allowed_time = buy_at + correct_time

            if time_now > allowed_time:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Too much time has passed')
            self.purchase = purchase

        except Purchase.DoesNotExist:
            self.add_error(None, "Error")
            messages.error(self.request, 'Purchase is not found')
