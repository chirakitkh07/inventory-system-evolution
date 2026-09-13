# tests/test_inventory_service.py — Unit tests for InventoryService (with mock repo)

import pytest
from unittest.mock import MagicMock, call

from models.product import Product
from services.inventory_service import InventoryService


# ---------------------------------------------------------------------------
# Fixtures: mock repository so service tests have no file I/O
# ---------------------------------------------------------------------------

def _make_product(pid=1, name="Widget", qty=10, price=5.00, cat="Parts",
                  barcode="", reorder_point=0):
    return Product(id=pid, name=name, qty=qty, price=price,
                   category=cat, barcode=barcode, reorder_point=reorder_point)


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return InventoryService(repo=mock_repo)


# ---------------------------------------------------------------------------
# Tests: read operations
# ---------------------------------------------------------------------------

class TestGetAll:
    def test_delegates_to_repo(self, service, mock_repo):
        mock_repo.find_all.return_value = [_make_product()]
        result = service.get_all_products()
        mock_repo.find_all.assert_called_once()
        assert len(result) == 1

    def test_empty_repo(self, service, mock_repo):
        mock_repo.find_all.return_value = []
        assert service.get_all_products() == []


class TestSearchByName:
    def test_partial_match(self, service, mock_repo):
        mock_repo.find_all.return_value = [
            _make_product(1, "Widget Pro"), _make_product(2, "Gadget")
        ]
        results = service.search_by_name("widget")
        assert len(results) == 1
        assert results[0].name == "Widget Pro"

    def test_case_insensitive(self, service, mock_repo):
        mock_repo.find_all.return_value = [_make_product(1, "Widget")]
        assert len(service.search_by_name("WIDGET")) == 1

    def test_no_match(self, service, mock_repo):
        mock_repo.find_all.return_value = [_make_product(1, "Widget")]
        assert service.search_by_name("xyz") == []


# ---------------------------------------------------------------------------
# Tests: CR-01 — Barcode search
# ---------------------------------------------------------------------------

class TestSearchByBarcode:
    def test_finds_product(self, service, mock_repo):
        mock_repo.find_by_barcode.return_value = _make_product(barcode="BC001")
        result = service.search_by_barcode("BC001")
        assert result is not None
        assert result.barcode == "BC001"

    def test_returns_none_when_not_found(self, service, mock_repo):
        mock_repo.find_by_barcode.return_value = None
        assert service.search_by_barcode("MISSING") is None


# ---------------------------------------------------------------------------
# Tests: add_product validation
# ---------------------------------------------------------------------------

class TestAddProduct:
    def test_add_valid(self, service, mock_repo):
        mock_repo.add.return_value = _make_product()
        result = service.add_product("Widget", 10, 5.00, "Parts")
        mock_repo.add.assert_called_once()
        assert result.name == "Widget"

    def test_add_with_barcode_and_reorder(self, service, mock_repo):
        mock_repo.add.return_value = _make_product(barcode="BC001", reorder_point=5)
        result = service.add_product("Widget", 10, 5.00, "Parts", "BC001", 5)
        assert result.barcode == "BC001"
        assert result.reorder_point == 5

    def test_empty_name_raises(self, service, mock_repo):
        with pytest.raises(ValueError, match="name cannot be empty"):
            service.add_product("", 10, 5.00, "Parts")

    def test_negative_qty_raises(self, service, mock_repo):
        with pytest.raises(ValueError, match="Quantity"):
            service.add_product("Widget", -1, 5.00, "Parts")

    def test_negative_price_raises(self, service, mock_repo):
        with pytest.raises(ValueError, match="Price"):
            service.add_product("Widget", 10, -1.00, "Parts")


# ---------------------------------------------------------------------------
# Tests: update_product
# ---------------------------------------------------------------------------

class TestUpdateProduct:
    def test_update_name(self, service, mock_repo):
        p = _make_product()
        mock_repo.find_by_id.return_value = p
        service.update_product(1, name="Super Widget")
        assert p.name == "Super Widget"
        mock_repo.update.assert_called_once_with(p)

    def test_update_not_found_raises(self, service, mock_repo):
        mock_repo.find_by_id.return_value = None
        with pytest.raises(ValueError):
            service.update_product(999, name="Ghost")


# ---------------------------------------------------------------------------
# Tests: delete_product
# ---------------------------------------------------------------------------

class TestDeleteProduct:
    def test_delete_calls_repo(self, service, mock_repo):
        service.delete_product(1)
        mock_repo.delete.assert_called_once_with(1)


# ---------------------------------------------------------------------------
# Tests: calculate_total_value
# ---------------------------------------------------------------------------

class TestTotalValue:
    def test_sum_of_all(self, service, mock_repo):
        mock_repo.find_all.return_value = [
            _make_product(qty=4, price=25.00),   # 100
            _make_product(qty=2, price=50.00),   # 100
        ]
        assert service.calculate_total_value() == 200.00

    def test_empty_inventory(self, service, mock_repo):
        mock_repo.find_all.return_value = []
        assert service.calculate_total_value() == 0.00


# ---------------------------------------------------------------------------
# Tests: CR-01 — get_low_stock_alerts (Reorder Point)
# ---------------------------------------------------------------------------

class TestLowStockAlerts:
    def test_returns_only_low_stock(self, service, mock_repo):
        mock_repo.find_all.return_value = [
            _make_product(1, qty=2, reorder_point=5),   # low
            _make_product(2, qty=10, reorder_point=5),  # ok
            _make_product(3, qty=5, reorder_point=5),   # exactly at point = low
        ]
        alerts = service.get_low_stock_alerts()
        assert len(alerts) == 2
        assert all(a.qty <= a.reorder_point for a in alerts)

    def test_no_alerts_when_all_stocked(self, service, mock_repo):
        mock_repo.find_all.return_value = [
            _make_product(qty=10, reorder_point=5),
        ]
        assert service.get_low_stock_alerts() == []

    def test_no_alerts_when_reorder_is_zero(self, service, mock_repo):
        mock_repo.find_all.return_value = [
            _make_product(qty=0, reorder_point=0),
        ]
        assert service.get_low_stock_alerts() == []
