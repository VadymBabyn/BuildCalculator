from db import get_connection
from models.matherial import Matherial

class MatherialRepository:
    def get_matherial_by_stage(self, stage_id=None, sub_stage_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        if stage_id:
            try:
                cursor.execute("SELECT id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial WHERE stages_id_matherial = %s", (stage_id,))
                rows = cursor.fetchall()
                matherial = [
                    Matherial(
                        id_matherial=row[0],
                        stages_id_matherial=row[1],
                        matherial_name=row[2],
                        unit=row[3],
                        amount=row[4],
                        price=row[5],
                        sum=row[6]
                    )
                    for row in rows
                ]
            finally:
                cursor.close()
                connection.close()
        else:
            try:
                cursor.execute("SELECT id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial WHERE sub_stage_id_sub_stage = %s", (sub_stage_id,))
                rows = cursor.fetchall()
                matherial = [
                    Matherial(
                        id_matherial=row[0],
                        stages_id_matherial=row[1],
                        matherial_name=row[2],
                        unit=row[3],
                        amount=row[4],
                        price=row[5],
                        sum=row[6]
                    )
                    for row in rows
                ]
            finally:
                cursor.close()
                connection.close()
        return matherial

    def get_id_material(self,  material_name, unit, amount, price, stage_id_material=None, sub_stage_id_material=None):
        connection = get_connection()
        cursor = connection.cursor()
        if stage_id_material:
            try:
                # Виконання SQL-запиту для отримання id_matherial
                cursor.execute(
                    "SELECT id_matherial FROM matherial WHERE stages_id_matherial = %s AND matherial_name = %s AND unit = %s AND amount = %s AND price = %s",
                    (stage_id_material, material_name, unit, amount, price)
                )
                # Отримання першого результату (або None, якщо даних немає)
                result = cursor.fetchone()
                return result[0] if result else None
            finally:
                cursor.close()
                connection.close()
        elif sub_stage_id_material:
            try:
                # Виконання SQL-запиту для отримання id_matherial
                cursor.execute(
                    "SELECT id_matherial FROM matherial WHERE sub_stage_id_sub_stage = %s AND matherial_name = %s AND unit = %s AND amount = %s AND price = %s",
                    (sub_stage_id_material, material_name, unit, amount, price)
                )
                # Отримання першого результату (або None, якщо даних немає)
                result = cursor.fetchone()
                return result[0] if result else None
            finally:
                cursor.close()
                connection.close()


    def add_material(self,  matherial_name, unit, amount, price, sum, stages_id_material=None, sub_stage_id_matherial=None):
        connection = get_connection()
        cursor = connection.cursor()
        if stages_id_material:
            cursor.execute("INSERT INTO matherial (stages_id_matherial, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s)", (stages_id_material, matherial_name, unit, amount, price, sum))
        elif sub_stage_id_matherial:
            cursor.execute("INSERT INTO matherial (sub_stage_id_sub_stage, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s)", (sub_stage_id_matherial, matherial_name, unit, amount, price, sum))
        connection.commit()
        cursor.close()
        connection.close()

    def update_material(self, material_id, matherial_name=None, unit=None, amount=None, price=None, sum=None):
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                # Формуємо SQL-запит для оновлення тільки тих полів, які були передані
                update_fields = []
                params = []

                if matherial_name is not None:
                    update_fields.append("matherial_name = %s")
                    params.append(matherial_name)
                if unit is not None:
                    update_fields.append("unit = %s")
                    params.append(unit)
                if amount is not None:
                    update_fields.append("amount = %s")
                    params.append(amount)
                if price is not None:
                    update_fields.append("price = %s")
                    params.append(price)
                if sum is not None:
                    update_fields.append("sum = %s")
                    params.append(sum)

                if not update_fields:
                    print("Немає змінених значень для оновлення.")
                    return  # або обробіть це іншим способом

                # Додаємо ID матеріалу в кінці списку параметрів для використання в WHERE
                params.append(material_id)

                # Формуємо SQL-запит
                query = f"UPDATE matherial SET {', '.join(update_fields)} WHERE id_matherial = %s"

                # Перевіряємо, що параметри та запит правильно сформовані
                print(f"Запит: {query}")
                print(f"Параметри: {params}")

                # Виконуємо SQL-запит
                cursor.execute(query, params)
                connection.commit()

    def delete_material(self, id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM matherial WHERE id_matherial = %s", (id_matherial,))
        connection.commit()                                                             ## доробити
        cursor.close()
        connection.close()
