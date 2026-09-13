# repositories/inventory_repository.py — JSON-backed Repository Pattern
from __future__ import annotations

import json
import os
from typing import List, Optional

from models.product import Product


class InventoryRepository:
    """
    Repository Pattern: abstracts all JSON persistence for Products.
    Business logic never touches files directly — it only calls this class.
    Dependency Injection: pass the filepath in __init__ to keep it testable.
    """

    def __init__(self, filepath: str = "inventory.json") -> None:
        self._filepath = filepath
        self._cache: Optional[List[Product]] = None

    # ------------------------------------------------------------------
    # Internal load / save (private)
    # ------------------------------------------------------------------

    def _load_from_file(self) -> List[Product]:
        """Read products from the JSON file. Returns empty list if missing."""
        if not os.path.exists(self._filepath):
            return []
        with open(self._filepath, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Product.from_dict(item) for item in raw]

    def _save_to_file(self, products: List[Product]) -> None:
        """Persist the product list to the JSON file."""
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in products], f, indent=2, ensure_ascii=False)

    def _get_cache(self) -> List[Product]:
        if self._cache is None:
            self._cache = self._load_from_file()
        return self._cache

    def _flush(self, products: List[Product]) -> None:
        self._cache = products
        self._save_to_file(products)

    def _next_id(self, products: List[Product]) -> int:
        return max((p.id for p in products), default=0) + 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def find_all(self) -> List[Product]:
        """Return all products."""
        return list(self._get_cache())

    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Return the product with the given ID, or None if not found."""
        for product in self._get_cache():
            if product.id == product_id:
                return product
        return None

    def find_by_barcode(self, barcode: str) -> Optional[Product]:
        """Return the product matching the barcode, or None."""
        for product in self._get_cache():
            if product.barcode == barcode:
                return product
        return None

    def add(self, product: Product) -> Product:
        """Persist a new product and return it with its assigned ID."""
        products = self._get_cache()
        product.id = self._next_id(products)
        products.append(product)
        self._flush(products)
        return product

    def update(self, updated: Product) -> None:
        """Replace the stored product with the updated version."""
        products = self._get_cache()
        for index, product in enumerate(products):
            if product.id == updated.id:
                products[index] = updated
                self._flush(products)
                return
        raise ValueError(f"Product with id={updated.id} not found.")

    def delete(self, product_id: int) -> None:
        """Remove the product with the given ID."""
        products = self._get_cache()
        original_length = len(products)
        products = [p for p in products if p.id != product_id]
        if len(products) == original_length:
            raise ValueError(f"Product with id={product_id} not found.")
        self._flush(products)
