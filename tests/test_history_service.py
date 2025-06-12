import pytest
from unittest.mock import MagicMock, patch
from service.history_service import HistoryService

@pytest.fixture
def service_with_mocks():
    service = HistoryService()
    # Підмінюємо репозиторії всередині сервісу моками
    service.history_repo = MagicMock()
    service.stage_repo = MagicMock()
    service.matherial_purch_repo = MagicMock()
    service.payment_repo = MagicMock()
    service.sub_stage_repo = MagicMock()
    return service

def test_get_history_calls_history_repo(service_with_mocks):
    service = service_with_mocks
    service.get_history(1, 2)
    service.history_repo.get_history_by_matherial.assert_called_once_with(1, 2)

def test_add_history_admin_true_calls_add_material(service_with_mocks):
    service = service_with_mocks
    service.add_history(True, "provider", "unit", 10, 5, 0, id_matherial_purch=1, payment_id=2)
    service.history_repo.add_material.assert_called_once_with("provider", "unit", 10, 5, 50, 1, 2)

def test_add_history_admin_false_does_nothing(service_with_mocks):
    service = service_with_mocks
    result = service.add_history(False, "provider", "unit", 10, 5, 0)
    assert result is None
    service.history_repo.add_material.assert_not_called()

def test_delete_history_admin_true_calls_delete_history(service_with_mocks):
    service = service_with_mocks
    service.delete_history(True, 123)
    service.history_repo.delete_history.assert_called_once_with(123)

def test_delete_history_admin_false_does_nothing(service_with_mocks):
    service = service_with_mocks
    result = service.delete_history(False, 123)
    assert result is None
    service.history_repo.delete_history.assert_not_called()
