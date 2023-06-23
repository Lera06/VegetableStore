from django.shortcuts import render, redirect
from django.views import View
from .models import Wishlist, Product
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.


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
