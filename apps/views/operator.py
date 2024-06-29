from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView

from apps.forms import OrderAcceptedModelForm, OrderCreateModelForm
from apps.models import Order, Region, District, Product


class BaseOperatorListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class NewOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.NEW)
    template_name = 'apps/operators/new_order.html'


class ReadyOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.READY_TO_DELIVERY)
    template_name = 'apps/operators/ready_to_delivery.html'


class DeliveringOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERING)
    template_name = 'apps/operators/delivering.html'


class WaitingOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.WAITING)
    template_name = 'apps/operators/waiting.html'


class ArchivedOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.ARCHIVE)
    template_name = 'apps/operators/archived.html'


class BrokenOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.BROKEN)
    template_name = 'apps/operators/broken.html'


class DeliveredOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.DELIVERED)
    template_name = 'apps/operators/delivered.html'


class CancelledOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.CANCELLED)
    template_name = 'apps/operators/cancelled.html'


class HoldOrderListView(BaseOperatorListView):
    queryset = Order.objects.filter(status=Order.Status.HOLD)
    template_name = 'apps/operators/hold.html'


class AllOrderListView(BaseOperatorListView):
    queryset = Order.objects.all()
    template_name = 'apps/operators/all.html'


class NewOrderCreateView(CreateView, BaseOperatorListView):
    model = Order
    form_class = OrderCreateModelForm
    template_name = 'apps/operators/zakaz.html'
    success_url = reverse_lazy('new')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()
        return context

    def form_valid(self, form):
        order = form.save(False)
        order.user = self.request.user
        order.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DownloadView(View):

    def get(self, request):
        user = request.user
        return FileResponse(user.avatar.file, as_attachment=True)


class ConditionUpdateView(UpdateView):
    model = Order
    form_class = OrderAcceptedModelForm
    template_name = 'apps/operators/accepted_order.html'
    success_url = reverse_lazy('ready')
    context_object_name = 'order'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.operator = self.request.user
        obj.save()
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context
