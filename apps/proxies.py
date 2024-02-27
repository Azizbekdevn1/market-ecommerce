from apps.models import User


class AdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class CurrierProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Kuryer'
        verbose_name_plural = 'Kuryerlar'


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class OperatorProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Operator'
        verbose_name_plural = 'Operatorlar'


class ManageerProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Menejer'
        verbose_name_plural = 'Menejerlar'