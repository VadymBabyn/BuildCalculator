from repository.sub_stage_repository import SubStageRepository

class SubStageService:
    def __init__(self):
        self.stage_repo = SubStageRepository()

    def get_all_sub_stages(self):
        # Користувачі та адміни можуть переглядати будинки
        return self.stage_repo.get_all_sub_stages()

    def get_sub_stages(self, stage_id):
        return self.stage_repo.get_stages_by_stage(stage_id)

    def get_sub_stage_name_by_id(self, sub_stage_id):
        return self.stage_repo.take_sub_stage_name_by_sub_stage_id(sub_stage_id)

    def add_sub_stage(self, is_admin, stage_id, sub_stage_name):
        if is_admin==True:
            self.stage_repo.add_stage(stage_id, sub_stage_name)
        else:
            return

    def update_sub_stage(self, is_admin, sub_stage_id, sub_stage_name):
        if is_admin == True:
            self.stage_repo.update_stage(sub_stage_id, sub_stage_name)
        else:
            return

    def delete_sub_stage(self, is_admin, sub_stage_id):
        if is_admin == True:
            self.stage_repo.delete_stage(sub_stage_id)
        else:
            return
