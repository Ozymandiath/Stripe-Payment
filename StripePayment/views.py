import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from stripe.error import InvalidRequestError

from .models import Item, Order, Discount, Tax

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
            coupons = Discount.objects.all()
            try:
                for coupon in coupons:
                    stripe.Coupon.delete(coupon.name_id)
            except InvalidRequestError:
                pass

            availability_promo = False
            for order in list_order:
                if order.taxs:
                    tax_id = stripe.TaxRate.create(display_name=order.taxs.name,
                                                   inclusive=order.taxs.inclusive,
                                                   percentage=order.taxs.percent)
                    Tax.objects.filter(id=order.taxs.id).update(name_id=tax_id["id"])
                if order.promo:
                    id_coupon = stripe.Coupon.create(percent_off=order.promo.percent,
                                                     duration="once",
                                                     currency=order.promo.currency)
                    Discount.objects.filter(id=order.promo.id).update(name_id=id_coupon["id"])
                    stripe.PromotionCode.create(coupon=id_coupon, code=order.promo.name, )
                    availability_promo = True

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': item_i.currency,
                            'unit_amount': item_i.price * 100,
                            'product_data': {
                                'name': item_i.name,
                            },
                        },
                        'quantity': 1,
                        'tax_rates': [order.taxs.name_id] if order.taxs else [],
                    } for order in list_order.prefetch_related("item").all() for item_i in order.item.all()],
                mode='payment',
                allow_promotion_codes=availability_promo,
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

    def delete(self, request, pk: int, pk1: int):
        order = Order.objects.prefetch_related("item").get(pk=pk)
        # c = list(order)
        item_remove = order.item.get(pk=pk1)
        order.item.remove(item_remove.id)
        order.save()
        # item.delete()
        return HttpResponse(200)
