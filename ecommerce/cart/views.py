from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from store.models import Product

from .cart import Cart


def cart_summary(request):
    return render(request, "cart/cart-summary.html")


def cart_add(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        product = get_object_or_404(Product, id=product_id)
        cart.add(
            product=product,
            product_qty=product_quantity,
        )
        return JsonResponse({"qty": len(cart)})


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product_id=product_id)
        return JsonResponse(
            {
                "qty": len(cart),
                "cart_total": cart.get_total(),
            }
        )


def cart_update(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        cart.update(
            product_id=product_id,
            product_qty=product_quantity,
        )

        return JsonResponse(
            {
                "qty": len(cart),
                "cart_total": cart.get_total(),
            }
        )
