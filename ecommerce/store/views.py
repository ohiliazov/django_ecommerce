from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def store(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, "store/store.html", context)


def list_category(request, category_slug: str):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    return render(
        request,
        "store/list-category.html",
        {"category": category, "products": products},
    )


def product_info(request, product_slug: str):
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}
    return render(request, "store/product-info.html", context)
