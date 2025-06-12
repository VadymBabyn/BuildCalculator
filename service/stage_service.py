from repository.stage_repository import StageRepository

class StageService:
    def __init__(self):
        self.stage_repo = StageRepository()

    def get_all_stages(self):
        # Користувачі та адміни можуть переглядати будинки
        return self.stage_repo.get_all_stages()

    def get_stages(self, house_id):
        return self.stage_repo.get_stages_by_house(house_id)

    def get_stage_name_by_id(self, stage_id):
        return self.stage_repo.take_stage_name_by_stage_id(stage_id)

    def add_stage(self, is_admin, house_id, stage_name):
        if is_admin==True:
            self.stage_repo.add_stage(house_id, stage_name)
        else:
            return

    def update_stage(self, is_admin, stage_id, stage_name):
        if is_admin == True:
            self.stage_repo.update_stage(stage_id, stage_name)
        else:
            return

    def delete_stage(self, is_admin, stage_id):
        if is_admin == True:
            self.stage_repo.delete_stage(stage_id)
        else:
            return
