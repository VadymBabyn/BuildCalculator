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
