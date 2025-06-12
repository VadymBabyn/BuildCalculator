from db import get_connection
from models.stage import Stage

class StageRepository:
    def get_stages_by_house(self, house_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stages WHERE id_stages_of_house = %s", (house_id,))
        rows = cursor.fetchall()
        stages = [Stage(row[0], row[1], row[2]) for row in rows]
        cursor.close()
        connection.close()
        return stages

    def take_stage_name_by_stage_id(self, stage_id):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            # SQL-запит для отримання імені етапу за його ID
            query = "SELECT stage_name FROM stages WHERE id_stages = %s"
            cursor.execute(query, (stage_id,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Повертаємо stage_name
            else:
                return None  # Якщо нічого не знайдено
        finally:
            cursor.close()
            connection.close()

    def get_all_stages(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stages")
        rows = cursor.fetchall()
        # Передаємо stage
        stages = [Stage(row[0], row[1], row[2]) for row in rows]
        cursor.close()
        connection.close()
        return stages

    def add_stage(self, id_stages_of_house, stage_name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO stages (id_stages_of_house, stage_name) VALUES (%s, %s)", (id_stages_of_house, stage_name))
        connection.commit()
        cursor.close()
        connection.close()

    def update_stage(self, id_stages, stage_name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE stages SET stage_name = %s WHERE id_stages = %s", (stage_name, id_stages))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_stage(self, id_stages):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM stages WHERE id_stages = %s", (id_stages,))
        connection.commit()
        cursor.close()
        connection.close()
