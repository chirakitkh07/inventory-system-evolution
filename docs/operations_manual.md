# System Operations and Maintenance Manual
## Inventory Management System v2.0
### Conforming to ISO/IEC 14764 Software Maintenance Standard

---

## 1. System Overview

The Inventory Management System (IMS) v2.0 is a command-line Python application for managing product inventory. It replaces the legacy `app_v1.py` monolithic script with a clean Repository Pattern architecture.

**Key components:**
- `main.py` — Entry point
- `models/product.py` — Data model
- `repositories/inventory_repository.py` — JSON persistence
- `services/inventory_service.py` — Business logic
- `ui/console_ui.py` — User interface
- `exporters/csv_report_exporter.py` — CSV reporting
- `inventory.json` — Data file (auto-created on first run)

---

## 2. Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Quick Start
```bash
# Windows
setup.bat

# Linux / macOS
bash setup.sh

# Manual
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
python main.py
```

### Docker
```bash
docker build -t inventory-system:2.0.0 .
docker run -it -v ./data:/app/data inventory-system:2.0.0
```

---

## 3. Operational Procedures

### Starting the Application
```bash
python main.py
```

### Running Tests
```bash
python -m pytest test_app.py tests/ -v
```

### Security Scan
```bash
python -m bandit -r . -ll --exclude ./.venv,./.git,./tests
```

### Exporting Reports
From the application menu, choose option **8** (Export CSV). Reports are saved as UTF-8 BOM-encoded CSV files compatible with Microsoft Excel.

---

## 4. Backup and Data Management

The inventory data is stored in `inventory.json`. Back up this file regularly:

```bash
# Manual backup
copy inventory.json inventory_backup_%date%.json   # Windows
cp inventory.json inventory_backup_$(date +%F).json  # Linux
```

---

## 5. Maintenance Classification (ISO 14764)

| Type | Description | Example |
|------|-------------|---------|
| **Corrective** | Fix defects found in production | Bug in reorder alert |
| **Adaptive** | Update for new environment | Python 3.14 compatibility |
| **Perfective** | Add features / performance | New search filter |
| **Preventive** | Restructure for future ease | Dependency refactoring |

---

## 6. Version History

| Version | Date | Type | Description |
|---------|------|------|-------------|
| v1.0.0-baseline | Week 1 | — | Legacy monolithic script |
| v2.0.0-evolution | Week 12 | Perfective + Corrective | Full refactor, barcode, reorder, CSV |
| v2.0.0-final | Week 15 | — | Production closure |

---

## 7. Contact and Escalation

For maintenance requests, file a Jira ticket with prefix `ENGSE-` and assign to the development team.
