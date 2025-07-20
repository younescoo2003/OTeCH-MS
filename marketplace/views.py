from django.views.generic import ListView, View, TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, CartItem

class MarketplaceHomeView(ListView):
    model = Product
    template_name = 'marketplace/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('marketplace:cart_view')


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CartItem.objects.filter(user=self.request.user)
        context['items'] = items
        context['total'] = sum(item.total_price() for item in items)
        return context
