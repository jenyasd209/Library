from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from myAdmin.models import Readers


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', widget=forms.TextInput)
    last_name = forms.CharField(label='Last name', widget=forms.TextInput)
    patronymic = forms.CharField(label='Patronimic', widget=forms.TextInput)
    email = forms.CharField(label='Email', widget=forms.TextInput)
    adress = forms.CharField(label='Address', widget=forms.TextInput)
    telephone = forms.CharField(label='Telephone', widget=forms.TextInput)

    class Meta:
        model = Readers
        fields = ('first_name', 'last_name', 'patronymic', 'login', 'password', 'email', 'adress', 'telephone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Readers
        fields = ('first_name', 'last_name', 'patronymic', 'login', 'password', 'email', 'adress', 'telephone','is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'patronymic', 'login', 'password', 'email', 'adress', 'telephone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'adress', 'telephone',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'email', 'adress', 'telephone',)}
        ),
    )
    search_fields = ('login',)
    ordering = ('login',)
    filter_horizontal = ()
admin.site.register(Readers, UserAdmin)
admin.site.unregister(Group)