from service.history_service import HistoryService

class HistoryController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.history_service = HistoryService()
    def view_history_by_date(self, start_date, end_date, house_id):
        return self.history_service.get_history_by_date(start_date, end_date, house_id)
    def view_history(self, matherial_purch_id=None, payment_id=None):
        return self.history_service.get_history(matherial_purch_id, payment_id)

    def add_new_history(self, provider, unit, amount, price, sum, id_matherial_purch=None, payment_id=None):
        self.history_service.add_history(self.is_admin, provider, unit, amount, price, sum, id_matherial_purch, payment_id)

    def purchase_history(self, material_id, amount=None, price=None):
        self.history_service.purchase_matherial(self.is_admin, material_id, amount, price)

    def edit_history(self, material_id, material_name=None, unit=None, amount=None, price=None, sum=None, table_as = None):
        if table_as == None:
            self.history_service.update_matherial(self.is_admin, material_id, material_name, unit, amount, price, sum)
        elif table_as == "planned":
            sum = None
            amount = None
            self.history_service.update_matherial(self.is_admin, material_id, material_name, unit, amount, price, sum)

    def remove_history(self, history_id):
        self.history_service.delete_history(self.is_admin, history_id)