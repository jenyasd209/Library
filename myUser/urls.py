from django.urls import path
from myUser import views

urlpatterns = [
    path('', views.returned),
    path('auth/', views.auth),
    path('reg/', views.reg),
    path('exit/', views.exit),
    path('reserv/', views.reserv),
    # path('return/', views.returned),
    path('on_hands/', views.on_hands),
    path('books/<int:id_book>', views.addBooking),
    # path('test/', views.test),
    # path('add/', views.addPost),
    # path('edit/<int:id_post>/', views.editPost),
    # path('delete/<int:id_post>/', views.)
]