from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return f"{self.product.product_name}_{self.value}%_{self.date_end}"

