from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, PositiveIntegerField, FloatField, ForeignKey, ImageField, \
    TextField, JSONField, Model, CASCADE, TextChoices, BooleanField, DateTimeField
from django.utils.timezone import now
from django_resized import ResizedImageField
from datetime import timedelta
from django.utils import timezone


class BaseModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(default=timezone.now)

    def created_at_product(self):
        return self.created_at.strftime("%d.%m.%Y")

    class Meta:
        abstract = True


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

    @property
    def count_wishlist(self):
        return self.wishlists.count()


# objects =CustomUserManager()


class Category(Model):
    name = CharField(max_length=255)
    image = ResizedImageField(size=[168, 168], upload_to='category/images', null=True, blank=True,
                              default='users/images/default.png')

    class Meta:
        verbose_name = 'Categoriya'
        verbose_name_plural = 'Categoriyalar'

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ResizedImageField(upload_to='product/images', size=[1098, 717], null=True,
                              blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

    def __repr__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Maxsulot rasmi'
        verbose_name_plural = 'Maxsulot rasmlari'


class Product(BaseModel):
    name = CharField(max_length=255)
    quantity = PositiveIntegerField(default=0)
    price = FloatField(default=200)
    spec = JSONField(null=True, blank=True)
    discount = FloatField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, 'categories')
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural = 'Maxsulotlar'

    @property
    def percent_product(self):
        return self.price * (1 - self.discount / 100)

    @property
    def image(self):
        return self.images.first()

    @property
    def in_stock(self):
        return self.quantity > 0

    @property
    def in_discount(self):
        return self.discount and self.discount > 0

    def __str__(self):
        return self.name

    def shipping_cost(self):
        return self.price * 0.03

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=7)


class Order(Model):
    name = CharField(max_length=20)
    phone_number = CharField(max_length=20)
    count = PositiveIntegerField(default=1)
    product = ForeignKey('apps.Product', CASCADE)

    @property
    def total(self):
        return self.count * self.product.percent_product


class WishList(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', CASCADE)
    added_at = DateTimeField(auto_now_add=True)
