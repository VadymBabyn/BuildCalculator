from db import get_connection
from models.house import House

class HouseRepository:
    def get_all_houses(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM houses")
        rows = cursor.fetchall()
        # Передаємо photo до House
        houses = [House(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        cursor.close()
        connection.close()
        return houses

    def add_house(self, name, address, floors):
        connection = get_connection()
        cursor = connection.cursor()
        # Додаємо photo до SQL запиту
        cursor.execute("INSERT INTO houses (photo, name, address, floors) VALUES (%s, %s, %s, %s)", ("photo/Build2.jpg", name, address, floors))
        connection.commit()
        cursor.close()
        connection.close()

    def update_house(self, house_id, photo, name, address, floors):
        connection = get_connection()
        cursor = connection.cursor()
        # Додаємо photo до SQL запиту
        cursor.execute("UPDATE houses SET photo=%s, name=%s, address=%s, floors=%s WHERE id=%s", (photo, name, address, floors, house_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_house(self, house_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM houses WHERE id=%s", (house_id,))
        connection.commit()
        cursor.close()
        connection.close()
