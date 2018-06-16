from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from books.models import Autors, Books, Genre, Publishing_house
from myUser.models import Booking
from myAdmin.models import Readers
from datetime import timedelta, datetime

def genre(request, id_cat):
    # genres = Genre.objects.all()
    # genre = Genre.objects.get(id = id_cat)
    return render(request, 'books/books.html', locals())

def search_books(request):
    book_name = request.GET['search_books']
    try:
        books_on_page = Books.objects.filter(title = book_name)
    except ObjectDoesNotExist:
        return render(request, 'myAdmin/unsearch.html', locals())
    return render(request, 'books/books.html', locals())

def genre(request, id_genre):
    genres = Genre.objects.all()
    books = Books.objects.all().filter(id_genre_id=id_genre).order_by("-date_add")
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    pag = Paginator(books, 9)
    try:
        books_on_page = pag.page(page_num)
    except InvalidPage:
        books_on_page = pag.page(1)
    return render(request, 'books/genre.html', locals())

def book(request, id_book):
    book = Books.objects.get(id = id_book)
    genres = Genre.objects.all()
    # author = Autors.objects.get(id = book.id_author)
    return render(request, 'books/book.html', locals())

def addBooking(request, id_book):
    readers = Readers.objects.get(id = request.user.id)
    book = Books.objects.get(id = id_book)
    print(book.count)
    book.count = book.count - 1
    book.save()
    # book.count -= 1
    booking = Booking.objects.all()
    print("sdgsf")
    newBooking = Booking()
    now = datetime.now()
    after_2_days = now + timedelta(days=2)
    
    newBooking.id_reader = readers
    newBooking.id_book = book
    print("sdgsf")
    newBooking.date_booking = now
    newBooking.reserved_until = after_2_days
    newBooking.save()
    return redirect("/books/")

    return render(request, 'books/books.html', locals())

def all_books(request):
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    books = Books.objects.all()
    pag = Paginator(books, 9)
    try:
        books_on_page = pag.page(page_num)
    except InvalidPage:
        books_on_page = pag.page(1)
    genres = Genre.objects.all()
    return render(request, 'books/books.html', locals())

# Create your views here.
