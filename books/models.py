from django.db import models
class Genre(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    # def __str__(self):
    #     return self.name

class Books(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    title = models.CharField(max_length=64)
    id_author = models.ForeignKey(to='Autors', on_delete=models.CASCADE, null=True, blank=True, default=None)
    text = models.TextField(null=False)
    year_publish = models.IntegerField(null=True, default=None)
    id_publishing_house = models.ForeignKey(to='Publishing_house', on_delete=models.CASCADE, null=True, blank=True, default=None)
    id_genre = models.ForeignKey(to='Genre', on_delete=models.CASCADE, null=True, blank=True, default=None)
    intro_images = models.CharField(max_length=256)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    count = models.IntegerField(null=False, default=0)
    count_page = models.IntegerField(null=False, default=0)
    view = models.IntegerField(null=False, default=0)
    like = models.IntegerField(null=False, default=0)
    disslike = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.title

class Autors(models.Model):
    id = models.AutoField(unique = True, primary_key = True)
    first_name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    middle_name = models.CharField(max_length = 64)
    date_of_birthd = models.DateField(null = True, default = None)
    date_of_death = models.DateField(null = True, default = None)
    country = models.CharField(max_length = 64, null = True, default = None)



class Publishing_house(models.Model):
    id = models.AutoField(unique = True, primary_key = True)
    title = models.CharField(max_length=64)
    address = models.CharField(max_length=64, null = True, default = None)
    
    # def __str__(self):
    #     return self.title
        
# Create your models here.
