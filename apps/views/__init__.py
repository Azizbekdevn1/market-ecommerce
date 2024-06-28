from apps.views.product import (ProductListView, ProductDetailView, OrderView, OrderedTemplateView,
                                WishlistView, WishlistsView, WishlistRemoveView, MarketView, StreamListView,
                                StatisticView, OrdersListView,QueriesListView)

from apps.views.user import (RegisterFormView, CustomLoginView, ProfileView, CustomUserLogoutView, ProfileSettingsView,
                             ChangePasswordView)

from apps.views.operator import (NewOrderListView, ReadyOrderListView, DeliveringOrderListView, WaitingOrderListView,
                                 ArchivedOrderListView, BrokenOrderListView,
                                 DeliveredOrderListView, CancelledOrderListView, AllOrderListView, HoldOrderListView,
                                 NewOrderCreateView, ConditionUpdateView)
