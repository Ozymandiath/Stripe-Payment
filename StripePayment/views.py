import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemView(View):
    template_name = "StripePayment/items.html"

    def get(self, request, pk: int):
        try:
            item_details = Item.objects.get(pk=pk)

            return render(request, self.template_name, {"item": item_details, "secret_key": settings.STRIPE_PUBLIC_KEY})

        except ObjectDoesNotExist:
            return render(request, self.template_name, {"error": True}, status=404)


class BuyItemIDView(View):

    def get(self, request, pk: int = None):
        if not pk:
            list_order = Order.objects.all()
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'rub',
                            'unit_amount': order.item.price * 100,
                            'product_data': {
                                'name': order.item.name,
                            },
                        },
                        'quantity': 1,
                    } for order in list_order],
                mode='payment',
                success_url="http://127.0.0.1:8000/succes",
                cancel_url="http://127.0.0.1:8000/cancel",
            )
        else:
            item_details = Item.objects.get(pk=pk)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'rub',
                            'unit_amount': item_details.price * 100,
                            'product_data': {
                                'name': item_details.name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url="http://127.0.0.1:8000/succes",
                cancel_url="http://127.0.0.1:8000/cancel",
            )

        return JsonResponse({
            'id': checkout_session.id
        })


class OrderView(View):
    template_name = "StripePayment/order.html"

    def get(self, request):
        list_order = Order.objects.all()
        return render(request, self.template_name, {"orders": list_order, "secret_key": settings.STRIPE_PUBLIC_KEY})


class DeleteItemView(View):

    def delete(self, request, pk: int):
        order = Order.objects.filter(pk=pk)
        order.delete()
        return HttpResponse(200)
