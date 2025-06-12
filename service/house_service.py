from repository.house_repository import HouseRepository

class HouseService:
    def __init__(self):
        self.house_repo = HouseRepository()

    def get_houses(self, user_role):
        # Користувачі та адміни можуть переглядати будинки
        return self.house_repo.get_all_houses()

    def change_photo(self,user_role, house_id, photo_path):
        if user_role == True:
            self.house_repo.change_photo(house_id,photo_path)
        else:
            return
    def add_house(self, user_role, name, address, floors):
        if user_role == True:
            self.house_repo.add_house(name, address, floors)
        else:
            return

    def update_house(self, user_role, house_id,  name, address, floors):
        if user_role:
            self.house_repo.update_house(house_id, name, address, floors)
        else:
            return

    def delete_house(self, user_role, house_id):
        if user_role:
            self.house_repo.delete_house(house_id)
        else:
            return
