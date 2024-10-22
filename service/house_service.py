from repository.house_repository import HouseRepository

class HouseService:
    def __init__(self):
        self.house_repo = HouseRepository()

    def get_houses(self, user_role):
        # Користувачі та адміни можуть переглядати будинки
        return self.house_repo.get_all_houses()

    def add_house(self, user_role, name, address, floors):
        if user_role == True:
            self.house_repo.add_house(name, address, floors)
        else:
            raise PermissionError("You do not have permission to add houses")

    def update_house(self, user_role, house_id, photo, name, address, floors):
        if user_role == 'admin':
            self.house_repo.update_house(house_id, photo, name, address, floors)
        else:
            raise PermissionError("You do not have permission to edit houses")

    def delete_house(self, user_role, house_id):
        if user_role == 'admin':
            self.house_repo.delete_house(house_id)
        else:
            raise PermissionError("You do not have permission to delete houses")
