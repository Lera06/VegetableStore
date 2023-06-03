from django.urls import path
from .views import IndexShopView, ContactView, AboutView

app_name = 'home'

urlpatterns = [
    path('', IndexShopView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
]