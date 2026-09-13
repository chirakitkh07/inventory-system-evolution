# tests/test_csv_report_exporter.py — Unit tests for CsvReportExporter (CR-02)

import csv
import pytest

from models.product import Product
from exporters.csv_report_exporter import CsvReportExporter


@pytest.fixture
def exporter():
    return CsvReportExporter()


def _make_product(pid=1, name="Widget", qty=10, price=5.00, cat="Parts",
                  barcode="BC001", reorder_point=0):
    return Product(id=pid, name=name, qty=qty, price=price,
                   category=cat, barcode=barcode, reorder_point=reorder_point)


class TestExportAll:
    def test_creates_file(self, exporter, tmp_path):
        filepath = str(tmp_path / "report.csv")
        exporter.export_all([_make_product()], filepath)
        assert (tmp_path / "report.csv").exists()

    def test_header_row(self, exporter, tmp_path):
        filepath = str(tmp_path / "report.csv")
        exporter.export_all([_make_product()], filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert "ID" in header
        assert "Name" in header
        assert "Barcode" in header
        assert "Reorder Point" in header

    def test_all_products_included(self, exporter, tmp_path):
        filepath = str(tmp_path / "report.csv")
        products = [_make_product(1, "Widget"), _make_product(2, "Gadget")]
        exporter.export_all(products, filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        # 1 header + 2 data rows
        assert len(rows) == 3

    def test_empty_inventory(self, exporter, tmp_path):
        filepath = str(tmp_path / "report.csv")
        exporter.export_all([], filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        assert len(rows) == 1  # only header


class TestExportLowStock:
    def test_only_low_stock_exported(self, exporter, tmp_path):
        filepath = str(tmp_path / "low_stock.csv")
        products = [
            _make_product(1, "Widget", qty=2, reorder_point=5),   # low
            _make_product(2, "Gadget", qty=10, reorder_point=5),  # ok
        ]
        exporter.export_low_stock(products, filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        assert len(rows) == 2  # header + 1 low stock item
        assert rows[1][1] == "Widget"

    def test_status_column_low_stock(self, exporter, tmp_path):
        filepath = str(tmp_path / "low_stock.csv")
        p = _make_product(qty=1, reorder_point=10)  # severely low
        exporter.export_low_stock([p], filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        status = rows[1][-1]
        assert "LOW" in status or "WARN" in status

    def test_utf8_bom_for_excel(self, exporter, tmp_path):
        """File should start with UTF-8 BOM \\xef\\xbb\\xbf for Excel."""
        filepath = str(tmp_path / "report.csv")
        exporter.export_all([_make_product()], filepath)
        with open(filepath, "rb") as f:
            bom = f.read(3)
        assert bom == b"\xef\xbb\xbf"
