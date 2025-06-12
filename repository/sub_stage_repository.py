from db import get_connection
from models.sub_stage import Sub_Stage

class SubStageRepository:
    def get_stages_by_stage(self, stage_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sub_stage WHERE stages_id_stages = %s", (stage_id,))
        rows = cursor.fetchall()
        sub_stages = [Sub_Stage(row[0], row[1], row[2]) for row in rows]
        cursor.close()
        connection.close()
        return sub_stages

    def take_sub_stage_name_by_sub_stage_id(self, sub_stage_id):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            # SQL-запит для отримання імені етапу за його ID
            query = "SELECT sub_stage_name FROM sub_stage WHERE id_sub_stage = %s"
            cursor.execute(query, (sub_stage_id,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Повертаємо stage_name
            else:
                return None  # Якщо нічого не знайдено
        finally:
            cursor.close()
            connection.close()

    def get_all_sub_stages(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sub_stage")
        rows = cursor.fetchall()
        # Передаємо stage
        stages = [Sub_Stage(row[0], row[1], row[2]) for row in rows]
        cursor.close()
        connection.close()
        return stages

    def add_stage(self, id_stages_of_stage, sub_stage_name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sub_stage (sub_stage_name, stages_id_stages) VALUES (%s, %s)", (sub_stage_name, id_stages_of_stage))
        connection.commit()
        cursor.close()
        connection.close()

    def update_stage(self, id_sub_stage, sub_stage_name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE sub_stage SET sub_stage_name = %s WHERE id_sub_stage = %s", (sub_stage_name, id_sub_stage))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_stage(self, id_sub_stage):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sub_stage WHERE id_sub_stage = %s", (id_sub_stage,))
        connection.commit()
        cursor.close()
        connection.close()
