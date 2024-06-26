from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.forms import ModelForm, ValidationError, CharField, PasswordInput, TextInput, ModelChoiceField
from apps.models import User, Order, Stream, Product, Region,District
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
    product = ModelChoiceField(queryset=Product.objects.all())
    stream = ModelChoiceField(queryset=Stream.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ('name', 'phone_number', 'product', 'count', 'stream')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'^\+998\(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            raise ValidationError("Invalid phone number format. Please use the format +998(__) ___-__ - __")
        return ''.join(re.findall('\d+', phone_number))


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'intro')


class StreamModelForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Stream
        fields = ('name', 'product')


class OrderAcceptedModelForm(ModelForm):
    region = ModelChoiceField(queryset=Region.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['region', 'status', 'comment', 'count']


class OrderCreateModelForm(ModelForm):
    region = ModelChoiceField(queryset=Region.objects.all())
    name = CharField(max_length=255, label="Ism familya")
    product=ModelChoiceField(queryset=Product.objects.all())
    district=ModelChoiceField(queryset=District.objects.all())

    class Meta:
        model = Order
        fields = ['name', 'region', 'district', 'count', 'phone_number', 'product']
