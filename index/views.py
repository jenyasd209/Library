from django.shortcuts import render
from books.models import Genre, Books

def index(request):
    books = Books.objects.all()
    genres = Genre.objects.all()
    return render(request, 'index/index.html', locals())
def about(request):
    genres = Genre.objects.all()
    return render(request, 'index/about.html', locals())

# Create your views here.
