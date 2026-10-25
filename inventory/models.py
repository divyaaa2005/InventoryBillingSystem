
from django.db import models, transaction
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bill(models.Model):
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def calculate_total(self):
        total = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("price") * F("quantity"),
                    output_field=DecimalField(
                        max_digits=12, decimal_places=2
                    ),
                )
            )
        )["total"]

        self.total_amount = total or 0
        self.save(update_fields=["total_amount"])

    def __str__(self):
        return f"Bill #{self.pk} - {self.customer_name}"


class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        with transaction.atomic():
            old_item = None

            if self.pk:
                old_item = (
                    BillItem.objects.select_for_update()
                    .filter(pk=self.pk)
                    .first()
                )

            if self.quantity <= 0:
                raise ValidationError(
                    "Item quantity must be greater than zero."
                )

            # Lock the affected product records in a stable order.
            product_ids = {self.product_id}
            if old_item:
                product_ids.add(old_item.product_id)

            products = {
                product.pk: product
                for product in Product.objects.select_for_update()
                .filter(pk__in=product_ids)
                .order_by("pk")
            }

            new_product = products.get(self.product_id)
            if new_product is None:
                raise ValidationError("Selected product does not exist.")

            if old_item is None:
                # New bill item: deduct its quantity from stock.
                updated = Product.objects.filter(
                    pk=self.product_id,
                    quantity__gte=self.quantity,
                ).update(quantity=F("quantity") - self.quantity)

                if not updated:
                    raise ValidationError("Insufficient product stock.")

            elif old_item.product_id == self.product_id:
                # Existing item: adjust stock by the quantity difference.
                difference = self.quantity - old_item.quantity

                if difference > 0:
                    updated = Product.objects.filter(
                        pk=self.product_id,
                        quantity__gte=difference,
                    ).update(quantity=F("quantity") - difference)

                    if not updated:
                        raise ValidationError("Insufficient product stock.")

                elif difference < 0:
                    Product.objects.filter(
                        pk=self.product_id
                    ).update(quantity=F("quantity") - difference)

            else:
                # Product changed: restore old stock and deduct new stock.
                Product.objects.filter(
                    pk=old_item.product_id
                ).update(
                    quantity=F("quantity") + old_item.quantity
                )

                updated = Product.objects.filter(
                    pk=self.product_id,
                    quantity__gte=self.quantity,
                ).update(quantity=F("quantity") - self.quantity)

                if not updated:
                    raise ValidationError("Insufficient product stock.")

            # Keep the price charged on this bill item.
            if old_item is None:
                self.price = new_product.price

            super().save(*args, **kwargs)
            self.bill.calculate_total()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            item = (
                BillItem.objects.select_for_update()
                .get(pk=self.pk)
            )

            Product.objects.filter(
                pk=item.product_id
            ).update(
                quantity=F("quantity") + item.quantity
            )

            bill = item.bill
            result = super().delete(*args, **kwargs)
            bill.calculate_total()

            return result

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
