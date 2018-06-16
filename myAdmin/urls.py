from django.urls import path
from myAdmin import views

urlpatterns = [
    path('', views.index),
    path('auth/', views.auth),
    path('exit/', views.exit),
    path('booking/', views.booking),
    path('booking/<int:id_booking>/', views.subBooking),
    path('on_hands/', views.on_hands),
    path('on_hands/<int:id_form>/', views.returnBook),
    path('add/', views.addBook),
    path('delete/', views.deleteBooking),
    path('edit/<int:id_book>/', views.editBook),
    path('delete/<int:id_book>/', views.deleteBook),    
    path('book_search/', views.search_book),
    path('booking/booking_search/', views.search_booking),
    path('on_hands/on_hands_search/', views.search_hand)
]
