from db import get_connection
from models.matherialPurchased import MatherialPurchased

class MatherialPurchasedRepository:
    def get_matherial_by_stage(self, stage_id=None, sub_stage_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            if stage_id:
                cursor.execute("SELECT id_matherial, matherial_id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial_purchased WHERE stages_id_matherial = %s", (stage_id,))
            else:
                cursor.execute(
                    "SELECT id_matherial, matherial_id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial_purchased WHERE sub_stage_id_sub_stage = %s",
                    (sub_stage_id,))
            rows = cursor.fetchall()
            matherial = [
                MatherialPurchased(
                    id_matherial=row[0],
                    matherial_id_matherial=row[1],
                    stages_id_matherial=row[2],
                    matherial_name=row[3],
                    unit=row[4],
                    amount=row[5],
                    price=row[6],
                    sum=row[7]
                )
                for row in rows
            ]
        finally:
            cursor.close()
            connection.close()
        return matherial

    def get_name_and_unit_by_id(self, matherial_id):
        connection = get_connection()  # Функція для отримання підключення до бази даних
        cursor = connection.cursor(dictionary=True)  # Використовуємо dict для зручного доступу до результатів
        try:
            # SQL-запит для отримання матеріалу за ID
            query = "SELECT matherial_name, unit FROM matherial_purchased WHERE id_matherial = %s;"
            cursor.execute(query, (matherial_id,))

            # Отримуємо перший результат
            result = cursor.fetchone()

            # Якщо запис знайдено, повертаємо результат
            if result:
                return {
                    "matherial_name": result["matherial_name"],
                    "unit": result["unit"]
                }
            else:
                return None  # Якщо записів немає

        except Exception as e:
            print(f"Помилка отримання матеріалу: {e}")
            return None
        finally:
            # Закриваємо з'єднання
            cursor.close()
            connection.close()

    def take_stage_id_by_matherial_id(self, matherial_id= None, matherial_sub_id=None):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # SQL-запит для отримання stage_id за matherial_id
            if matherial_id:
                query = """
                        SELECT s.id_stages
                        FROM stages s
                        JOIN matherial_purchased mp ON s.id_stages = mp.stages_id_matherial
                        WHERE mp.id_matherial = %s
                    """
                cursor.execute(query, (matherial_id,))
            elif matherial_sub_id:
                query = """
                                        SELECT s.id_sub_stage
                                        FROM sub_stage s
                                        JOIN matherial_purchased mp ON s.id_sub_stage = mp.sub_stage_id_sub_stage
                                        WHERE mp.id_matherial = %s
                                    """
                cursor.execute(query, (matherial_sub_id,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Повертаємо stage_id
            else:
                return None  # Якщо нічого не знайдено
        finally:
            cursor.close()
            connection.close()

    def add_material(self, matherial_id_matherial, matherial_name, unit, amount, price, sum, stages_id_material=None, sub_stages_id_matherial=None):
        connection = get_connection()
        cursor = connection.cursor()
        amount = 0
        sum = 0
        if stages_id_material:
            cursor.execute("INSERT INTO matherial_purchased (matherial_id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s, %s)", (matherial_id_matherial, stages_id_material, matherial_name, unit, amount, price, sum))
        else:
            cursor.execute(
                "INSERT INTO matherial_purchased (matherial_id_matherial, sub_stage_id_sub_stage, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (matherial_id_matherial, sub_stages_id_matherial, matherial_name, unit, amount, price, sum))
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
                query = f"UPDATE matherial_purchased SET {', '.join(update_fields)} WHERE id_matherial = %s"

                # Перевіряємо, що параметри та запит правильно сформовані
                print(f"Запит: {query}")
                print(f"Параметри: {params}")

                # Виконуємо SQL-запит
                cursor.execute(query, params)
                connection.commit()

    def get_id_material(self, matherial_id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            # Виконання SQL-запиту для отримання id_matherial
            cursor.execute(
                "SELECT id_matherial FROM matherial_purchased WHERE matherial_id_matherial = %s",
                (matherial_id_matherial,)  # Передаємо параметр як кортеж
            )
            # Отримання першого результату (або None, якщо даних немає)
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            # Закриття курсора та з'єднання
            cursor.close()
            connection.close()

    def get_martherial_by_id(self, id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT id_matherial, matherial_id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial_purchased WHERE id_matherial = %s",
                (id_matherial,))
            rows = cursor.fetchall()
            matherial = [
                MatherialPurchased(
                    id_matherial=row[0],
                    matherial_id_matherial=row[1],
                    stages_id_matherial=row[2],
                    matherial_name=row[3],
                    unit=row[4],
                    amount=row[5],
                    price=row[6],
                    sum=row[7]
                )
                for row in rows
            ]
        finally:
            cursor.close()
            connection.close()
        return matherial
    def delete_material(self, id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM matherial WHERE id_matherial = %s", (id_matherial,))
        connection.commit()
        cursor.close()
        connection.close()
