class Payment:
    def __init__(self, id_payment, stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum):
        self.id_payment = id_payment
        self.stages_id_stages = stages_id_stages
        self.matherial_purchased_id_matherial = matherial_purchased_id_matherial
        self.matherial_name = matherial_name
        self.unit = unit
        self.amount = amount
        self.price = price
        self.sum = sum