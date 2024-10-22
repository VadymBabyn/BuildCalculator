from service.house_service import HouseService

class HouseController:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin  # Додаємо атрибут is_admin
        self.house_service = HouseService()

    def view_houses(self):
        # Показати всі будинки
        houses = self.house_service.get_houses(self.is_admin)
        return houses

    def create_house(self, name, address, floors):
        self.house_service.add_house(self.is_admin, name, address, floors)

    def edit_house(self, house_id, photo, name, address, floors):
        self.house_service.update_house(self.is_admin, house_id, photo, name, address, floors)

    def remove_house(self, house_id):
        self.house_service.delete_house(self.is_admin, house_id)
