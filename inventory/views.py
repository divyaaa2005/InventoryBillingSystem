
from django.shortcuts import render
from .models import Product, Bill


def dashboard(request):
    products = Product.objects.all()
    bills = Bill.objects.order_by("-created_at")[:5]

    total_products = products.count()
    total_stock = sum(product.quantity for product in products)

    context = {
        "products": products,
        "bills": bills,
        "total_products": total_products,
        "total_stock": total_stock,
        "total_bills": Bill.objects.count(),
    }

    return render(request, "inventory/dashboard.html", context)


def product_list(request):
    products = Product.objects.all().order_by("name")
    return render(
        request,
        "inventory/product_list.html",
        {"products": products},
    )


def bill_list(request):
    bills = Bill.objects.prefetch_related("items__product").order_by(
        "-created_at"
    )
    return render(
        request,
        "inventory/bill_list.html",
        {"bills": bills},
    )
