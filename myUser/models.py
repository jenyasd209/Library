from django.db import models
from datetime import timedelta, datetime
from books.models import Books
from myAdmin.models import Readers

class Booking(models.Model):
    now = datetime.now()
    after_2_days = now + timedelta(days=2)

    id = models.AutoField(unique=True, primary_key=True)
    id_reader = models.ForeignKey(to='myAdmin.Readers', on_delete=models.CASCADE, null=True, blank=True, default=None)
    id_book = models.ForeignKey(to='books.Books', on_delete=models.CASCADE, null=True, blank=True, default=None)
    date_booking = models.DateTimeField(auto_now_add=True)
    reserved_until = models.DateTimeField()

    # def __str__(self):
    #     return self.title

class Forms(models.Model):
    # now = datetime.now()
    # after_30_days = now + timedelta(days=30)

    id = models.AutoField(unique=True, primary_key=True)
    id_reader = models.ForeignKey(to='myAdmin.Readers', on_delete=models.CASCADE, null=True, blank=True, default=None)
    id_book = models.ForeignKey(to='books.Books', on_delete=models.CASCADE, null=True, blank=True, default=None)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    return_to = models.DateTimeField()

# class Reader(models.Model):
#     id = models.AutoField(unique = True, primary_key = True)
#     first_name = models.CharField(max_length = 64)
#     last_name = models.CharField(max_length = 64)
#     patronymic = models.CharField(max_length = 64)
#     login = models.CharField(max_length = 64, unique = True)
#     password = models.CharField(max_length = 128)
#     email = models.CharField(max_length = 64, null = True)
#     adress = models.CharField(max_length = 64)
#     telephone = models.CharField(max_length = 64)
#     date_of_reg = models.DateTimeField(auto_now_add=True, blank = True, null = True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

# Create your models here.
