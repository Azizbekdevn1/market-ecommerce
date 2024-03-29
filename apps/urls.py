from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.urls import path
from .tasks import add_data
from apps.tasks import task_one
from apps.views import ProductListView, ProductDetailView, RegisterFormView, CustomLoginView, ProfileView, \
    CustomUserLogoutView, OrderView, OrderedTemplateView, ProfileSettingsView, ChangePasswordView, WishlistView, \
    WishlistsView, WishlistRemoveView, MarketView
from root import settings
from django.urls import path


def djagshjhags(request):
    add_data()
    return JsonResponse({})


urlpatterns = [
                  path('', ProductListView.as_view(), name='product-list'),
                  path('data/', djagshjhags),
                  path('product/<str:slug>/', ProductDetailView.as_view(), name='product-detail'),
                  path('register/', RegisterFormView.as_view(), name='register'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('profile/', ProfileView.as_view(), name='profile'),
                  path('settings/', ProfileSettingsView.as_view(), name='settings'),
                  path('logout/', CustomUserLogoutView.as_view(), name='logout'),
                  path('order/', OrderView.as_view(), name='order'),
                  path('ordered/<int:pk>/', OrderedTemplateView.as_view(), name='ordered'),
                  path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
                  path('wishlist/add/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
                  path('wishlist/', WishlistsView.as_view(), name='wishlist_list'),
                  path('wishlist/delete/<int:product_id>', WishlistRemoveView.as_view(), name='wishlist_delete'),
                  path('market/', MarketView.as_view(), name='market')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
