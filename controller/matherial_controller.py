from service.matherial_service import MatherialService

class MatherialController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.matherial_service = MatherialService()

    def view_matherial(self, stage_id=None, sub_stage_id=None):
        return self.matherial_service.get_matherial(stage_id, sub_stage_id)

    def add_new_matherial(self,  matherial_name, unit, amount, price, stages_id_matherial=None, sub_stage_id_matherial=None):
        self.matherial_service.add_matherial(self.is_admin, matherial_name, unit, amount, price, stages_id_matherial, sub_stage_id_matherial)

    def edit_matherial(self, material_id, material_name=None, unit=None, amount=None, price=None, sum=None):
        self.matherial_service.update_matherial(self.is_admin, material_id, material_name, unit, amount, price, sum)

    def remove_matherial(self, matherial_id):
        print("Try to remove: ",matherial_id)
        self.matherial_service.delete_matherial(self.is_admin, matherial_id)