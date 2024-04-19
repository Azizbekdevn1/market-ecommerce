from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, UpdateView
from apps.forms import UserRegistrationForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import User


class RegisterFormView(NotLoginRequiredMixin, FormView):
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


class CustomUserLogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
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
