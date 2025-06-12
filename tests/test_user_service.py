import pytest
from unittest.mock import MagicMock
from service.user_service import UserService
from utils.password_utils import hash_password

@pytest.fixture
def user_service_with_mock_repo():
    service = UserService()
    service.user_repo = MagicMock()
    return service

def test_authenticate_user_success(user_service_with_mock_repo):
    service = user_service_with_mock_repo
    fake_user = MagicMock()
    fake_user.password = hash_password("secret123")
    service.user_repo.get_user_by_username.return_value = fake_user

    result = service.authenticate_user("username", "secret123")
    assert result == fake_user

def test_authenticate_user_wrong_password(user_service_with_mock_repo):
    service = user_service_with_mock_repo
    fake_user = MagicMock()
    fake_user.password = hash_password("secret123")
    service.user_repo.get_user_by_username.return_value = fake_user

    result = service.authenticate_user("username", "wrongpass")
    assert result is None

def test_authenticate_user_no_user(user_service_with_mock_repo):
    service = user_service_with_mock_repo
    service.user_repo.get_user_by_username.return_value = None

    result = service.authenticate_user("username", "password")
    assert result is None

def test_register_user_success(user_service_with_mock_repo):
    service = user_service_with_mock_repo
    service.user_repo.get_user_by_username.return_value = None

    service.register_user("newuser", "password123")
    service.user_repo.add_user.assert_called_once()
    args, kwargs = service.user_repo.add_user.call_args
    assert args[0] == "newuser"

def test_register_user_existing_username_raises(user_service_with_mock_repo):
    service = user_service_with_mock_repo
    service.user_repo.get_user_by_username.return_value = MagicMock()

    with pytest.raises(Exception) as e:
        service.register_user("existinguser", "password123")
    assert str(e.value) == "Username already exists."
