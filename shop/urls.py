from django.urls import path
from .views import ShopView, ProductSingleView, CartView

app_name = 'shop'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('product/<int:product_id>/', ProductSingleView.as_view(), name='product'),
    path('product/', ProductSingleView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    ]

