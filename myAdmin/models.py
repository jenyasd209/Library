from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class ReadersManager(BaseUserManager):
    def create_user(self, first_name, last_name, patronymic, login, password, email, adress, telephone,):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not login:
            raise ValueError('Users must have a login')
        if not adress:
            raise ValueError('Users must have an address')
        if not password:
            raise ValueError('Users must have a password')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not first_name:
            raise ValueError('Users must have a first name')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            patronymic = patronymic,
            login = login,
            email=self.normalize_email(email),
            adress = adress,
            telephone = telephone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, patronymic, login, password, email, adress, telephone):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            patronymic = patronymic,
            login = login,
            password = password,
            email=self.normalize_email(email),
            adress = adress,
            telephone = telephone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Readers(AbstractBaseUser):
    # id = models.AutoField(unique = True, primary_key = True)
    first_name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    patronymic = models.CharField(max_length = 64)
    login = models.CharField(max_length = 64, unique = True)
    password = models.CharField(max_length = 128)
    email = models.CharField(max_length = 64, null = True)
    adress = models.CharField(max_length = 64)
    telephone = models.CharField(max_length = 64)
    date_of_reg = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ReadersManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'patronymic', 'email', 'adress', 'telephone',]

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

