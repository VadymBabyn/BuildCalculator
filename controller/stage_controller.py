from service.stage_service import StageService

class StageController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.stage_service = StageService()

    def view_stages(self, house_id):
        return self.stage_service.get_stages(house_id)

    def view_all_stages(self):
        # Показати всі будинки
        stages = self.stage_service.get_all_stages()
        return stages

    def get_stage_name_by_id(self, stage_id):
        return self.stage_service.get_stage_name_by_id(stage_id)

    def add_new_stage(self, house_id, stage_name):
        self.stage_service.add_stage(self.is_admin, house_id, stage_name)

    def edit_stage(self, stage_id, stage_name):
        self.stage_service.update_stage(self.is_admin, stage_id, stage_name)

    def remove_stage(self, stage_id):
        self.stage_service.delete_stage(self.is_admin, stage_id)
