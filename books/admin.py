from django.contrib import admin
from books.models import Books, Publishing_house, Autors, Genre

admin.site.register(Books)
admin.site.register(Publishing_house)
admin.site.register(Autors)
admin.site.register(Genre)
# Register your models here.
