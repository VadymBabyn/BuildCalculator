from repository.matherial_purchased_repository import MatherialPurchasedRepository
from repository.payment_repository import PaymentRepository
class MatherialPurchasedService:
    def __init__(self):
        self.matherial_purch_repo = MatherialPurchasedRepository()
        self.payment_repo = PaymentRepository()
    def get_matherial(self, stage_id=None,sub_stage_id=None):
        return self.matherial_purch_repo.get_matherial_by_stage(stage_id, sub_stage_id)

    def get_name_and_unit(self, matherial_id):
        return self.matherial_purch_repo.get_name_and_unit_by_id(matherial_id)

    def take_stage_id_by_matherial_id(self, matherial_id=None, payment_id=None):
        if matherial_id:
            return self.matherial_purch_repo.take_stage_id_by_matherial_id(matherial_id)
        else:
            return self.payment_repo.take_stage_id_by_payment_id(payment_id)

    def take_sub_stage_id_by_matherial_id(self, matherial_id=None, payment_id=None):
        if matherial_id:
            return self.matherial_purch_repo.take_stage_id_by_matherial_id(None, matherial_id)
        else:
            return self.payment_repo.take_stage_id_by_payment_id(None, payment_id)

    def add_matherial(self, is_admin, stages_id_matherial, matherial_name, unit, amount, price):
        if is_admin == True:
            self.matherial_purch_repo.add_material(stages_id_matherial, matherial_name, unit, amount, price, sum)
            matherial_id = self.matherial_purch_repo.get_id_material(stages_id_matherial)
            if matherial_id:
                self.matherial_purch_repo.add_material(matherial_id, stages_id_matherial, matherial_name, unit, amount,
                                                   price, sum)
        else:
            return

    def purchase_matherial(self, is_admin, id_matherial, amount, price):
        if is_admin == True:
            matherial = self.matherial_purch_repo.get_martherial_by_id(id_matherial)
            sum = amount * price
            done_sum = matherial[0].sum + sum
            done_amount = matherial[0].amount + amount
            price = done_sum/done_amount
            self.matherial_purch_repo.update_material(id_matherial, None, None, done_amount, price, done_sum)
            self.payment_repo.update_payment_by_matherial_purch_id(id_matherial, None, None, done_amount, None, None)
        else:
            return

    def update_matherial(self, is_admin, material_id, material_name=None, unit=None, amount=None, price=None, sum=None):
        if is_admin==True:
            if amount and price:
                sum = amount * price
            self.matherial_purch_repo.update_material(material_id, material_name, unit, amount, price, sum)
        else:
            return

    def delete_matherial(self, is_admin, matherial_id):
        if is_admin==True:
            self.matherial_purch_repo.delete_material(matherial_id)
        else:
            return
