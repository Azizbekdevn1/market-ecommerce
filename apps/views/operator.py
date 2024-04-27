from apps.models import Order
from apps.mixins import NotLoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView


class BaseOperatorListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.NEW)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'


class OrderREADYTODELIVERYListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'


class OrderARCHIVEListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'


class OrderDELIVEREDListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'


class OrderBROKENListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'




