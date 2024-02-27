from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.forms import ModelForm, ValidationError, CharField, PasswordInput, TextInput
from apps.models import User, Order
import re


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', required=True)
    password_confirm = CharField(label='Confirm Password', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = CharField(widget=TextInput)
    password = CharField(widget=PasswordInput)


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'phone_number', 'product','count')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'^\+998\(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            raise ValidationError("Invalid phone number format. Please use the format +998(__) ___-__ - __")
        return phone_number


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'intro')
