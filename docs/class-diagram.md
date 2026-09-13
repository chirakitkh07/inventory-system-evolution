# To-Be Architecture — Class Diagram (Mermaid)
## Inventory Management System v2.0

```mermaid
classDiagram
    direction TB

    class Product {
        +int id
        +str name
        +int qty
        +float price
        +str category
        +str barcode
        +int reorder_point
        +to_dict() dict
        +from_dict(data: dict)$ Product
    }

    class InventoryRepository {
        -str _filepath
        -list~Product~ _cache
        +__init__(filepath: str)
        +load() list~Product~
        +save(products: list~Product~) None
        +find_all() list~Product~
        +find_by_id(id: int) Product
        +find_by_barcode(barcode: str) Product
        +add(product: Product) Product
        +update(product: Product) None
        +delete(id: int) None
    }

    class InventoryService {
        -InventoryRepository _repo
        +__init__(repo: InventoryRepository)
        +get_all_products() list~Product~
        +get_product(id: int) Product
        +search_by_name(name: str) list~Product~
        +search_by_barcode(barcode: str) Product
        +add_product(name, qty, price, category, barcode, reorder_point) Product
        +update_product(id, **kwargs) Product
        +delete_product(id: int) None
        +calculate_total_value() float
        +get_low_stock_alerts() list~Product~
    }

    class CsvReportExporter {
        +export_low_stock(products: list~Product~, filepath: str) None
        +export_all(products: list~Product~, filepath: str) None
    }

    class ConsoleUI {
        -InventoryService _service
        -CsvReportExporter _exporter
        +__init__(service: InventoryService, exporter: CsvReportExporter)
        +run() None
        -_menu() None
        -_add_product() None
        -_view_all() None
        -_search() None
        -_update() None
        -_delete() None
        -_total_value() None
        -_low_stock_report() None
        -_export_csv() None
    }

    InventoryService --> InventoryRepository : uses (DI)
    InventoryService --> Product : manages
    InventoryRepository --> Product : persists
    ConsoleUI --> InventoryService : uses (DI)
    ConsoleUI --> CsvReportExporter : uses (DI)
```

---

## Design Patterns Applied

| Pattern | Where Used | Reason |
|---------|-----------|--------|
| **Repository** | `InventoryRepository` | Decouples persistence (JSON) from business logic; swap to DB without changing service |
| **Dependency Injection** | `InventoryService.__init__(repo)` | Eliminates `global x`; makes unit-testing with mock repos trivial |
| **Factory Method** | `Product.from_dict()` | Centralises object construction from raw data |
| **Facade** | `InventoryService` | Single entry point for all business operations; hides repository complexity from UI |

---

## ISO 25010 Quality Evaluation

| Characteristic | v1 (Baseline) | v2 (Target) | Improvement |
|---------------|--------------|------------|-------------|
| **Maintainability** | ❌ Global state, no classes | ✅ Repository + DI | Major |
| **Testability** | ❌ `input()` in logic | ✅ Pure functions, DI | Major |
| **Reliability** | ❌ No error handling | ✅ Exception handling | Major |
| **Security** | ❌ Raw `input()` → crashes | ✅ Validated inputs | Moderate |
| **Portability** | ❌ In-memory only | ✅ JSON persistence | Moderate |
| **Functional Suitability** | ⚠️ Basic CRUD | ✅ + Barcode, Reorder, CSV | High |

---

## Architecture Layers

```
┌─────────────────────────────────────┐
│          ConsoleUI (UI Layer)        │  ← user interaction only
├─────────────────────────────────────┤
│      InventoryService (Logic Layer)  │  ← pure business rules
├─────────────────────────────────────┤
│  InventoryRepository (Data Layer)   │  ← JSON read/write
├─────────────────────────────────────┤
│        Product (Model Layer)        │  ← data structure
└─────────────────────────────────────┘
```
