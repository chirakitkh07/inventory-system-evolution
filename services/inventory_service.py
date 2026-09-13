# services/inventory_service.py — Business logic layer (Facade + DI pattern)
from __future__ import annotations

from typing import List, Optional

from models.product import Product
from repositories.inventory_repository import InventoryRepository


class InventoryService:
    """
    Business logic layer. Receives an InventoryRepository via Dependency Injection.
    No I/O here — pure logic only. This eliminates the global `x` from app_v1.py.
    """

    def __init__(self, repo: InventoryRepository) -> None:
        self._repo = repo

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_all_products(self) -> List[Product]:
        """Return all products in inventory."""
        return self._repo.find_all()

    def get_product(self, product_id: int) -> Optional[Product]:
        """Return a single product by ID, or None."""
        return self._repo.find_by_id(product_id)

    def search_by_name(self, name: str) -> List[Product]:
        """Case-insensitive partial-name search."""
        name_lower = name.lower()
        return [p for p in self._repo.find_all() if name_lower in p.name.lower()]

    def search_by_barcode(self, barcode: str) -> Optional[Product]:
        """Return product matching exact barcode, or None."""
        return self._repo.find_by_barcode(barcode)

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def add_product(
        self,
        name: str,
        qty: int,
        price: float,
        category: str,
        barcode: str = "",
        reorder_point: int = 0,
    ) -> Product:
        """Validate and persist a new product."""
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if qty < 0:
            raise ValueError("Quantity cannot be negative.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        product = Product(
            id=0,  # will be assigned by repository
            name=name.strip(),
            qty=qty,
            price=price,
            category=category.strip(),
            barcode=barcode.strip(),
            reorder_point=reorder_point,
        )
        return self._repo.add(product)

    def update_product(self, product_id: int, **kwargs) -> Product:
        """
        Partially update a product. Only fields present in kwargs are changed.
        Raises ValueError if product not found.
        """
        product = self._repo.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id={product_id} not found.")

        for field_name, value in kwargs.items():
            if hasattr(product, field_name) and value is not None:
                setattr(product, field_name, value)

        self._repo.update(product)
        return product

    def delete_product(self, product_id: int) -> None:
        """Delete a product by ID. Raises ValueError if not found."""
        self._repo.delete(product_id)

    # ------------------------------------------------------------------
    # Computed / aggregate operations
    # ------------------------------------------------------------------

    def calculate_total_value(self) -> float:
        """Sum of qty × price across all products."""
        return sum(p.total_value for p in self._repo.find_all())

    def get_low_stock_alerts(self) -> List[Product]:
        """Return products where qty <= reorder_point (and reorder_point > 0)."""
        return [p for p in self._repo.find_all() if p.is_low_stock]
