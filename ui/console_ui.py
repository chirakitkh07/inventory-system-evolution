# ui/console_ui.py — Console UI layer (all I/O lives here)
from __future__ import annotations

from services.inventory_service import InventoryService
from exporters.csv_report_exporter import CsvReportExporter


class ConsoleUI:
    """
    All user interaction (input/print) is confined to this layer.
    Business logic is delegated to InventoryService via Dependency Injection.
    """

    def __init__(self, service: InventoryService, exporter: CsvReportExporter) -> None:
        self._service = service
        self._exporter = exporter

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Main loop."""
        print("\n🏭  Inventory Management System v2.0")
        while True:
            self._menu()
            choice = input("Choice: ").strip()
            if choice == "1":
                self._add_product()
            elif choice == "2":
                self._view_all()
            elif choice == "3":
                self._search()
            elif choice == "4":
                self._update()
            elif choice == "5":
                self._delete()
            elif choice == "6":
                self._total_value()
            elif choice == "7":
                self._low_stock_report()
            elif choice == "8":
                self._export_csv()
            elif choice == "0":
                print("Goodbye. 👋")
                break
            else:
                print("⚠  Invalid choice. Try again.")

    # ------------------------------------------------------------------
    # Menu display
    # ------------------------------------------------------------------

    def _menu(self) -> None:
        print("\n" + "=" * 40)
        print("  INVENTORY SYSTEM — Main Menu")
        print("=" * 40)
        print("  1. Add product")
        print("  2. View all products")
        print("  3. Search product")
        print("  4. Update product")
        print("  5. Delete product")
        print("  6. Total inventory value")
        print("  7. Low-stock alerts")
        print("  8. Export CSV report")
        print("  0. Exit")
        print("=" * 40)

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def _add_product(self) -> None:
        print("\n--- Add Product ---")
        name = input("  Name: ").strip()
        try:
            qty = int(input("  Quantity: "))
            price = float(input("  Price: "))
        except ValueError:
            print("❌  Invalid number. Cancelled.")
            return
        category = input("  Category: ").strip()
        barcode = input("  Barcode (leave blank to skip): ").strip()
        reorder_raw = input("  Reorder point (0 = no alert): ").strip()
        try:
            reorder_point = int(reorder_raw) if reorder_raw else 0
        except ValueError:
            reorder_point = 0

        try:
            product = self._service.add_product(name, qty, price, category, barcode, reorder_point)
            print(f"✅  Added: [{product.id}] {product.name}")
        except ValueError as err:
            print(f"❌  {err}")

    def _view_all(self) -> None:
        products = self._service.get_all_products()
        if not products:
            print("\n⚠  No products in inventory.")
            return
        print(f"\n{'ID':>4}  {'Name':<25} {'Qty':>6} {'Price':>8}  {'Category':<15}  {'Barcode':<14}  Alert")
        print("-" * 85)
        for p in products:
            alert = "🔴 LOW" if p.qty <= p.reorder_point / 2 and p.is_low_stock else ("🟡 WARN" if p.is_low_stock else "")
            print(f"{p.id:>4}  {p.name:<25} {p.qty:>6} {p.price:>8.2f}  {p.category:<15}  {p.barcode:<14}  {alert}")

    def _search(self) -> None:
        print("\n--- Search ---")
        term = input("  Search by name or barcode: ").strip()
        if not term:
            return

        # Try barcode first (exact match), then name (partial)
        by_barcode = self._service.search_by_barcode(term)
        if by_barcode:
            results = [by_barcode]
        else:
            results = self._service.search_by_name(term)

        if not results:
            print("  Not found.")
            return
        for p in results:
            print(f"  [{p.id}] {p.name} | Qty:{p.qty} | Price:{p.price:.2f} | Cat:{p.category} | Barcode:{p.barcode}")

    def _update(self) -> None:
        print("\n--- Update Product ---")
        try:
            product_id = int(input("  Enter product ID: "))
        except ValueError:
            print("❌  Invalid ID.")
            return

        product = self._service.get_product(product_id)
        if not product:
            print("  Not found.")
            return

        print(f"  Updating: [{product.id}] {product.name} (leave blank to keep current value)")
        new_name = input(f"  Name [{product.name}]: ").strip() or None
        qty_raw = input(f"  Qty [{product.qty}]: ").strip()
        price_raw = input(f"  Price [{product.price}]: ").strip()
        new_barcode = input(f"  Barcode [{product.barcode}]: ").strip() or None
        reorder_raw = input(f"  Reorder point [{product.reorder_point}]: ").strip()

        kwargs: dict = {}
        if new_name:
            kwargs["name"] = new_name
        if qty_raw:
            try:
                kwargs["qty"] = int(qty_raw)
            except ValueError:
                print("❌  Invalid quantity — skipped.")
        if price_raw:
            try:
                kwargs["price"] = float(price_raw)
            except ValueError:
                print("❌  Invalid price — skipped.")
        if new_barcode:
            kwargs["barcode"] = new_barcode
        if reorder_raw:
            try:
                kwargs["reorder_point"] = int(reorder_raw)
            except ValueError:
                print("❌  Invalid reorder point — skipped.")

        try:
            updated = self._service.update_product(product_id, **kwargs)
            print(f"✅  Updated: [{updated.id}] {updated.name}")
        except ValueError as err:
            print(f"❌  {err}")

    def _delete(self) -> None:
        print("\n--- Delete Product ---")
        try:
            product_id = int(input("  Enter product ID to delete: "))
        except ValueError:
            print("❌  Invalid ID.")
            return
        confirm = input(f"  Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("  Cancelled.")
            return
        try:
            self._service.delete_product(product_id)
            print("✅  Deleted.")
        except ValueError as err:
            print(f"❌  {err}")

    def _total_value(self) -> None:
        total = self._service.calculate_total_value()
        print(f"\n💰  Total inventory value: {total:,.2f}")

    def _low_stock_report(self) -> None:
        alerts = self._service.get_low_stock_alerts()
        if not alerts:
            print("\n✅  All products are sufficiently stocked.")
            return
        print(f"\n⚠  LOW STOCK ALERTS ({len(alerts)} item(s)):")
        print("-" * 60)
        for p in alerts:
            level = "🔴" if p.qty <= p.reorder_point / 2 else "🟡"
            print(f"  {level} [{p.id}] {p.name} — Qty: {p.qty} (reorder at: {p.reorder_point})")

    def _export_csv(self) -> None:
        print("\n--- Export CSV ---")
        mode = input("  Export (1) low-stock only or (2) all products? [1/2]: ").strip()
        filepath = input("  Output filename [report.csv]: ").strip() or "report.csv"
        products = self._service.get_all_products()
        try:
            if mode == "2":
                self._exporter.export_all(products, filepath)
                print(f"✅  All products exported to {filepath}")
            else:
                low_stock = self._service.get_low_stock_alerts()
                self._exporter.export_low_stock(low_stock, filepath)
                print(f"✅  Low-stock report exported to {filepath} ({len(low_stock)} item(s))")
        except OSError as err:
            print(f"❌  Export failed: {err}")
