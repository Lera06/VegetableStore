from django.urls import path
from .views import WishlistView, WhishlistViewDelete, WishlistViewAdd

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),
    path('add_wish/<int:product_id>', WishlistViewAdd.as_view(), name='add_wish'),
    path('delete/<int:product_id>', WhishlistViewDelete.as_view(), name='delete'),
]