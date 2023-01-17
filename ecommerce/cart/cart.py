from decimal import Decimal
from django.http import HttpRequest

from store.models import Product


class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        self.cart = self.session.setdefault("cart", {})

    def add(self, product: Product, product_qty: int):
        product_id = str(product.id)

        self.cart.setdefault(product_id, {"price": str(product.price)})
        self.cart[product_id]["qty"] = product_qty

        self.session.modified = True

    def delete(self, product_id: int):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product_id: int, product_qty: int):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_qty

        self.session.modified = True

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]

            yield item

    def get_total(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
