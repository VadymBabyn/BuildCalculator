from service.sub_stage_service import SubStageService

class SubStageController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.stage_service = SubStageService()

    def view_sub_stages(self, stage_id):
        return self.stage_service.get_sub_stages(stage_id)

    def view_all_sub_stages(self):
        # Показати всі будинки
        stages = self.stage_service.get_all_sub_stages()
        return stages

    def get_sub_stage_name_by_id(self, sub_stage_id):
        return self.stage_service.get_sub_stage_name_by_id(sub_stage_id)

    def add_new_sub_stage(self, stage_id, stage_name):
        self.stage_service.add_sub_stage(self.is_admin, stage_id, stage_name)

    def edit_sub_stage(self, sub_stage_id, stage_name):
        self.stage_service.update_sub_stage(self.is_admin, sub_stage_id, stage_name)

    def remove_sub_stage(self, sub_stage_id):
        self.stage_service.delete_sub_stage(self.is_admin, sub_stage_id)
