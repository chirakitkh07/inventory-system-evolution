# exporters/csv_report_exporter.py — CR-02: CSV export (CsvReportExporter class)
from __future__ import annotations

import csv
from typing import List

from models.product import Product


class CsvReportExporter:
    """
    Responsible for exporting inventory data to CSV files.
    CR-02 requirement: low-stock report exportable and openable in Excel.
    """

    _HEADERS = ["ID", "Name", "Quantity", "Price", "Category", "Barcode", "Reorder Point", "Total Value", "Status"]

    def _product_to_row(self, product: Product) -> list:
        if product.is_low_stock:
            status = "LOW STOCK" if product.qty <= product.reorder_point / 2 else "WARNING"
        else:
            status = "OK"
        return [
            product.id,
            product.name,
            product.qty,
            f"{product.price:.2f}",
            product.category,
            product.barcode,
            product.reorder_point,
            f"{product.total_value:.2f}",
            status,
        ]

    def export_low_stock(self, products: List[Product], filepath: str) -> None:
        """Export only low-stock products to a CSV file."""
        low_stock = [p for p in products if p.is_low_stock]
        self._write_csv(low_stock, filepath)

    def export_all(self, products: List[Product], filepath: str) -> None:
        """Export all products to a CSV file."""
        self._write_csv(products, filepath)

    def _write_csv(self, products: List[Product], filepath: str) -> None:
        """Write products to CSV with UTF-8-BOM encoding for Excel compatibility."""
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(self._HEADERS)
            for product in products:
                writer.writerow(self._product_to_row(product))
