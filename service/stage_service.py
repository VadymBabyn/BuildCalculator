from repository.stage_repository import StageRepository

class StageService:
    def __init__(self):
        self.stage_repo = StageRepository()

    def get_stages(self, house_id):
        return self.stage_repo.get_stages_by_house(house_id)

    def add_stage(self, house_id, stage_name):
        self.stage_repo.add_stage(house_id, stage_name)

    def update_stage(self, stage_id, stage_name):
        self.stage_repo.update_stage(stage_id, stage_name)

    def delete_stage(self, stage_id):
        self.stage_repo.delete_stage(stage_id)
