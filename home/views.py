from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexShopView(View):

    def get(self, request):
        return render(request, 'home/index.html')


class ContactView(View):

    def get(self, request):
        return render(request, 'home/contact.html')


class AboutView(View):

    def get(self, request):
        return render(request, 'home/about.html')