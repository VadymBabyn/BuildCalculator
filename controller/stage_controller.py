from service.stage_service import StageService

class StageController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.stage_service = StageService()

    def view_stages(self, house_id):
        return self.stage_service.get_stages(house_id)

    def add_new_stage(self, house_id, stage_name):
        self.stage_service.add_stage(house_id, stage_name)

    def edit_stage(self, stage_id, stage_name):
        self.stage_service.update_stage(stage_id, stage_name)

    def remove_stage(self, stage_id):
        self.stage_service.delete_stage(stage_id)
