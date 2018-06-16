from django import forms
from books.models import Autors, Books, Publishing_house, Genre

class UsersAuth(forms.Form):
    login = forms.CharField(label="Login", max_length=64)
    password = forms.CharField(label="Password", max_length=64)

class BookForm(forms.Form):
    title = forms.CharField(label="Заголовок")
    id_author = forms.ModelChoiceField(queryset=Autors.objects.all(), label="Автор")
    text = forms.CharField(label="Описание", widget=forms.Textarea)
    count = forms.IntegerField(label="Количесвто в наличие")
    count_page = forms.IntegerField(label="Количество страниц")
    year_publish = forms.IntegerField(label="Год публикации")
    id_publishing_house = forms.ModelChoiceField(queryset=Publishing_house.objects.all(), label="Издательство")
    id_genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label="Жанр")
    intro_images = forms.FileField(label="Изображение")
# class PostForm(forms.Form):
#     title = forms.CharField(label="Заголовок")
#     text = forms.CharField(label="Текст статьи", widget=forms.Textarea)
#     id_category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
#     intro_images = forms.FileField(label="Главное изображение")
