from django.urls import path
from books import views
# from myUser import views

urlpatterns = [
    path('', views.all_books),
    path('genre/<int:id_genre>/', views.genre),
    path('<int:id_book>', views.book),
    path('<int:id_book>/reserv', views.addBooking),
    path('books_search/', views.search_books),
]