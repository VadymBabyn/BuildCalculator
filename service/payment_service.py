from repository.payment_repository import PaymentRepository
class PaymentService:
    def __init__(self):
        self.payment_repo = PaymentRepository()

    def get_payment(self, stage_id=None, sub_stage_id=None):
        return self.payment_repo.get_payment_by_stage(stage_id, sub_stage_id)

    def get_name_and_unit(self, matherial_id):
        return self.payment_repo.get_name_and_unit_by_id(matherial_id)

    def add_payment(self, is_admin, stages_id_stages,sub_stage_id_sub_stage, matherial_purchased_id_matherial, matherial_name,unit, amount, price):
        if is_admin==True:
            sum = amount * price
            self.payment_repo.add_payment( matherial_purchased_id_matherial, matherial_name,unit, amount, price, sum, stages_id_stages,sub_stage_id_sub_stage)
        else:
            return
    def purchase_payment(self, is_admin, id_payment, amount, price):
        if is_admin == True:
            payment = self.payment_repo.get_payment_by_id(id_payment)
            sum = amount * price
            done_sum = payment[0].sum + sum
            done_amount = payment[0].amount + amount
            price = done_sum/done_amount
            self.payment_repo.update_payment(id_payment, None, None, done_amount, price, done_sum)
        else:
            return
    def update_payment(self, is_admin, payment_id, material_name=None, unit=None, amount=None, price=None, sum=None):
        if is_admin == True:
            if amount and price:
                sum = amount * price
            self.payment_repo.update_payment(payment_id, material_name, unit, amount, price, sum)
        else:
            return
    def delete_payment(self, is_admin, payment_id):
        if is_admin == True:
            self.payment_repo.delete_payment(payment_id)
        else:
            return