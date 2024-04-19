from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, TextField, TextChoices, BooleanField
from django_resized import ResizedImageField


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = "admin", "Admin"
        CURRIER = "currier", "Yetkazib beruvchi"
        USERS = "users", "Foydalanuvchi"
        OPERATOR = "operator", "Operator"
        MANAGER = "manager", "Menejer"

    type = CharField(max_length=20, choices=Type.choices, default=Type.USERS)
    phone_regex = RegexValidator(regex=r'^\d{12}$',
                                 message="Phone number must be entered in the format: '999999999'. Up to 15 digits allowed.")
    intro = TextField(max_length=1024, blank=True, null=True, default="Here is into from user")
    avatar = ResizedImageField(size=[168, 168], upload_to='users/images', null=True, blank=True,
                               default='users/images/default.png')
    banner = ResizedImageField(size=[1198, 124], upload_to='users/images', null=True, blank=True,
                               default='users/images/default.png')
    workout = CharField(max_length=50, blank=True, null=True, default="Here is")
    country = CharField(max_length=30, blank=True, null=True, default="Uzbekistan")
    is_verified = BooleanField(default=False)
    phone = CharField(max_length=25, unique=True, validators=[phone_regex], null=True)

    def __str__(self):
        return f'{self.id} - {self.type}'

    @property
    def count_wishlist(self):
        return self.wishlists.count()

    @property
    def is_operator(self):
        return self.type == self.Type.OPERATOR
