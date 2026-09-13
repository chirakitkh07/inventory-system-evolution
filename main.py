# main.py — Entry point: wires all components via Dependency Injection
from repositories.inventory_repository import InventoryRepository
from services.inventory_service import InventoryService
from exporters.csv_report_exporter import CsvReportExporter
from ui.console_ui import ConsoleUI


def main() -> None:
    """
    Composition root: build the dependency graph and start the app.
    All dependencies are injected here — no global state anywhere.
    """
    repo = InventoryRepository(filepath="inventory.json")
    service = InventoryService(repo=repo)
    exporter = CsvReportExporter()
    ui = ConsoleUI(service=service, exporter=exporter)
    ui.run()


if __name__ == "__main__":
    main()
