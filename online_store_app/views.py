from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from online_store_app.forms import UserForm, ProductForm, PurchaseForm
from online_store_app.models import Product, Purchase, Return


class BaseView(ListView):
    model = Product
    paginate_by = 4
    template_name = 'home_page.html'
    queryset = Product.objects.all()


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock_availability']
    template_name = 'update_product.html'
    queryset = Product.objects.all()
    success_url = '/'
    login_url = 'login.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/'
    login_url = 'login.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'detail_product.html'
    extra_context = {'form': PurchaseForm()}
    login_url = 'login.html'


class ProductBuyCreate(CreateView):
    http_method_names = ['post']
    form_class = PurchaseForm
    success_url = '/'


    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.product = Product.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        obj.save()
        return super().form_valid(form=form)


class BasketDetailView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'basket.html'
    queryset = Purchase.objects.all()
    login_url = 'login.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SuperUserReturns(LoginRequiredMixin, ListView):
    model = Return
    template_name = 'admin_returns.html'
    queryset = Return.objects.all()
    login_url = 'login.html'


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
