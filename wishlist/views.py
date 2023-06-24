from django.shortcuts import render, redirect
from django.views import View
from .models import Wishlist, Product
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from .serializers import WishlistSerializer

# Create your views here.


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Переопределили метод get_queryset
        wish_items = self.get_queryset().filter(product__id=request.data.get('product'))

        if wish_items: # Если продукт в избранном:
            wish_item = wish_items[0]
            if request.data.get('quantity'):
                wish_item.quantity += int(request.data.get('quantity'))
            else:
                wish_item.quantity += 1

        else:  # Если продукта ещё нет в избранном:
            product = get_object_or_404(Product, id=request.data.get('product'))
            if request.data.get('quantity'):
                wish_item = Wishlist(user=request.user, product=product, quantity=request.data.get('quantity'))
            else:
                wish_item = Wishlist(user=request.user, product=product)
        wish_item.save()

        return response.Response({'message': 'Product added to wishlist'}, status=201)

    def update(self, request, *args, **kwargs):
        wish_item = get_object_or_404(Wishlist, id=kwargs['pk'])
        if request.data.get('quantity'):
            wish_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(Product, id=request.data['product'])
            wish_item.product = product
        wish_item.save()

        return response.Response({'message': 'Product changed to wishlist'}, status=201)

    def destroy(self, request, *args, **kwargs):
        wish_item = self.get_queryset().get(id=kwargs['pk'])
        wish_item.delete()
        return response.Response({'message': 'Product deleted from wishlist'}, status=201)


class WishlistView(View):

    def get(self, request):
        if request.user.is_authenticated:
            wish = Wishlist.objects.filter(user=request.user).annotate(
                    total_price=F('product__price') * F('quantity')
                )
            return render(request, "wishlist/wishlist.html", {"data": wish})

        return redirect('login:login')


class WishlistViewAdd(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, id=request.user.id)
        wish_items = Wishlist.objects.filter(user=user, product=product)
        if not wish_items:
            wish_item = Wishlist(user=user, product=product)
            wish_item.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))  # Остаться на текущей странице
        #return redirect('shop:shop')


class WhishlistViewDelete(View):
    def get(self, request, product_id):
        wish_item = Wishlist.objects.get(user=request.user, product__id=product_id)
        wish_item.delete()

        return redirect('wishlist:wishlist')
