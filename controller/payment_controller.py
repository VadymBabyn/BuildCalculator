from service.payment_service import PaymentService

class PaymentController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.payment_service = PaymentService()

    def view_payment(self, stage_id=None, sub_stage_id=None):
        return self.payment_service.get_payment(stage_id, sub_stage_id)

    def get_name_and_unit_by_id(self, matherial_payment_id):
        return self.payment_service.get_name_and_unit(matherial_payment_id)

    def add_new_payment(self, stages_id_stages, sub_stage_id_sub_stage, matherial_purchased_id_matherial, matherial_name, unit, amount, price):
        self.payment_service.add_payment(self.is_admin, stages_id_stages, sub_stage_id_sub_stage, matherial_purchased_id_matherial, matherial_name,unit, amount, price)

    def purchase_payment(self, payment_id, amount=None, price=None):
        self.payment_service.purchase_payment(self.is_admin, payment_id, amount, price)

    def edit_payment(self, payment_id, material_name=None, unit=None, amount=None, price=None, sum=None, table_as = None):
        if table_as == "payment":
            self.payment_service.update_payment(self.is_admin, payment_id, material_name, unit, amount, price, sum)

    def remove_matherial(self, matherial_id):
        self.payment_service.delete_payment(self.is_admin, matherial_id)