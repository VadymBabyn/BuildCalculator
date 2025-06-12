from repository.history_repository import HistoryRepository
from repository.stage_repository import StageRepository
from repository.matherial_purchased_repository import MatherialPurchasedRepository
from repository.payment_repository import PaymentRepository
from repository.sub_stage_repository import SubStageRepository
class HistoryService:
    def __init__(self):
        self.history_repo = HistoryRepository()
        self.stage_repo = StageRepository()
        self.matherial_purch_repo = MatherialPurchasedRepository()
        self.payment_repo = PaymentRepository()
        self.sub_stage_repo = SubStageRepository()
    def get_history(self, matherial_purch_id=None,payment_id=None):
        return self.history_repo.get_history_by_matherial(matherial_purch_id,payment_id)

    def get_history_by_date(self, start_date, end_date, id_house):
        stages = self.stage_repo.get_stages_by_house(id_house)
        all_history = []
        for stage in stages:
            matherial_purch = self.matherial_purch_repo.get_matherial_by_stage(stage.id_stages)
            payment = self.payment_repo.get_payment_by_stage(stage.id_stages)
            substage = self.sub_stage_repo.get_stages_by_stage(stage.id_stages)

            for matherial in matherial_purch:
                history = self.history_repo.get_history_by_matherial_and_date(start_date, end_date, matherial.id_matherial)
                all_history.extend(history)

            for pay in payment:
                history2 = self.history_repo.get_history_by_matherial_and_date(start_date, end_date, None, pay.id_payment)
                all_history.extend(history2)
            for substag in substage:
                matherial_purch_sub = self.matherial_purch_repo.get_matherial_by_stage(None, substag.id_sub_stage)
                payment_sub = self.payment_repo.get_payment_by_stage(None, substag.id_sub_stage)

                for matherial_sub in matherial_purch_sub:
                    history = self.history_repo.get_history_by_matherial_and_date(start_date, end_date,
                                                                                  matherial_sub.id_matherial)
                    all_history.extend(history)

                for pay_sub in payment_sub:
                    history2 = self.history_repo.get_history_by_matherial_and_date(start_date, end_date, None,
                                                              pay_sub.id_payment)
                    all_history.extend(history2)
        return all_history

    def add_history(self, is_admin, provider, unit, amount, price, sum, id_matherial_purch = None, payment_id = None):
        if is_admin==True:
            sum = amount * price
            self.history_repo.add_material(provider, unit, amount, price, sum, id_matherial_purch, payment_id)
        else:
            return
    def purchase_matherial(self, is_admin, id_matherial, amount, price):
        if is_admin == True:
            matherial = self.history_repo.get_martherial_by_id(id_matherial)
            sum = amount * price
            done_sum = matherial[0].sum + sum
            done_amount = matherial[0].amount + amount
            price = done_sum/done_amount
            self.history_repo.update_material(id_matherial, None, None, done_amount, price, done_sum)
        else:
            return
    def update_matherial(self, is_admin, material_id, material_name=None, unit=None, amount=None, price=None, sum=None):
        if is_admin == True:
            if amount and price:
                sum = amount * price
            self.history_repo.update_material(material_id, material_name, unit, amount, price, sum)
        else:
            return
    def delete_history(self, is_admin, history_id):
        if is_admin==True:
            self.history_repo.delete_history(history_id)
        else:
            return