from django.shortcuts import render
from django.views import View
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Sum, Case, When
from .models import Product, Discount, Cart
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect


# Create your views here.

# Функцмя для отображения страниц
def get_pages_list(page, max_pages):
    if max_pages < 5:
        return list(range(1, max_pages + 1))

    data = [1]
    if page > 3:
        data += ["..."]

    if 2 < page < max_pages - 1:
        data += list(range(page - 1, page + 2))
    elif page == 1:
        data += [2]
    elif page == 2:
        data += [2, 3]
    elif page == max_pages - 1:
        data += [page - 1, page]
    elif page == max_pages:
        data += [page - 1]

    if page + 2 < max_pages:
        data += ["..."]
    data += [max_pages]

    return data


class ShopView(View):

    def get(self, request):
        items_per_page = 2

        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        """Используем Subquery чтобы чтобы вытащить все скидки для используемых продуктов, 
        если скидок нет, то будет выведен None"""

        products = Product.objects.select_related('category').annotate(
            discount_value=Subquery(
                Discount.objects.filter(product_id=OuterRef('id')).values('value')
            ),
            price_before=F('price'),
            price_after=price_with_discount
        ).values('id', 'product_name', 'image', 'category', 'price_before', 'price_after', 'discount_value')

        category = request.GET.get("category", "All")
        if not category == "All":
            products = products.filter(category__category_name=category)  # имя модели__имя поля


        paginator = Paginator(products, items_per_page)
        page = int(request.GET.get('page', 1))
        items = paginator.get_page(page)

        max_pages = paginator.num_pages
        data_pages = get_pages_list(page, max_pages)

        return render(request, 'shop/shop.html',
                      {"data": items,
                       "category": category,
                       "page": page,
                       "next": items.has_next(),
                       "previous": items.has_previous(),
                       "max_pages": max_pages,
                       "data_pages": data_pages})


        # context = {'data': [{'name': 'Bell Pepper',
        #                      'discount': 30,
        #                      'price_before': 120.00,
        #                      'price_after': 80.00,
        #                      'id': 1,
        #                      'url': 'store/images/product-1.jpg'},
        #                     {'name': 'Strawberry',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'id': 2,
        #                      'url': 'store/images/product-2.jpg'},
        #                     {'name': 'Green Beans',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'id': 3,
        #                      'url': 'store/images/product-3.jpg'},
        #                      {'name': 'Purple Cabbage',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 4,
        #                       'url': 'store/images/product-4.jpg'},
        #                      {'name': 'Tomatoe',
        #                       'discount': 30,
        #                       'price_before': 120.00,
        #                       'price_after': 80.00,
        #                       'id': 5,
        #                       'url': 'store/images/product-5.jpg'},
        #                      {'name': 'Brocolli',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 6,
        #                       'url': 'store/images/product-6.jpg'},
        #                      {'name': 'Carrots',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 7,
        #                       'url': 'store/images/product-7.jpg'},
        #                      {'name': 'Fruit Juice',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 8,
        #                       'url': 'store/images/product-8.jpg'},
        #                      {'name': 'Onion',
        #                       'discount': 30,
        #                       'price_before': 120.00,
        #                       'price_after': 80.00,
        #                       'id': 9,
        #                       'url': 'store/images/product-9.jpg'},
        #                      {'name': 'Apple',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 10,
        #                       'url': 'store/images/product-10.jpg'},
        #                      {'name': 'Garlic',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 11,
        #                       'url': 'store/images/product-11.jpg'},
        #                      {'name': 'Chilli',
        #                       'discount': None,
        #                       'price_before': 120.00,
        #                       'id': 12,
        #                       'url': 'store/images/product-12.jpg'},
        #                                          ]
        #                                 }
        #
        # return render(request, 'shop/shop.html', context)


class ProductSingleView(View):

    def get(self, request, product_id=1):
        data = Product.objects.get(id=product_id)
        return render(request, 'shop/product-single.html', {"product": data})


    # def get(self, request, id):
    #
    #     data = {1: {'name': 'Bell Pepper',
    #                 'description': 'Bell Pepper',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-1.jpg'},
    #             2: {'name': 'Strawberry',
    #                 'description': 'Strawberry',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-2.jpg'},
    #             3: {'name': 'Green Beans',
    #                 'description': 'Green Beans',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-3.jpg'},
    #             4: {'name': 'Purple Cabbage',
    #                 'description': 'Purple Cabbage',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-4.jpg'},
    #             5: {'name': 'Tomatoe',
    #                 'description': 'Tomatoe',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-5.jpg'},
    #             6: {'name': 'Brocolli',
    #                 'description': 'Brocolli',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-6.jpg'},
    #             7: {'name': 'Carrots',
    #                 'description': 'Carrots',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-7.jpg'},
    #             8: {'name': 'Fruit Juice',
    #                 'description': 'Fruit Juice',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-8.jpg'},
    #             9: {'name': 'Onion',
    #                 'description': 'Onion',
    #                 'price': 120.00,
    #                 'rating': 5.0,
    #                 'url': 'store/images/product-9.jpg'},
    #             10: {'name': 'Apple',
    #                  'description': 'Apple',
    #                  'price': 120.00,
    #                  'rating': 5.0,
    #                  'url': 'store/images/product-10.jpg'},
    #             11: {'name': 'Garlic',
    #                  'description': 'Garlic',
    #                  'price': 120.00,
    #                  'rating': 5.0,
    #                  'url': 'store/images/product-11.jpg'},
    #             12: {'name': 'Chilli',
    #                  'description': 'Chilli',
    #                  'price': 120.00,
    #                  'rating': 5.0,
    #                  'url': 'store/images/product-12.jpg'}
    #       }
    #
    #     return render(request, 'shop/product-single.html', context=data[id])


class CartView(View):

    def get(self, request):
        if request.user.is_authenticated:
            user_cart = Cart.objects.filter(user=request.user).select_related('product')
            total_discount = Case(When(product__discount__value__gte=0,
                                       product__discount__date_begin__lte=timezone.now(),
                                       product__discount__date_end__gte=timezone.now(),
                                       then=F('total_price') * F('product__discount__value') / 100),
                                       default=0,
                                       output_field=DecimalField(max_digits=10, decimal_places=2)
                              )
            cart = user_cart.annotate(
            total_price=F('product__price') * F('quantity'),
            total_discount=total_discount,
            total_price_with_discount=F('total_price') - F('total_discount'),
        )

            sum_data = cart.aggregate(sum_price=Sum('total_price'),
                                      sum_discount=Sum('total_discount'),
                                      sum_price_with_discount=Sum('total_price_with_discount'))

            context = {"data": cart}
            context.update(sum_data)

            return render(request, 'shop/cart.html', context)
        return redirect("login:login")
        # cart = Cart.objects.filter(user=request.user).annotate(total_price=F('product__price') * F('quantity'))
        # return render(request, 'shop/cart.html', {"data": cart})

        #return render(request, 'shop/cart.html')


class ViewCartBuy(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, id=request.user.id)
        cart_items = Cart.objects.filter(user=user, product=product)
        if cart_items:
            cart_item = cart_items[0]
            cart_item.quantity += 1
        else:
            cart_item = Cart(user=user, product=product)
        cart_item.save()
        return redirect('shop:cart')

class ViewCartAdd(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, id=request.user.id)
        cart_items = Cart.objects.filter(user=user, product=product)
        if cart_items:
            cart_item = cart_items[0]
            cart_item.quantity += 1
        else:
            cart_item = Cart(user=user, product=product)
        cart_item.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        #return redirect('shop:shop')



class ViewCartDelete(View):
    def get(self, request, product_id):
        cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
        return redirect('shop:cart')

