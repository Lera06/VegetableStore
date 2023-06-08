from django.urls import path
from .views import ShopView, ProductSingleView, CartView, ViewCartBuy, ViewCartAdd, ViewCartDelete

app_name = 'shop'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('product/<int:product_id>/', ProductSingleView.as_view(), name='product'),
    path('product/', ProductSingleView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('buy/<int:product_id>/', ViewCartBuy.as_view(), name='buy'),
    path('add/<int:product_id>/', ViewCartAdd.as_view(), name='add'),
    path('delete/<int:product_id>/', ViewCartDelete.as_view(), name='delete')

    ]

