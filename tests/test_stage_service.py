import pytest
from unittest.mock import MagicMock
from service.stage_service import StageService

@pytest.fixture
def stage_service_with_mocks():
    service = StageService()
    service.stage_repo = MagicMock()
    return service

def test_get_all_stages_calls_repo(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.get_all_stages()
    service.stage_repo.get_all_stages.assert_called_once()

def test_get_stages_calls_repo(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.get_stages(10)
    service.stage_repo.get_stages_by_house.assert_called_once_with(10)

def test_get_stage_name_by_id_calls_repo(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.get_stage_name_by_id(5)
    service.stage_repo.take_stage_name_by_stage_id.assert_called_once_with(5)

def test_add_stage_admin_calls_add(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.add_stage(True, 1, "New Stage")
    service.stage_repo.add_stage.assert_called_once_with(1, "New Stage")

def test_add_stage_non_admin_does_nothing(stage_service_with_mocks):
    service = stage_service_with_mocks
    result = service.add_stage(False, 1, "New Stage")
    assert result is None
    service.stage_repo.add_stage.assert_not_called()

def test_update_stage_admin_calls_update(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.update_stage(True, 2, "Updated Stage")
    service.stage_repo.update_stage.assert_called_once_with(2, "Updated Stage")

def test_update_stage_non_admin_does_nothing(stage_service_with_mocks):
    service = stage_service_with_mocks
    result = service.update_stage(False, 2, "Updated Stage")
    assert result is None
    service.stage_repo.update_stage.assert_not_called()

def test_delete_stage_admin_calls_delete(stage_service_with_mocks):
    service = stage_service_with_mocks
    service.delete_stage(True, 3)
    service.stage_repo.delete_stage.assert_called_once_with(3)

def test_delete_stage_non_admin_does_nothing(stage_service_with_mocks):
    service = stage_service_with_mocks
    result = service.delete_stage(False, 3)
    assert result is None
    service.stage_repo.delete_stage.assert_not_called()
