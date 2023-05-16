"""
URL configuration for django_module project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from online_store_app.views import Login, Logout, Register, BaseView, ProductUpdateView, ProductCreateView, \
    ProductDetailView, BasketDetailView, SuperUserReturns, PurchaseCreateView, ObjReturnCreateView, \
    AcceptReturnDeleteView, RejectReturnDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('', BaseView.as_view(), name='home'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('show_product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('purchase/<int:product_id>/', PurchaseCreateView.as_view(), name='buy_product'),
    path('create_return/<int:purchase_id>', ObjReturnCreateView.as_view(), name='create_return'),
    path('accept_return/<int:pk>', AcceptReturnDeleteView.as_view(), name='accept_return'),
    path('reject_return/<int:pk>', RejectReturnDeleteView.as_view(), name='reject_return'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('basket/', BasketDetailView.as_view(), name='basket'),
    path('user_returns/', SuperUserReturns.as_view(), name='return'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
