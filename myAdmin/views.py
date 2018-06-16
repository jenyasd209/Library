from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, HttpResponse, redirect
from myAdmin.forms import UsersAuth
from django.contrib.auth import authenticate, login, logout
from books.models import Autors, Books, Publishing_house, Genre
from myUser.models import Booking, Forms
from myAdmin.models import Readers
from datetime import timedelta, datetime
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
import json

def booking(request):
    genres = Genre.objects.all()
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    bookings = Booking.objects.all()
    pag = Paginator(bookings, 15)
    try:
        bookings_on_page = pag.page(page_num)
    except InvalidPage:
        bookings_on_page = pag.page(1)
    return render(request, 'myAdmin/booking.html', locals())

def subBooking(request, id_booking):
    genres = Genre.objects.all()
    booking = Booking.objects.get(id = id_booking)
    forms = Forms.objects.all()
    newForm = Forms()

    now = datetime.now()
    after_30_days = now + timedelta(days=30)
    
    newForm.id_reader = booking.id_reader
    newForm.id_book = booking.id_book
    newForm.date_of_issue = now
    newForm.return_to = after_30_days
    newForm.save()
    booking.delete()
    return redirect("/admins/booking/")

def returnBook(request, id_form):
    genres = Genre.objects.all()
    form = Forms.objects.get(id = id_form)
    book = Books.objects.get(id = form.id_book_id)
    book.count = book.count + 1
    book.save()

    now = datetime.now()
    form.return_date = now
    form.save()
    
    return redirect("/admins/booking/")

def auth(request):
    genres = Genre.objects.all()
    if request.user.is_authenticated:
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
    else:
        form = UsersAuth(request.POST)
    return render(request, 'myAdmin/login.html', locals())


def index(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated or not request.user.is_staff:
        # return redirect('/admins/auth/')
        return redirect('/user/auth/')
    else:
        books = Books.objects.all().order_by("-date_add")
        user = request.user
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(books, 15)
        try:
            books_on_page = pag.page(page_num)
        except InvalidPage:
            books_on_page = pag.page(1)
        return render(request, 'myAdmin/cabinet.html', locals())


def exit(request):
    logout(request)
    return redirect('/')


def addBook(request):
    genres = Genre.objects.all()
    publishing_houses = Publishing_house.objects.all()
    authors = Autors.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        id_author = request.POST.get('id_author')
        text = request.POST.get('text')
        count = request.POST.get('count')
        count_page = request.POST.get('count_page')
        year_publish = request.POST.get('year_publish')
        publishing_house = request.POST.get('publishing_house')
        genre = request.POST.get('genre')
        intro_images = ''
        view = 0
        like = 0
        disslike = 0
        print("do")
        if request.FILES:
            if request.FILES.get('intro_file'):
                url = 'static/image/' + request.FILES.get('intro_file').name
                handle_uploaded_file(request.FILES.get('intro_file'), url)
                intro_images = '/' + url

        newBook = Books()
        newBook.title = title
        newBook.id_author = Autors.objects.get(id = id_author)
        newBook.text = text
        newBook.count = count
        newBook.count_page = count_page
        newBook.year_publish = year_publish
        newBook.id_publishing_house = Publishing_house.objects.get(id = publishing_house)
        newBook.id_genre = Genre.objects.get(id = genre)
        newBook.intro_images = intro_images
        newBook.like = like
        newBook.disslike = disslike
        newBook.view = view
        newBook.save()
        return redirect("/admins/")

    return render(request, 'myAdmin/bookadd.html', locals())


def editBook(request, id_book):
    book = Books.objects.get(id = id_book)
    genres = Genre.objects.all()
    publishing_houses = Publishing_house.objects.all()
    authors = Autors.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        id_author = request.POST.get('id_author')
        text = request.POST.get('text')
        count = request.POST.get('count')
        count_page = request.POST.get('count_page')
        year_publish = request.POST.get('year_publish')
        publishing_house = request.POST.get('publishing_house')
        id_genre = request.POST.get('id_genre')


        book.title = title
        book.id_author = Autors.objects.get(id=id_author)
        book.text = text
        book.count = count
        book.count_page = count_page
        book.year_publish = year_publish
        book.id_publishing_house = Publishing_house.objects.get(id=publishing_house)
        book.save()
        return redirect("/admins/")
    return render(request, 'myAdmin/edit.html', locals())

def deleteBook(request, id_book):
    genres = Genre.objects.all()
    book = Books.objects.get(id = id_book)
    book.delete()
    return redirect("/admins/")

def deleteBooking(request):
    # orig_date = datetime.datetime(x,y,z)
    # orig_date = str(orig_date)
    # d = datetime.datetime.strptime(orig_date, '%Y-%m-%d %H:%M:%S')
    # d = d.strftime('%m/%d/%y')
    genres = Genre.objects.all()

    now = datetime.now()
    # before_2_days = now - timedelta(days=2)
    # before_2_days = str(before_2_days)
    now = str(now)
    n = datetime.strptime(now, '%Y-%m-%d %H:%M:%S.%f')
    n = n.strftime('%Y-%m-%d %H:%M:%S.%f')
    with connection.cursor() as cursor:
        cursor.callproc('PR_DELETE_BOOKING', [n])
    booking = Booking.objects.all()
    # booking.
    # return row
    # book.delete()
    return redirect("/admins/booking/")

def handle_uploaded_file(f, url):
    genres = Genre.objects.all()
    with open(url, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def on_hands(request):
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return redirect('/user/auth/')
    else:
        forms = Forms.objects.all()
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(forms, 15)
        try:
            forms_on_page = pag.page(page_num)
        except InvalidPage:
            forms_on_page = pag.page(1)
        return render(request, 'myAdmin/on_hands.html', locals())

def search_book(request):
    book_name = request.GET['search_book']
    try:
        books_on_page = Books.objects.filter(title = book_name)
    except ObjectDoesNotExist:
        return render(request, 'myAdmin/unsearch.html', locals())
    return render(request, 'myAdmin/cabinet.html', locals())
    
def search_booking(request):
    try:
        booking_name = request.GET['search_booking']
    # if hands_name is not None:
        try:
            book = Books.objects.get(title = booking_name)
        except ObjectDoesNotExist:
            return render(request, 'myAdmin/unsearch.html', locals())
        bookings_on_page = Booking.objects.filter(id_book = book.id)
    except InvalidPage:
        bookings_on_page = Booking.objects.all()
        bookings_on_page = pag.page(1)
        return render(request, 'myAdmin/booking.html', locals())

def search_hand(request):
    hands_name = request.GET['search_hands']
    try:
    # if hands_name is not None:
        try:
            book = Books.objects.get(title = hands_name)
        except ObjectDoesNotExist:
            return render(request, 'myAdmin/unsearch.html', locals())
        forms_on_page = Forms.objects.filter(id_book = book.id)
        return render(request, 'myAdmin/on_hands.html', locals())
    except KeyError:
        forms_on_page = Forms.objects.all()
        forms_on_page = pag.page(1)
        return render(request, 'myAdmin/on_hands.html', locals())

# class PatientListView(CompanyProtectionMixin, ListView):
#     model = Patient
#     paginate_by = 12
#     template_name = 'patient/patient_list.html'
#     context_object_name = 'patients'
 
#     def get_queryset(self):
#         result = super(PatientListView, self).get_queryset()
 
#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(firstname__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(lastname__icontains=q) for q in query_list))  |
#                 reduce(operator.and_,
#                        (Q(midle_name__icontains=q) for q in query_list))
#             )
#         return result