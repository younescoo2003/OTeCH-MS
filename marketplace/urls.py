from django.urls import path
from .views import MarketplaceHomeView, AddToCartView, CartView

app_name = 'marketplace'

urlpatterns = [
    path('', MarketplaceHomeView.as_view(), name='home'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),
]
