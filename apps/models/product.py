from datetime import timedelta
from django.db.models import CharField, PositiveIntegerField, FloatField, ForeignKey, TextField, JSONField, Model, \
    CASCADE, TextChoices, DateTimeField, SlugField, SET_NULL, IntegerField
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField
from apps.models.user import User
from django_ckeditor_5.fields import CKEditor5Field


class BaseModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(default=timezone.now)

    def created_at_product(self):
        return self.created_at.strftime("%d.%m.%Y")

    class Meta:
        abstract = True


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
        while Category.objects.filter(slug=unique_slug).exists():
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
    slug = SlugField(max_length=255, unique=True, editable=False)
    quantity = PositiveIntegerField(default=0)
    price = IntegerField(default=200)
    spec = JSONField(null=True, blank=True)
    discount = IntegerField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, 'categories')
    description = CKEditor5Field(blank=True, null=True)

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
        if not self.slug:
            self.slug = self._get_unique_slug()
        return super().save(force_insert, force_update, using, update_fields)

    @property
    def percent_product(self):
        return int(self.price * (1 - self.discount / 100))

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


class Order(BaseModel):
    class Status(TextChoices):
        NEW = 'yangi', 'Yangi'
        DELIVERED = 'yetkazildi', 'Yetkazildi'
        ARCHIVE = 'arxivlandi', 'Arxivlandi'
        DELIVERING = 'yetkazilmoqda', 'Yetkazilmoqda'
        BROKEN = 'nosoz_mahsulot', 'Nosoz maxsulot'
        RETURNED = 'qaytib_keldi', 'Qaytib keldi'
        CANCELLED = 'bekor_qilindi', 'Bekor qilindi'
        WAITING = 'keyin_oladi', 'Keyin oladi'
        READY_TO_DELIVERY = 'dastavkaga_tayyor', 'Dastavkaga tayyor'
        HOLD = 'hold', 'Hold'

    status = CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    name = CharField(max_length=20)
    phone_number = CharField(max_length=20)
    count = PositiveIntegerField(default=1)
    product = ForeignKey('apps.Product', CASCADE, to_field='slug')
    currier = ForeignKey('apps.User', SET_NULL, limit_choices_to={'type': User.Type.CURRIER}, null=True, blank=True)
    comment = CharField(max_length=255, blank=True, null=True)
    region = ForeignKey('apps.Region', CASCADE, verbose_name='Viloyat', blank=True, null=True)
    stream = ForeignKey('apps.Stream', SET_NULL, blank=True, null=True, related_name="orders")
    district = ForeignKey('apps.District', CASCADE, verbose_name='Tuman', blank=True, null=True)
    street = CharField(max_length=25, verbose_name="Ko'cha", blank=True, null=True)
    operator = ForeignKey('apps.User', CASCADE, 'operator', blank=True, null=True, verbose_name='Operator')
    user = ForeignKey('apps.User', CASCADE, 'user', blank=True, null=True, verbose_name='Foydalanuvchi')

    @property
    def total(self):
        return self.count * self.product.percent_product

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Zakaz'
        verbose_name_plural = 'Zakazlar'


class Region(Model):
    name = CharField(max_length=30)

    class Meta:
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyatlar'


class District(Model):
    name = CharField(max_length=30)
    region = ForeignKey('apps.Region', CASCADE)

    class Meta:
        verbose_name = 'Tuman'
        verbose_name_plural = 'Tumanlar'


class WishList(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', CASCADE)
    added_at = DateTimeField(auto_now_add=True)


class SiteSetting(Model):
    delivery_price = IntegerField('Yetkazib berish narxi')

    class Meta:
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Yetkazib berish narhi"


class Stream(Model):
    name = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE, related_name='streams')
    product = ForeignKey('apps.Product', CASCADE)
    view = IntegerField(default=0)

    class Meta:
        ordering = ['-id']
        verbose_name = "Oqim"
        verbose_name_plural = "Oqimlar ro'yhati"

    def __str__(self):
        return f'{self.product.name} --> {self.user}'
