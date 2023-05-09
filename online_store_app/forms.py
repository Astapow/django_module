from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
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


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['amount']



class ReturnForm(ModelForm):
    class Meta:
        model = Return
        fields = ['purchase']
