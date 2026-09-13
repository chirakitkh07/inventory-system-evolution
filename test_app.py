# test_app.py — Baseline Regression Tests for app_v1.py
# Phase 1: Covers all existing behaviour BEFORE any refactoring.
# All tests must pass (green 100%) before any code changes begin.

import pytest
import app_v1


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset the global inventory list and counter before each test."""
    app_v1.x = []
    app_v1.n = 0
    yield
    app_v1.x = []
    app_v1.n = 0


# ---------------------------------------------------------------------------
# Helper: directly manipulate global state (bypassing input()) to test logic
# ---------------------------------------------------------------------------

def _add_item(name: str, qty: int, price: float, cat: str) -> dict:
    """Insert an item directly into the global inventory (no I/O)."""
    app_v1.n += 1
    item = {"id": app_v1.n, "name": name, "qty": qty, "price": price, "cat": cat}
    app_v1.x.append(item)
    return item


# ---------------------------------------------------------------------------
# Tests: global state management
# ---------------------------------------------------------------------------

class TestGlobalState:
    def test_inventory_starts_empty(self):
        assert app_v1.x == []

    def test_counter_starts_at_zero(self):
        assert app_v1.n == 0

    def test_adding_item_increments_counter(self):
        _add_item("Widget", 10, 5.00, "Parts")
        assert app_v1.n == 1

    def test_id_auto_increments(self):
        a = _add_item("Widget", 10, 5.00, "Parts")
        b = _add_item("Gadget", 5, 12.50, "Electronics")
        assert a["id"] == 1
        assert b["id"] == 2


# ---------------------------------------------------------------------------
# Tests: view() — display all inventory
# ---------------------------------------------------------------------------

class TestView:
    def test_view_empty_inventory(self, capsys):
        app_v1.view()
        captured = capsys.readouterr()
        assert "No items" in captured.out

    def test_view_shows_all_items(self, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        _add_item("Gadget", 3, 12.50, "Electronics")
        app_v1.view()
        captured = capsys.readouterr()
        assert "Widget" in captured.out
        assert "Gadget" in captured.out

    def test_view_shows_correct_fields(self, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        app_v1.view()
        captured = capsys.readouterr()
        assert "Widget" in captured.out
        assert "10" in captured.out
        assert "5.0" in captured.out
        assert "Parts" in captured.out


# ---------------------------------------------------------------------------
# Tests: srch() — search by name (via patched input)
# ---------------------------------------------------------------------------

class TestSearch:
    def test_search_finds_match(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "widget")
        app_v1.srch()
        captured = capsys.readouterr()
        assert "Widget" in captured.out

    def test_search_case_insensitive(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "WIDGET")
        app_v1.srch()
        captured = capsys.readouterr()
        assert "Widget" in captured.out

    def test_search_not_found(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "xyz")
        app_v1.srch()
        captured = capsys.readouterr()
        assert "Not found" in captured.out

    def test_search_partial_match(self, monkeypatch, capsys):
        _add_item("Widget Pro", 5, 20.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "widge")
        app_v1.srch()
        captured = capsys.readouterr()
        assert "Widget Pro" in captured.out


# ---------------------------------------------------------------------------
# Tests: upd() — update an existing item
# ---------------------------------------------------------------------------

class TestUpdate:
    def test_update_name(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        inputs = iter(["1", "SuperWidget", "", ""])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.upd()
        assert app_v1.x[0]["name"] == "SuperWidget"

    def test_update_quantity(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        inputs = iter(["1", "", "99", ""])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.upd()
        assert app_v1.x[0]["qty"] == 99

    def test_update_price(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        inputs = iter(["1", "", "", "7.77"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.upd()
        assert app_v1.x[0]["price"] == 7.77

    def test_update_blank_keeps_value(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        inputs = iter(["1", "", "", ""])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.upd()
        assert app_v1.x[0]["name"] == "Widget"
        assert app_v1.x[0]["qty"] == 10
        assert app_v1.x[0]["price"] == 5.00

    def test_update_not_found(self, monkeypatch, capsys):
        inputs = iter(["999"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.upd()
        captured = capsys.readouterr()
        assert "Not found" in captured.out


# ---------------------------------------------------------------------------
# Tests: dlt() — delete an item
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_item(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        app_v1.dlt()
        assert len(app_v1.x) == 0

    def test_delete_prints_deleted(self, monkeypatch, capsys):
        _add_item("Widget", 10, 5.00, "Parts")
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        app_v1.dlt()
        captured = capsys.readouterr()
        assert "Deleted" in captured.out

    def test_delete_not_found(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _="": "999")
        app_v1.dlt()
        captured = capsys.readouterr()
        assert "Not found" in captured.out

    def test_delete_correct_item_when_multiple(self, monkeypatch):
        _add_item("Widget", 10, 5.00, "Parts")
        _add_item("Gadget", 3, 12.50, "Electronics")
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        app_v1.dlt()
        assert len(app_v1.x) == 1
        assert app_v1.x[0]["name"] == "Gadget"


# ---------------------------------------------------------------------------
# Tests: tot() — total inventory value calculation
# ---------------------------------------------------------------------------

class TestTotalValue:
    def test_total_empty_inventory(self, capsys):
        app_v1.tot()
        captured = capsys.readouterr()
        assert "0.00" in captured.out

    def test_total_single_item(self, capsys):
        _add_item("Widget", 4, 25.00, "Parts")   # 4 * 25 = 100.00
        app_v1.tot()
        captured = capsys.readouterr()
        assert "100.00" in captured.out

    def test_total_multiple_items(self, capsys):
        _add_item("Widget", 4, 25.00, "Parts")   # 100.00
        _add_item("Gadget", 2, 50.00, "Electronics")  # 100.00
        app_v1.tot()
        captured = capsys.readouterr()
        assert "200.00" in captured.out

    def test_total_float_precision(self, capsys):
        _add_item("Item", 3, 1.10, "Misc")  # 3.30
        app_v1.tot()
        captured = capsys.readouterr()
        assert "3.30" in captured.out


# ---------------------------------------------------------------------------
# Tests: add() via patched input — integration path
# ---------------------------------------------------------------------------

class TestAdd:
    def test_add_via_input(self, monkeypatch, capsys):
        inputs = iter(["Widget", "10", "5.00", "Parts"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.add()
        assert len(app_v1.x) == 1
        assert app_v1.x[0]["name"] == "Widget"
        assert app_v1.x[0]["qty"] == 10
        assert app_v1.x[0]["price"] == 5.00
        assert app_v1.x[0]["cat"] == "Parts"

    def test_add_prints_confirmation(self, monkeypatch, capsys):
        inputs = iter(["Widget", "10", "5.00", "Parts"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        app_v1.add()
        captured = capsys.readouterr()
        assert "Added" in captured.out

    def test_add_multiple_items_unique_ids(self, monkeypatch):
        for name in ["A", "B", "C"]:
            inputs = iter([name, "1", "1.00", "X"])
            monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
            app_v1.add()
        ids = [i["id"] for i in app_v1.x]
        assert ids == [1, 2, 3]
