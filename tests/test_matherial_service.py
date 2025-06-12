import pytest
from unittest.mock import MagicMock
from service.matherial_service import MatherialService

@pytest.fixture
def service_with_mocks():
    service = MatherialService()
    service.matherial_repo = MagicMock()
    service.matherial_purch_repo = MagicMock()
    service.payment_repo = MagicMock()
    return service

def test_get_matherial_calls_repo(service_with_mocks):
    service = service_with_mocks
    service.get_matherial(1, 2)
    service.matherial_repo.get_matherial_by_stage.assert_called_once_with(1, 2)

def test_add_matherial_with_stage_id_admin_calls_all_repos(service_with_mocks):
    service = service_with_mocks
    # Підготувати значення, які будуть повертати get_id_material
    service.matherial_repo.get_id_material.return_value = 1
    service.matherial_purch_repo.get_id_material.return_value = 2

    service.add_matherial(True, "mat", "kg", 10, 5, stages_id_matherial=3)

    service.matherial_repo.add_material.assert_called_once_with("mat", "kg", 10, 5, 50, 3, None)
    service.matherial_repo.get_id_material.assert_called_once_with("mat", "kg", 10, 5, 3, None)

    service.matherial_purch_repo.add_material.assert_called_once_with(1, "mat", "kg", 10, 5, 50, 3, None)
    service.matherial_purch_repo.get_id_material.assert_called_once_with(1)

    service.payment_repo.add_payment.assert_called_once_with(2, "mat", "kg", 0, 0, 0, 3, None)

def test_add_matherial_with_sub_stage_id_admin_calls_all_repos(service_with_mocks):
    service = service_with_mocks
    service.matherial_repo.get_id_material.return_value = 10
    service.matherial_purch_repo.get_id_material.return_value = 20

    service.add_matherial(True, "mat2", "l", 5, 2, sub_stage_id_matherial=7)

    service.matherial_repo.add_material.assert_called_once_with("mat2", "l", 5, 2, 10, None, 7)
    service.matherial_repo.get_id_material.assert_called_once_with("mat2", "l", 5, 2, None, 7)

    service.matherial_purch_repo.add_material.assert_called_once_with(10, "mat2", "l", 5, 2, 10, None, 7)
    service.matherial_purch_repo.get_id_material.assert_called_once_with(10)

    service.payment_repo.add_payment.assert_called_once_with(20, "mat2", "l", 0, 0, 0, None, 7)

def test_add_matherial_non_admin_does_nothing(service_with_mocks):
    service = service_with_mocks
    result = service.add_matherial(False, "mat", "kg", 10, 5, stages_id_matherial=3)
    assert result is None
    service.matherial_repo.add_material.assert_not_called()
    service.matherial_purch_repo.add_material.assert_not_called()
    service.payment_repo.add_payment.assert_not_called()

def test_update_matherial_admin_calls_update(service_with_mocks):
    service = service_with_mocks
    service.update_matherial(True, 1, material_name="mat", amount=10, price=5)
    service.matherial_repo.update_material.assert_called_once_with(1, "mat", None, 10, 5, 50)

def test_update_matherial_non_admin_does_nothing(service_with_mocks):
    service = service_with_mocks
    result = service.update_matherial(False, 1, material_name="mat")
    assert result is None
    service.matherial_repo.update_material.assert_not_called()

def test_delete_matherial_admin_calls_delete(service_with_mocks):
    service = service_with_mocks
    service.delete_matherial(True, 1)
    service.matherial_repo.delete_material.assert_called_once_with(1)

def test_delete_matherial_non_admin_does_nothing(service_with_mocks):
    service = service_with_mocks
    result = service.delete_matherial(False, 1)
    assert result is None
    service.matherial_repo.delete_material.assert_not_called()
