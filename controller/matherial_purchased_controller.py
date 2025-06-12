from service.matherial_purchase_service import MatherialPurchasedService

class MatherialPurchasedController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.matherial_service = MatherialPurchasedService()

    def view_matherial(self, stage_id=None, sub_stage_id=None):
        return self.matherial_service.get_matherial(stage_id, sub_stage_id)

    def get_name_and_unit_by_id(self, matherial_purch_id):
        return self.matherial_service.get_name_and_unit(matherial_purch_id)

    def take_stage_id_by_matherial_id(self, matherial_id=None, payment_id=None):
        return self.matherial_service.take_stage_id_by_matherial_id(matherial_id, payment_id)

    def take_sub_stage_id_by_matherial_id(self, matherial_id=None, payment_id=None):
        return self.matherial_service.take_sub_stage_id_by_matherial_id(matherial_id, payment_id)

    def add_new_matherial(self, stages_id_matherial, matherial_name, unit, amount, price):
        self.matherial_service.add_matherial(self.is_admin, stages_id_matherial, matherial_name, unit, amount, price)

    def purchase_matherial(self, material_id, amount=None, price=None):
        self.matherial_service.purchase_matherial(self.is_admin, material_id, amount, price)

    def edit_matherial(self, material_id, material_name=None, unit=None, amount=None, price=None, sum=None, table_as = None):
        if table_as == None:
            self.matherial_service.update_matherial(self.is_admin, material_id, material_name, unit, amount, price, sum)
        elif table_as == "planned":
            sum = None
            amount = None
            self.matherial_service.update_matherial(self.is_admin, material_id, material_name, unit, amount, price, sum)

    def remove_matherial(self, matherial_id):
        self.matherial_service.delete_matherial(self.is_admin, matherial_id)