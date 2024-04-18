from audioop import reverse
from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, PositiveIntegerField, FloatField, ForeignKey, ImageField, \
    TextField, JSONField, Model, CASCADE, TextChoices, BooleanField, DateTimeField, SlugField, SET_NULL
from django.utils.timezone import now
from django_resized import ResizedImageField
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify


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

    def __str__(self):
        return f'{self.id} - {self.type}'

    @property
    def count_wishlist(self):
        return self.wishlists.count()

    @property
    def is_operator(self):
        return self.type == self.Type.OPERATOR


class Category(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)
    image = ResizedImageField(size=[168, 168], upload_to='category/images', null=True, blank=True,
                              default='users/images/default.png')

    class Meta:
        verbose_name = 'Categoriya'
        verbose_name_plural = 'Categoriyalar'

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


class ProductImage(Model):
    image = ResizedImageField(upload_to='product/images', size=[1098, 717], null=True, blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

    def __repr__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Maxsulot rasmi'
        verbose_name_plural = 'Maxsulot rasmlari'


class Product(BaseModel):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)
    quantity = PositiveIntegerField(default=0)
    price = FloatField(default=200)
    spec = JSONField(null=True, blank=True)
    discount = FloatField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, 'categories')
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural = 'Maxsulotlar'

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)

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
    class Status(TextChoices):
        NEW = 'yangi', 'Yangi'
        DELIVERED = 'yetkazildi', 'Yetkazildi'
        ARCHIVE = 'arxivlandi', 'Arxivlandi'
        DELIVERING = 'yetkazilmoqda', 'Yetkazilmoqda'
        BROKEN = 'nosoz_mahsulot', 'Nosoz_maxsulot'
        RETURNED = 'qaytib_keldi', 'Qaytib_keldi'
        CANCELLED = 'bekor_qilindi', 'Bekor_qilibdi'
        WAITING = 'keyin_oladi', 'Keyin_oladi'
        READY_TO_DELIVERY = 'dastavkaga_tayyor', 'Dastavkaga_tayyor'

    status = CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    name = CharField(max_length=20)
    phone_number = CharField(max_length=20)
    count = PositiveIntegerField(default=1)
    product = ForeignKey('apps.Product', CASCADE, to_field='slug')
    currier = ForeignKey('apps.User', SET_NULL, limit_choices_to={'type': User.Type.CURRIER}, null=True, blank=True)

    @property
    def total(self):
        return self.count * self.product.percent_product


class Region(Model):
    name = CharField(max_length=30)


class District(Model):
    name = CharField(max_length=30)
    region = ForeignKey('apps.Region', CASCADE)


class WishList(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', CASCADE)
    added_at = DateTimeField(auto_now_add=True)


class Stream(Model):
    name = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE, related_name='streams')
    product = ForeignKey('apps.Product', CASCADE)


    class Meta:
        verbose_name = "Oqim"
        verbose_name_plural = "Oqimlar ro'yhati"
