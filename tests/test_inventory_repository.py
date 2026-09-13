# tests/test_inventory_repository.py — Unit tests for InventoryRepository

import json
import os
import pytest

from models.product import Product
from repositories.inventory_repository import InventoryRepository


@pytest.fixture
def tmp_repo(tmp_path):
    """Create a fresh InventoryRepository backed by a temp JSON file."""
    filepath = str(tmp_path / "test_inventory.json")
    return InventoryRepository(filepath=filepath)


@pytest.fixture
def repo_with_data(tmp_repo):
    """Repository pre-seeded with two products."""
    tmp_repo.add(Product(id=0, name="Widget", qty=10, price=5.00, category="Parts"))
    tmp_repo.add(Product(id=0, name="Gadget", qty=3, price=12.50, category="Electronics"))
    return tmp_repo


class TestRepositoryBasic:
    def test_empty_repo_returns_empty_list(self, tmp_repo):
        assert tmp_repo.find_all() == []

    def test_add_assigns_id(self, tmp_repo):
        p = tmp_repo.add(Product(id=0, name="Widget", qty=10, price=5.00, category="Parts"))
        assert p.id == 1

    def test_add_increments_id(self, tmp_repo):
        p1 = tmp_repo.add(Product(id=0, name="A", qty=1, price=1.0, category="X"))
        p2 = tmp_repo.add(Product(id=0, name="B", qty=2, price=2.0, category="Y"))
        assert p1.id == 1
        assert p2.id == 2

    def test_find_all_returns_all(self, repo_with_data):
        assert len(repo_with_data.find_all()) == 2

    def test_find_by_id_found(self, repo_with_data):
        p = repo_with_data.find_by_id(1)
        assert p is not None
        assert p.name == "Widget"

    def test_find_by_id_not_found(self, repo_with_data):
        assert repo_with_data.find_by_id(999) is None


class TestRepositoryPersistence:
    def test_data_persists_across_instances(self, tmp_path):
        filepath = str(tmp_path / "inv.json")
        repo1 = InventoryRepository(filepath=filepath)
        repo1.add(Product(id=0, name="Widget", qty=10, price=5.00, category="Parts"))

        repo2 = InventoryRepository(filepath=filepath)
        products = repo2.find_all()
        assert len(products) == 1
        assert products[0].name == "Widget"

    def test_missing_file_returns_empty(self, tmp_path):
        repo = InventoryRepository(filepath=str(tmp_path / "nonexistent.json"))
        assert repo.find_all() == []


class TestRepositoryUpdate:
    def test_update_existing(self, repo_with_data):
        p = repo_with_data.find_by_id(1)
        p.name = "SuperWidget"
        repo_with_data.update(p)
        assert repo_with_data.find_by_id(1).name == "SuperWidget"

    def test_update_not_found_raises(self, tmp_repo):
        p = Product(id=999, name="Ghost", qty=1, price=1.0, category="X")
        with pytest.raises(ValueError):
            tmp_repo.update(p)


class TestRepositoryDelete:
    def test_delete_existing(self, repo_with_data):
        repo_with_data.delete(1)
        assert len(repo_with_data.find_all()) == 1

    def test_delete_not_found_raises(self, tmp_repo):
        with pytest.raises(ValueError):
            tmp_repo.delete(999)
