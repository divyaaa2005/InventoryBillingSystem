
from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Product, Bill, BillItem


class InventoryBillingTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Notebook",
            price=Decimal("50.00"),
            quantity=10,
            category="Stationery",
        )

        self.bill = Bill.objects.create(
            customer_name="Test Customer"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Notebook")
        self.assertEqual(self.product.quantity, 10)

    def test_bill_item_deducts_stock_and_calculates_total(self):
        item = BillItem.objects.create(
            bill=self.bill,
            product=self.product,
            quantity=2,
            price=self.product.price,
        )

        self.product.refresh_from_db()
        self.bill.refresh_from_db()

        self.assertEqual(self.product.quantity, 8)
        self.assertEqual(item.subtotal, Decimal("100.00"))
        self.assertEqual(self.bill.total_amount, Decimal("100.00"))

    def test_insufficient_stock_is_rejected(self):
        with self.assertRaises(ValidationError):
            BillItem.objects.create(
                bill=self.bill,
                product=self.product,
                quantity=11,
                price=self.product.price,
            )

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)

    def test_deleting_bill_item_restores_stock(self):
        item = BillItem.objects.create(
            bill=self.bill,
            product=self.product,
            quantity=3,
            price=self.product.price,
        )

        item.delete()
        self.product.refresh_from_db()
        self.bill.refresh_from_db()

        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.bill.total_amount, Decimal("0"))
