from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from apps.forms import OrderModelForm, StreamModelForm
from apps.models import Product, Order, WishList, Category, Stream


class ProductListView(ListView):
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/product/product_grid.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
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
    slug_url_kwarg = 'slug'


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product/product_details.html'

    def form_valid(self, form):
        order = form.save()
        return redirect(reverse('ordered', kwargs={'pk': order.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product-detail', kwargs={'slug': self.request.POST.get('product')}))


class OrderedTemplateView(DetailView):
    template_name = 'apps/product/ordered.html'
    model = Order
    context_object_name = 'order'


class OrdersListView(ListView):
    template_name = 'apps/product/operator.html'
    model = Order
    context_object_name = 'orders'


class WishlistView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        wishlist, created = WishList.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            wishlist.delete()
        return redirect('/')


class WishlistsView(ListView):
    template_name = 'apps/product/wishlist.html'
    model = WishList
    context_object_name = 'wishlists'


class WishlistRemoveView(View):

    def get(self, request, product_id):
        WishList.objects.filter(product_id=product_id, user_id=self.request.user.id).delete()
        return redirect(reverse('wishlist_list'))


class MarketView(ListView):
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['streams'] = Stream.objects.filter(user=self.request.user)
    #     return context

    def form_valid(self, form):
        stream = form.save(commit=False)
        stream.user = self.request.user
        stream.save()
        return redirect('stream')


class StreamDetailView(DetailView):
    model = Stream
    template_name = 'apps/product/product_details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        stream = get_object_or_404(Stream.objects.all(), pk=pk)
        return stream.product


class StatisticView(ListView):
    model = Stream
    template_name = 'apps/product/statistic.html'


class OperatorView(ListView):
    model = Order
    template_name = 'apps/product/operators.html'
    context_object_name = 'orders'
