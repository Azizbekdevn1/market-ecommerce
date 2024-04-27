from django.urls import reverse_lazy

from apps.forms import OrderAcceptedModelForm
from apps.models import Order, Region, District
from apps.mixins import NotLoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView, UpdateView


class NewOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.NEW)
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context



class ReadyOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.READY_TO_DELIVERY)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class DeliveringOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERING)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class WaitingOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.WAITING)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class ArchivedOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.ARCHIVE)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class BrokenOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.BROKEN)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class DeliveredOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class CancelledOrderListView(ListView):
    queryset = Order.objects.filter(status=Order.Status.CANCELLED)
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


# class HoldOrderListView(ListView):
#     queryset = Order.objects.filter(status=Order.Status.HOLD)
#     paginate_by = 10
#     template_name = 'apps/operators/hold.html'
#     context_object_name = 'hold'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context['regions'] = Region.objects.all()
#         context['districts'] = District.objects.all()
#         return context


class AllOrderListView(ListView):
    queryset = Order.objects.all()
    paginate_by = 10
    template_name = 'apps/operators/operators.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class OrderAcceptedView(UpdateView):
    model = Order
    form_class = OrderAcceptedModelForm
    template_name = 'apps/operators/operators.html'
    success_url = reverse_lazy('new')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class ConditionUpdateView(UpdateView):
    model = Order
    form_class = OrderAcceptedModelForm
    template_name = 'apps/operators/operators.html'
    success_url = reverse_lazy('ready')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context
