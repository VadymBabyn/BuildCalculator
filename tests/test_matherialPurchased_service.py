import pytest
from unittest.mock import MagicMock
from service.matherial_purchase_service import MatherialPurchasedService

@pytest.fixture
def service_with_mock_repos():
    service = MatherialPurchasedService()
    service.matherial_purch_repo = MagicMock()
    service.payment_repo = MagicMock()
    return service

def test_get_matherial_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    service.get_matherial(1, 2)
    service.matherial_purch_repo.get_matherial_by_stage.assert_called_once_with(1, 2)

def test_get_name_and_unit_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    service.get_name_and_unit(10)
    service.matherial_purch_repo.get_name_and_unit_by_id.assert_called_once_with(10)

def test_take_stage_id_by_matherial_id_when_matherial_id(service_with_mock_repos):
    service = service_with_mock_repos
    service.take_stage_id_by_matherial_id(matherial_id=5)
    service.matherial_purch_repo.take_stage_id_by_matherial_id.assert_called_once_with(5)
    service.payment_repo.take_stage_id_by_payment_id.assert_not_called()

def test_take_stage_id_by_matherial_id_when_payment_id(service_with_mock_repos):
    service = service_with_mock_repos
    service.take_stage_id_by_matherial_id(payment_id=7)
    service.payment_repo.take_stage_id_by_payment_id.assert_called_once_with(7)
    service.matherial_purch_repo.take_stage_id_by_matherial_id.assert_not_called()

def test_take_sub_stage_id_by_matherial_id_when_matherial_id(service_with_mock_repos):
    service = service_with_mock_repos
    service.take_sub_stage_id_by_matherial_id(matherial_id=8)
    service.matherial_purch_repo.take_stage_id_by_matherial_id.assert_called_once_with(None, 8)
    service.payment_repo.take_stage_id_by_payment_id.assert_not_called()

def test_take_sub_stage_id_by_matherial_id_when_payment_id(service_with_mock_repos):
    service = service_with_mock_repos
    service.take_sub_stage_id_by_matherial_id(payment_id=9)
    service.payment_repo.take_stage_id_by_payment_id.assert_called_once_with(None, 9)
    service.matherial_purch_repo.take_stage_id_by_matherial_id.assert_not_called()

def test_add_matherial_admin_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    # sum не передається у сервіс — треба підставити якийсь dummy sum
    service.matherial_purch_repo.get_id_material.return_value = 1
    service.add_matherial(True, 1, "mat", "kg", 10, 5)
    # Перевіряємо, що виклик відбувся двічі (за логікою сервісу)
    assert service.matherial_purch_repo.add_material.call_count == 2
    service.matherial_purch_repo.get_id_material.assert_called_once_with(1)

def test_add_matherial_non_admin_no_call(service_with_mock_repos):
    service = service_with_mock_repos
    result = service.add_matherial(False, 1, "mat", "kg", 10, 5)
    assert result is None
    service.matherial_purch_repo.add_material.assert_not_called()

def test_purchase_matherial_admin_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    fake_material = [MagicMock(sum=100, amount=10)]
    service.matherial_purch_repo.get_martherial_by_id.return_value = fake_material

    service.purchase_matherial(True, 1, 5, 20)
    service.matherial_purch_repo.update_material.assert_called_once()
    service.payment_repo.update_payment_by_matherial_purch_id.assert_called_once()

def test_purchase_matherial_non_admin_no_call(service_with_mock_repos):
    service = service_with_mock_repos
    result = service.purchase_matherial(False, 1, 5, 20)
    assert result is None
    service.matherial_purch_repo.update_material.assert_not_called()
    service.payment_repo.update_payment_by_matherial_purch_id.assert_not_called()

def test_update_matherial_admin_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    service.update_matherial(True, 1, material_name="name", amount=10, price=5)
    service.matherial_purch_repo.update_material.assert_called_once()

def test_update_matherial_non_admin_no_call(service_with_mock_repos):
    service = service_with_mock_repos
    result = service.update_matherial(False, 1)
    assert result is None
    service.matherial_purch_repo.update_material.assert_not_called()

def test_delete_matherial_admin_calls_repo(service_with_mock_repos):
    service = service_with_mock_repos
    service.delete_matherial(True, 1)
    service.matherial_purch_repo.delete_material.assert_called_once_with(1)

def test_delete_matherial_non_admin_no_call(service_with_mock_repos):
    service = service_with_mock_repos
    result = service.delete_matherial(False, 1)
    assert result is None
    service.matherial_purch_repo.delete_material.assert_not_called()