from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView, UpdateView
from apps.models import Product, User, Order, WishList, Category
from .forms import UserRegistrationForm, OrderModelForm
from django.core.mail import send_mail

from .mixins import NotLoginRequiredMixin


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'


class RegisterFormView(FormView, NotLoginRequiredMixin):
    form_class = UserRegistrationForm
    template_name = 'apps/auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the form data
        form.save()

        # Send an email to the user
        user_email = form.cleaned_data['email']
        send_mail(
            'Assalomu Alaykum saytimizga xush kelibsiz ',
            'Tanlang va sotib oling ',
            'azizbekmurodov2003@gmail.com',  # Sender's email
            [user_email],  # Recipient's email
            fail_silently=False,
        )

        # Call the parent class's form_valid method
        return super().form_valid(form)


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/auth/login.html'
    authentication_form = AuthenticationForm
    next_page = 'product-list'


class ProfileView(ListView, NotLoginRequiredMixin):
    template_name = 'apps/users/profile.html'
    queryset = User.objects.all()


class CustomUserLogoutView(TemplateView):
    template_name = 'apps/auth/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product/product-details.html'

    def form_valid(self, form):
        order = form.save()
        return redirect(reverse('ordered', kwargs={'pk': order.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product-detail', kwargs={'pk': self.request.POST.get('product')}))


class OrderedTemplateView(DetailView):
    template_name = 'apps/product/ordered.html'
    model = Order
    context_object_name = 'order'


class ProfileSettingsView(UpdateView):
    template_name = 'apps/users/settings.html'
    model = User
    fields = ('phone', 'first_name', 'last_name', 'email', 'intro')
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'apps/users/settings.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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
