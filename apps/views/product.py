from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Count, Sum
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from apps.forms import OrderModelForm, StreamModelForm
from apps.models import Product, Order, WishList, Category, Stream, SiteSetting


class ProductListView(ListView):
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/product/product_grid.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['delivery_price'] = SiteSetting.objects.first()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        search = self.request.GET.get('search')
        queryset = super().get_queryset()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product_details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            stream = get_object_or_404(Stream.objects.all(), pk=pk)
            stream.view += 1
            stream.save()
            return stream.product

        product = get_object_or_404(Product.objects.all(), slug=slug)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        context['delivery_price'] = SiteSetting.objects.first()
        return context


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product/product_details.html'

    def form_valid(self, form):
        order = form.save(False)
        order.user = self.request.user
        order.save()
        return redirect(reverse('ordered', kwargs={'pk': order.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product_detail', kwargs={'slug': self.request.POST.get('product')}))


class OrderedTemplateView(DetailView):
    template_name = 'apps/product/ordered.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery_price'] = SiteSetting.objects.first().delivery_price
        return context


class WishlistView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        wishlist, created = WishList.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            wishlist.delete()
        return redirect('/')


class WishlistsView(LoginRequiredMixin, ListView):
    template_name = 'apps/product/wishlist.html'
    model = WishList
    context_object_name = 'wishlists'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class WishlistRemoveView(View):
    def get(self, request, product_id):
        WishList.objects.filter(product_id=product_id, user_id=self.request.user.id).delete()
        return redirect(reverse('wishlist_list'))


class MarketView(LoginRequiredMixin, ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'apps/product/market.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()


class StreamListView(LoginRequiredMixin, FormView):
    template_name = 'apps/product/oqim.html'
    form_class = StreamModelForm

    def form_valid(self, form):
        stream = form.save(commit=False)
        stream.user = self.request.user
        stream.save()
        return redirect('stream')


class StatisticView(LoginRequiredMixin, ListView):
    queryset = Stream.objects.annotate(
        new=Count('orders', filter=Q(orders__status=Order.Status.NEW)),
        delivered=Count('orders', filter=Q(orders__status=Order.Status.DELIVERED)),
        archive=Count('orders', filter=Q(orders__status=Order.Status.ARCHIVE)),
        delivering=Count('orders', filter=Q(orders__status=Order.Status.DELIVERING)),
        cancelled=Count('orders', filter=Q(orders__status=Order.Status.CANCELLED)),
        waiting=Count('orders', filter=Q(orders__status=Order.Status.WAITING)),
        ready_to_delivery=Count('orders', filter=Q(orders__status=Order.Status.READY_TO_DELIVERY)),
    ).select_related('product')
    template_name = 'apps/product/statistic.html'
    context_object_name = "streams_statistic"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        qs = self.get_queryset()
        context.update(**qs.aggregate(
            visit_count=Sum('view'),
            new_count=Sum('new'),
            delivered_count=Sum('delivered'),
            archive_count=Sum('archive'),
            delivering_count=Sum('delivering'),
            cancelled_count=Sum('cancelled'),
            waiting_count=Sum('waiting'),
            ready_to_delivery_count=Sum('ready_to_delivery'),
        ))
        return context


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/product/orders_list.html'
    context_object_name = "orders"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class QueriesListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all().select_related('product', 'operator')
    template_name = 'apps/product/queries.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class CompetitionView(ListView):
    template_name = 'aoo'
