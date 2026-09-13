# models/product.py — Product data model
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Product:
    """Represents a single inventory product (data model layer)."""

    id: int
    name: str
    qty: int
    price: float
    category: str
    barcode: str = ""
    reorder_point: int = 0

    # ------------------------------------------------------------------
    # Factory Method pattern: construct from raw dict (JSON persistence)
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> Product:
        """Create a Product instance from a plain dictionary."""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            qty=int(data["qty"]),
            price=float(data["price"]),
            category=str(data.get("category", data.get("cat", ""))),
            barcode=str(data.get("barcode", "")),
            reorder_point=int(data.get("reorder_point", 0)),
        )

    def to_dict(self) -> dict:
        """Serialise the Product to a plain dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "qty": self.qty,
            "price": self.price,
            "category": self.category,
            "barcode": self.barcode,
            "reorder_point": self.reorder_point,
        }

    @property
    def total_value(self) -> float:
        """Quantity × unit price."""
        return self.qty * self.price

    @property
    def is_low_stock(self) -> bool:
        """True when qty has fallen to or below the reorder point (and reorder_point > 0)."""
        return self.reorder_point > 0 and self.qty <= self.reorder_point
