from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path

from apps.views import ProductListView, ProductDetailView, RegisterFormView, CustomLoginView, ProfileView, \
    CustomUserLogoutView, OrderView, OrderedTemplateView, ProfileSettingsView, ChangePasswordView, WishlistView, \
    WishlistsView, WishlistRemoveView, MarketView, StreamListView, StatisticView, \
    NewOrderListView, ReadyOrderListView, DeliveringOrderListView, WaitingOrderListView, ArchivedOrderListView, \
    BrokenOrderListView, \
    DeliveredOrderListView, CancelledOrderListView, AllOrderListView, OrdersListView, HoldOrderListView, \
    NewOrderCreateView, ConditionUpdateView,QueriesListView

from root import settings
from .tasks import add_data

# def djagshjhags(request):
#     add_data()
#     return JsonResponse({})


urlpatterns = ([
                   path('', ProductListView.as_view(), name='product_list'),
                   path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
                   path('stream/<int:pk>/', ProductDetailView.as_view(), name='stream_detail'),
                   path('order/', OrderView.as_view(), name='order'),
                   path('ordered/<int:pk>/', OrderedTemplateView.as_view(), name='ordered'),
                   path('wishlist/add/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
                   path('wishlist/', WishlistsView.as_view(), name='wishlist_list'),
                   path('wishlist/delete/<int:product_id>', WishlistRemoveView.as_view(), name='wishlist_delete'),
                   path('market/', MarketView.as_view(), name='market'),
                   path('stream/', StreamListView.as_view(), name='stream'),
                   path('statistics/', StatisticView.as_view(), name='statistic'),
                   path('orders/', OrdersListView.as_view(), name='orders_list'),
                   path('queries/', QueriesListView.as_view(), name='queries_list'),

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
    path('operator/new/', NewOrderListView.as_view(), name='new'),
    path('operator/ready/', ReadyOrderListView.as_view(), name='ready'),
    path('operator/delivering/', DeliveringOrderListView.as_view(), name='delivering'),
    path('operator/waiting/', WaitingOrderListView.as_view(), name='waiting'),
    path('operator/archived/', ArchivedOrderListView.as_view(), name='archived'),
    path('operator/broken/', BrokenOrderListView.as_view(), name='broken'),
    path('operator/delivered/', DeliveredOrderListView.as_view(), name='delivered'),
    path('operator/cancelled/', CancelledOrderListView.as_view(), name='cancelled'),
    path('operator/all/', AllOrderListView.as_view(), name='all'),
    path('operator/hold/', HoldOrderListView.as_view(), name='hold'),
    path('operator/create_order/', NewOrderCreateView.as_view(), name='order_create'),
    path('operator/condition/<int:pk>/', ConditionUpdateView.as_view(), name='condition_update'),

]
