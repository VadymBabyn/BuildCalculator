import pytest
from unittest.mock import MagicMock
from service.sub_stage_service import SubStageService

@pytest.fixture
def sub_stage_service_with_mocks():
    service = SubStageService()
    service.stage_repo = MagicMock()
    return service

def test_get_all_sub_stages_calls_repo(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.get_all_sub_stages()
    service.stage_repo.get_all_sub_stages.assert_called_once()

def test_get_sub_stages_calls_repo(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.get_sub_stages(10)
    service.stage_repo.get_stages_by_stage.assert_called_once_with(10)

def test_get_sub_stage_name_by_id_calls_repo(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.get_sub_stage_name_by_id(5)
    service.stage_repo.take_sub_stage_name_by_sub_stage_id.assert_called_once_with(5)

def test_add_sub_stage_admin_calls_add(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.add_sub_stage(True, 1, "New SubStage")
    service.stage_repo.add_stage.assert_called_once_with(1, "New SubStage")

def test_add_sub_stage_non_admin_does_nothing(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    result = service.add_sub_stage(False, 1, "New SubStage")
    assert result is None
    service.stage_repo.add_stage.assert_not_called()

def test_update_sub_stage_admin_calls_update(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.update_sub_stage(True, 2, "Updated SubStage")
    service.stage_repo.update_stage.assert_called_once_with(2, "Updated SubStage")

def test_update_sub_stage_non_admin_does_nothing(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    result = service.update_sub_stage(False, 2, "Updated SubStage")
    assert result is None
    service.stage_repo.update_stage.assert_not_called()

def test_delete_sub_stage_admin_calls_delete(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    service.delete_sub_stage(True, 3)
    service.stage_repo.delete_stage.assert_called_once_with(3)

def test_delete_sub_stage_non_admin_does_nothing(sub_stage_service_with_mocks):
    service = sub_stage_service_with_mocks
    result = service.delete_sub_stage(False, 3)
    assert result is None
    service.stage_repo.delete_stage.assert_not_called()
