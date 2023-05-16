from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from online_store_app.forms import UserForm, ProductForm, PurchaseForm, ReturnForm
from online_store_app.models import Product, Purchase, Return


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class BaseView(ListView):
    model = Product
    paginate_by = 4
    template_name = 'home_page.html'
    queryset = Product.objects.all()


class ProductUpdateView(AdminPassedMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock_availability']
    template_name = 'update_product.html'
    queryset = Product.objects.all()
    success_url = '/'
    login_url = 'login/'


class ProductCreateView(AdminPassedMixin, CreateView):
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/'
    login_url = 'login/'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'detail_product.html'
    extra_context = {'form': PurchaseForm()}
    login_url = 'login/'


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"product_id": self.kwargs['product_id'], "request": self.request}
        )
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        amount = form.cleaned_data['amount']
        product = form.product
        obj.product = product
        obj.user = self.request.user
        product.stock_availability -= amount
        cost = amount * product.price
        obj.user.wallet -= cost
        with transaction.atomic():
            obj.save()
            product.save()
            obj.user.save()
        messages.success(self.request, 'Purchase completed successfully!')
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return redirect('/')


class BasketDetailView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'basket.html'
    queryset = Purchase.objects.all()
    login_url = 'login/'
    extra_context = {'form': ReturnForm()}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ObjReturnCreateView(LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request, "purchase_id": self.kwargs['purchase_id']}
        )
        return kwargs

    def form_valid(self, form):
        obj_purchase = form.purchase
        obj_returns = Return(purchase=obj_purchase)
        obj_returns.save()
        messages.success(self.request, 'Return is done!!!, wait for admin confirmation')
        return redirect('/')

    def form_invalid(self, form):
        return redirect('/')


class SuperUserReturns(AdminPassedMixin, ListView):
    model = Return
    template_name = 'admin_returns.html'
    queryset = Return.objects.all()
    login_url = 'login/'


class AcceptReturnDeleteView(AdminPassedMixin, DeleteView):
    model = Purchase
    success_url = '/'

    def form_valid(self, form):
        self.object.product.stock_availability += self.object.amount
        self.object.user.wallet += self.object.amount * self.object.product.price
        with transaction.atomic():
            self.object.product.save()
            self.object.user.save()
            return super().form_valid(form=form)


class RejectReturnDeleteView(AdminPassedMixin, DeleteView):
    model = Return
    success_url = '/'


class Login(LoginView):
    http_method_names = ['get', 'post']
    template_name = 'login.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class Register(CreateView):
    form_class = UserForm
    template_name = 'register.html'
    success_url = '/'
