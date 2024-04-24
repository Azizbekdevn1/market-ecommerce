from apps.models import Order
from apps.mixins import NotLoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView


class BaseOperatorListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.NEW)
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'

    # def get_queryset(self):
    #     return super().get_queryset().filter(status=Order.Status.NEW)
