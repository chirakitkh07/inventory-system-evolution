# tests/test_product.py — Unit tests for Product model

import pytest
from models.product import Product


class TestProductCreation:
    def test_basic_creation(self):
        p = Product(id=1, name="Widget", qty=10, price=5.00, category="Parts")
        assert p.id == 1
        assert p.name == "Widget"
        assert p.qty == 10
        assert p.price == 5.00
        assert p.category == "Parts"

    def test_defaults(self):
        p = Product(id=1, name="Widget", qty=10, price=5.00, category="Parts")
        assert p.barcode == ""
        assert p.reorder_point == 0

    def test_with_barcode_and_reorder(self):
        p = Product(id=1, name="Widget", qty=10, price=5.00, category="Parts",
                    barcode="1234567890", reorder_point=5)
        assert p.barcode == "1234567890"
        assert p.reorder_point == 5


class TestProductFromDict:
    def test_from_dict_full(self):
        data = {"id": 1, "name": "Widget", "qty": 10, "price": 5.00,
                "category": "Parts", "barcode": "BC001", "reorder_point": 3}
        p = Product.from_dict(data)
        assert p.id == 1
        assert p.name == "Widget"
        assert p.barcode == "BC001"
        assert p.reorder_point == 3

    def test_from_dict_legacy_cat_key(self):
        """Supports old 'cat' key from app_v1.py data."""
        data = {"id": 1, "name": "Widget", "qty": 5, "price": 10.0, "cat": "OldCat"}
        p = Product.from_dict(data)
        assert p.category == "OldCat"

    def test_from_dict_missing_optional(self):
        data = {"id": 2, "name": "Gadget", "qty": 3, "price": 15.0, "category": "Elec"}
        p = Product.from_dict(data)
        assert p.barcode == ""
        assert p.reorder_point == 0

    def test_to_dict_round_trip(self):
        p = Product(id=1, name="Widget", qty=10, price=5.00, category="Parts",
                    barcode="BC001", reorder_point=5)
        d = p.to_dict()
        restored = Product.from_dict(d)
        assert restored.id == p.id
        assert restored.name == p.name
        assert restored.barcode == p.barcode
        assert restored.reorder_point == p.reorder_point


class TestProductProperties:
    def test_total_value(self):
        p = Product(id=1, name="Widget", qty=4, price=25.00, category="Parts")
        assert p.total_value == 100.00

    def test_total_value_zero_qty(self):
        p = Product(id=1, name="Widget", qty=0, price=25.00, category="Parts")
        assert p.total_value == 0.00

    def test_is_low_stock_true(self):
        p = Product(id=1, name="Widget", qty=3, price=5.00, category="Parts", reorder_point=5)
        assert p.is_low_stock is True

    def test_is_low_stock_false_above_reorder(self):
        p = Product(id=1, name="Widget", qty=10, price=5.00, category="Parts", reorder_point=5)
        assert p.is_low_stock is False

    def test_is_low_stock_false_when_reorder_zero(self):
        p = Product(id=1, name="Widget", qty=0, price=5.00, category="Parts", reorder_point=0)
        assert p.is_low_stock is False

    def test_is_low_stock_at_exact_reorder_point(self):
        p = Product(id=1, name="Widget", qty=5, price=5.00, category="Parts", reorder_point=5)
        assert p.is_low_stock is True
