from django.urls import path
from .views import ShopView, ProductSingleView, CartView

app_name = 'shop'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('product/<int:id>/', ProductSingleView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    ]