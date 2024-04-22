from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path

from apps.views import ProductListView, ProductDetailView, RegisterFormView, CustomLoginView, ProfileView, \
    CustomUserLogoutView, OrderView, OrderedTemplateView, ProfileSettingsView, ChangePasswordView, WishlistView, \
    WishlistsView, WishlistRemoveView, MarketView, StreamListView, StreamDetailView, StatisticView, \
    BaseOperatorListView, \
    OrdersListView
from root import settings
from .tasks import add_data

# def djagshjhags(request):
#     add_data()
#     return JsonResponse({})
#
#
# def trigger_error(request):
#     division_by_zero = 1 / 0


urlpatterns = ([
                   path('', ProductListView.as_view(), name='product-list'),
                   # path('data/', djagshjhags),
                   # path('sentry-debug/', trigger_error),
                   path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
                   path('order/', OrderView.as_view(), name='order'),
                   path('ordered/<int:pk>/', OrderedTemplateView.as_view(), name='ordered'),
                   path('wishlist/add/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
                   path('wishlist/', WishlistsView.as_view(), name='wishlist_list'),
                   path('wishlist/delete/<int:product_id>', WishlistRemoveView.as_view(), name='wishlist_delete'),
                   path('market/', MarketView.as_view(), name='market'),
                   path('stream/', StreamListView.as_view(), name='stream'),
                   path('stream/<int:pk>/', StreamDetailView.as_view(), name='stream_detail'),
                   path('statistics/', StatisticView.as_view(), name='statistic'),
               ]

               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
# auth site

urlpatterns += [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', ProfileSettingsView.as_view(), name='settings'),
    path('logout/', CustomUserLogoutView.as_view(), name='logout'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
]

# operator side
urlpatterns += [
    path('operator/new/', BaseOperatorListView.as_view(), name='orders_list'),

]
