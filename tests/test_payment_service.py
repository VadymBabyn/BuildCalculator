import pytest
from unittest.mock import MagicMock
from service.payment_service import PaymentService

@pytest.fixture
def payment_service_with_mocks():
    service = PaymentService()
    service.payment_repo = MagicMock()
    return service

def test_get_payment_calls_repo(payment_service_with_mocks):
    service = payment_service_with_mocks
    service.get_payment(1, 2)
    service.payment_repo.get_payment_by_stage.assert_called_once_with(1, 2)

def test_get_name_and_unit_calls_repo(payment_service_with_mocks):
    service = payment_service_with_mocks
    service.get_name_and_unit(5)
    service.payment_repo.get_name_and_unit_by_id.assert_called_once_with(5)

def test_add_payment_admin_calls_add(payment_service_with_mocks):
    service = payment_service_with_mocks
    service.add_payment(True, 1, 2, 3, "mat", "kg", 10, 5)
    service.payment_repo.add_payment.assert_called_once_with(3, "mat", "kg", 10, 5, 50, 1, 2)

def test_add_payment_non_admin_does_nothing(payment_service_with_mocks):
    service = payment_service_with_mocks
    result = service.add_payment(False, 1, 2, 3, "mat", "kg", 10, 5)
    assert result is None
    service.payment_repo.add_payment.assert_not_called()

def test_purchase_payment_admin_updates(payment_service_with_mocks):
    service = payment_service_with_mocks
    # Мокаємо повернення з get_payment_by_id
    mock_payment = [MagicMock()]
    mock_payment[0].sum = 100
    mock_payment[0].amount = 10
    service.payment_repo.get_payment_by_id.return_value = mock_payment

    service.purchase_payment(True, 1, 5, 20)

    done_sum = 100 + 5*20  # 100 + 100 = 200
    done_amount = 10 + 5  # 15
    price = done_sum / done_amount  # 200 / 15 ≈ 13.3333

    service.payment_repo.update_payment.assert_called_once_with(1, None, None, done_amount, price, done_sum)

def test_purchase_payment_non_admin_does_nothing(payment_service_with_mocks):
    service = payment_service_with_mocks
    result = service.purchase_payment(False, 1, 5, 20)
    assert result is None
    service.payment_repo.get_payment_by_id.assert_not_called()
    service.payment_repo.update_payment.assert_not_called()

def test_update_payment_admin_calls_update(payment_service_with_mocks):
    service = payment_service_with_mocks
    service.update_payment(True, 1, material_name="mat", amount=10, price=5)
    service.payment_repo.update_payment.assert_called_once_with(1, "mat", None, 10, 5, 50)

def test_update_payment_non_admin_does_nothing(payment_service_with_mocks):
    service = payment_service_with_mocks
    result = service.update_payment(False, 1, material_name="mat")
    assert result is None
    service.payment_repo.update_payment.assert_not_called()

def test_delete_payment_admin_calls_delete(payment_service_with_mocks):
    service = payment_service_with_mocks
    service.delete_payment(True, 1)
    service.payment_repo.delete_payment.assert_called_once_with(1)

def test_delete_payment_non_admin_does_nothing(payment_service_with_mocks):
    service = payment_service_with_mocks
    result = service.delete_payment(False, 1)
    assert result is None
    service.payment_repo.delete_payment.assert_not_called()
