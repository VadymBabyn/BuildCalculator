import pytest
from unittest.mock import MagicMock
from service.house_service import HouseService

@pytest.fixture
def service_with_mock_repo():
    service = HouseService()
    service.house_repo = MagicMock()
    return service

def test_get_houses_calls_repo(service_with_mock_repo):
    service = service_with_mock_repo
    service.get_houses(user_role=True)
    service.house_repo.get_all_houses.assert_called_once()

def test_change_photo_admin_calls_change_photo(service_with_mock_repo):
    service = service_with_mock_repo
    service.change_photo(True, 1, "path/to/photo.jpg")
    service.house_repo.change_photo.assert_called_once_with(1, "path/to/photo.jpg")

def test_change_photo_non_admin_does_nothing(service_with_mock_repo):
    service = service_with_mock_repo
    result = service.change_photo(False, 1, "path/to/photo.jpg")
    assert result is None
    service.house_repo.change_photo.assert_not_called()

def test_add_house_admin_calls_add_house(service_with_mock_repo):
    service = service_with_mock_repo
    service.add_house(True, "House A", "123 Street", 5)
    service.house_repo.add_house.assert_called_once_with("House A", "123 Street", 5)

def test_add_house_non_admin_does_nothing(service_with_mock_repo):
    service = service_with_mock_repo
    result = service.add_house(False, "House A", "123 Street", 5)
    assert result is None
    service.house_repo.add_house.assert_not_called()

def test_update_house_admin_calls_update_house(service_with_mock_repo):
    service = service_with_mock_repo
    service.update_house(True, 1, "House B", "456 Avenue", 10)
    service.house_repo.update_house.assert_called_once_with(1, "House B", "456 Avenue", 10)

def test_update_house_non_admin_does_nothing(service_with_mock_repo):
    service = service_with_mock_repo
    result = service.update_house(False, 1, "House B", "456 Avenue", 10)
    assert result is None
    service.house_repo.update_house.assert_not_called()

def test_delete_house_admin_calls_delete_house(service_with_mock_repo):
    service = service_with_mock_repo
    service.delete_house(True, 1)
    service.house_repo.delete_house.assert_called_once_with(1)

def test_delete_house_non_admin_does_nothing(service_with_mock_repo):
    service = service_with_mock_repo
    result = service.delete_house(False, 1)
    assert result is None
    service.house_repo.delete_house.assert_not_called()
