from django.shortcuts import render
from django.views import View

# Create your views here.


class BlogView(View):

    def get(self, request):
        return render(request, 'blog/blog.html')


class BlogSingleView(View):

    def get(self, request):
        return render(request, 'blog/blog-single.html')