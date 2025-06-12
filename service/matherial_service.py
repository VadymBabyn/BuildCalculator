from repository.matherial_repository import MatherialRepository
from repository.matherial_purchased_repository import MatherialPurchasedRepository
from repository.payment_repository import PaymentRepository
class MatherialService:
    def __init__(self):
        self.matherial_repo = MatherialRepository()
        self.matherial_purch_repo = MatherialPurchasedRepository()
        self.payment_repo = PaymentRepository()
    def get_matherial(self, stage_id=None, sub_stage=None):
        return self.matherial_repo.get_matherial_by_stage(stage_id, sub_stage)

    def add_matherial(self, is_admin, matherial_name, unit, amount, price, stages_id_matherial=None, sub_stage_id_matherial=None,):
        if stages_id_matherial:
            if is_admin ==True:
                sum = amount * price
                self.matherial_repo.add_material(matherial_name, unit, amount, price, sum, stages_id_matherial, None)
                matherial_id = self.matherial_repo.get_id_material( matherial_name, unit, amount, price, stages_id_matherial, None)
                if matherial_id:
                    self.matherial_purch_repo.add_material(matherial_id, matherial_name, unit, amount, price, sum, stages_id_matherial, None)
                    matherial_purch_id = self.matherial_purch_repo.get_id_material(matherial_id)
                    if matherial_purch_id:
                        self.payment_repo.add_payment( matherial_purch_id, matherial_name, unit, 0, 0, 0, stages_id_matherial, None)
            else:
                return
        elif sub_stage_id_matherial:
            if is_admin ==True:
                sum = amount * price
                self.matherial_repo.add_material(matherial_name, unit, amount, price, sum, None, sub_stage_id_matherial)
                matherial_id = self.matherial_repo.get_id_material(matherial_name, unit, amount, price, None, sub_stage_id_matherial)
                if matherial_id:
                    self.matherial_purch_repo.add_material(matherial_id, matherial_name, unit, amount, price, sum, None, sub_stage_id_matherial)
                    matherial_purch_id = self.matherial_purch_repo.get_id_material(matherial_id)
                    if matherial_purch_id:
                        self.payment_repo.add_payment(matherial_purch_id, matherial_name, unit, 0, 0, 0, None, sub_stage_id_matherial)
            else:
                return


    def update_matherial(self, is_admin, material_id, material_name=None, unit=None, amount=None, price=None, sum=None):
        if is_admin==True:
            if amount and price:
                sum = amount * price
            self.matherial_repo.update_material(material_id, material_name, unit, amount, price, sum)
        else:
            return


    def delete_matherial(self, is_admin, matherial_id):
        if is_admin == True:
            self.matherial_repo.delete_material(matherial_id)
        else:
            return