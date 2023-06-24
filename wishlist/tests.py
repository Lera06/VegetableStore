from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import Wishlist
from shop.models import Product, Category
from .serializers import WishlistSerializer
from .views import WishlistViewSet


# Create your tests here.
class WishlistViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category_name="Vegetables")
        self.product = Product.objects.create(product_name='Test Product', description='Test Description',
                                              price=10.0, category=category)

    def test_create_wish_item(self):
        request = self.factory.post('/wish/', {'product': self.product.id})
        request.user = self.user
        view = WishlistViewSet.as_view({'post': 'create'})

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product added to wishlist')
        self.assertEqual(Wishlist.objects.count(), 1)

    def test_update_wish_item(self):
        wish_item = Wishlist.objects.create(user=self.user, product=self.product)
        request = self.factory.put(f'/wish/{wish_item.id}/', {'quantity': 5})
        request.user = self.user
        view = WishlistViewSet.as_view({'put': 'update'})

        response = view(request, pk=wish_item.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product changed to wishlist')
        wish_item.refresh_from_db()
        self.assertEqual(wish_item.quantity, 5)

    def test_delete_wish_item(self):
        wish_item = Wishlist.objects.create(user=self.user, product=self.product)
        request = self.factory.delete(f'/wish/{wish_item.id}/')
        request.user = self.user
        view = WishlistViewSet.as_view({'delete': 'destroy'})

        response = view(request, pk=wish_item.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product deleted from wishlist')
        self.assertEqual(Wishlist.objects.count(), 0)


class WishlistSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category_name="Vegetables")
        self.product = Product.objects.create(product_name='Test Product', description='Test Description',
                                              price=10.0, category=category)
        self.wish_item = Wishlist.objects.create(user=self.user, product=self.product)

    def test_wish_serializer(self):
        serializer = WishlistSerializer(instance=self.wish_item)
        expected_data = {
            'id': self.wish_item.id,
            'user': self.user.id,
            'quantity': self.wish_item.quantity,
            'product': self.product.id,
        }
        self.assertEqual(serializer.data, expected_data)
