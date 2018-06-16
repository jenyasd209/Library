from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, HttpResponse, redirect
from myAdmin.forms import UsersAuth
from django.contrib.auth import authenticate, login, logout
from books.models import Autors, Books, Publishing_house, Genre
from myUser.models import Booking, Forms
from myAdmin.models import Readers
import json

def reg(request):
    genres = Genre.objects.all()
    # publishing_houses = Publishing_house.objects.all()
    # authors = Autors.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        patronymic = request.POST.get('patronymic')
        login = request.POST.get('login')
        password = request.POST.get('password')
        email = request.POST.get('e-mail')
        address = request.POST.get('address')
        telephone = request.POST.get('telephone')

        newUser = Readers()

        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.patronymic = patronymic
        newUser.login = login
        newUser.set_password(password)
        newUser.email = email
        newUser.address = address
        newUser.telephone = telephone

        newUser.save()

    return render(request, 'myUser/reg.html', locals())


def auth(request):
    genres = Genre.objects.all()
    if request.user.is_authenticated:
        return redirect('/user/')
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admins/')
    if request.method == "POST":
        form = UsersAuth(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            myuser = authenticate(username=username, password=password)
            if myuser is not None:
                login(request, myuser)
                return redirect('/admins/')
                if request.user.is_staff:
                    return redirect('/admins/')
    else:
        form = UsersAuth(request.POST)
    return render(request, 'myUser/login.html', locals())


def index(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return redirect('/user/auth/')
    else:
        books = Books.objects.all().order_by("-date_add")
        user = request.user
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(books, 15, orphans=2)
        try:
            books_on_page = pag.page(page_num)
        except InvalidPage:
            books_on_page = pag.page(1)
        return render(request, 'myUser/cab.html', locals())


def exit(request):
    logout(request)
    return redirect('/')

def reserv(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return redirect('/user/auth/')
    else:
        readers = Readers.objects.get(id = request.user.id)
        bookings = Booking.objects.all().filter(id_reader_id = request.user.id)
        user = request.user
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(bookings, 15)
        try:
            bookings_on_page = pag.page(page_num)
        except InvalidPage:
            bookings_on_page = pag.page(1)
        return render(request, 'myUser/reserv.html', locals())

def returned(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return redirect('/user/auth/')
    else:
        forms = Forms.objects.filter(return_date__isnull = False, id_reader_id = request.user.id)
        user = request.user
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(forms, 15)
        try:
            forms_on_page = pag.page(page_num)
        except InvalidPage:
            forms_on_page = pag.page(1)
        return render(request, 'myUser/return.html', locals())

def on_hands(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return redirect('/user/auth/')
    else:
        forms = Forms.objects.all().filter(id_reader_id = request.user.id)
        user = request.user
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(forms, 15)
        try:
            forms_on_page = pag.page(page_num)
        except InvalidPage:
            forms_on_page = pag.page(1)
        return render(request, 'myUser/on_hands.html', locals())

def addBooking(request, id_book):
    genres = Genre.objects.all()
    booking = Booking.objects.all()
    book = Books.objects.get(id = id_book)
    print(book.count)
    book.count = book.count - 1
    book.save()
    print("sdgsf")
    newBooking = Booking()
    now = datetime.now()
    after_2_days = now + timedelta(days=2)
    
    newBooking.id_reader = request.user.id
    newBooking.id_book = id_book
    print("sdgsf")
    newBooking.date_booking = now
    newBooking.reserved_until = after_2_days
    newBooking.save()
    return redirect("/books/book.id")

    return render(request, 'books/books.html', locals())
