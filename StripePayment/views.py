import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Item

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

    def get(self, request, pk: int):
        item_details = Item.objects.get(pk=pk)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # 'description': item_details.description,
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item_details.price,
                        'product_data': {
                            'name': item_details.name,
                        },
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                "product_id": item_details.id
            },
            mode='payment',
            success_url="http://127.0.0.1:8000/succes",
            cancel_url="http://127.0.0.1:8000/cancel",
        )

        return JsonResponse({
            'id': checkout_session.id
        })
