from db import get_connection
from models.payment import Payment

class PaymentRepository:
    def get_payment_by_stage(self, stage_id=None, sub_stage_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            if stage_id:
                cursor.execute("SELECT id_payment, stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum FROM payment WHERE stages_id_stages = %s", (stage_id,))
            else:
                cursor.execute(
                    "SELECT id_payment, stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum FROM payment WHERE sub_stage_id_sub_stage = %s",
                    (sub_stage_id,))
            rows = cursor.fetchall()
            payment = [
                Payment(
                    id_payment=row[0],
                    stages_id_stages=row[1],
                    matherial_purchased_id_matherial=row[2],
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
        return payment

    def get_name_and_unit_by_id(self, matherial_id):
        connection = get_connection()  # Функція для отримання підключення до бази даних
        cursor = connection.cursor(dictionary=True)  # Використовуємо dict для зручного доступу до результатів
        try:
            # SQL-запит для отримання матеріалу за ID
            query = "SELECT matherial_name, unit FROM payment WHERE id_payment = %s;"
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

    def take_stage_id_by_payment_id(self, payment_id=None, payment_sub_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            # SQL-запит для отримання stage_id за matherial_id
            if payment_id:
                query = """
                        SELECT s.id_stages
                        FROM stages s
                        JOIN payment p ON s.id_stages = p.stages_id_stages
                        WHERE p.id_payment = %s
                    """
                cursor.execute(query, (payment_id,))
            elif payment_sub_id:
                query = """
                                        SELECT s.id_sub_stage
                                        FROM sub_stage s
                                        JOIN payment p ON s.id_sub_stage = p.sub_stage_id_sub_stage
                                        WHERE p.id_payment = %s
                                    """
                cursor.execute(query, (payment_sub_id,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Повертаємо stage_id
            else:
                return None  # Якщо нічого не знайдено
        finally:
            cursor.close()
            connection.close()

    def add_payment(self, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum, stages_id_stages=None, sub_stages_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        if stages_id_stages:
            cursor.execute("INSERT INTO payment (stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s, %s)", (stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum))
        else:
            cursor.execute(
                "INSERT INTO payment (sub_stage_id_sub_stage, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (sub_stages_id, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum))
        connection.commit()
        cursor.close()
        connection.close()

    def update_payment_by_matherial_purch_id(self, material_purch_id, matherial_name=None, unit=None, amount=None, price=None, sum=None):
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
                params.append(material_purch_id)

                # Формуємо SQL-запит
                query = f"UPDATE payment SET {', '.join(update_fields)} WHERE matherial_purchased_id_matherial = %s"

                # Перевіряємо, що параметри та запит правильно сформовані
                print(f"Запит: {query}")
                print(f"Параметри: {params}")

                # Виконуємо SQL-запит
                cursor.execute(query, params)
                connection.commit()

    def update_payment(self, payment_id, matherial_name=None, unit=None, amount=None, price=None, sum=None):
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
                params.append(payment_id)

                # Формуємо SQL-запит
                query = f"UPDATE payment SET {', '.join(update_fields)} WHERE id_payment = %s"

                # Перевіряємо, що параметри та запит правильно сформовані
                print(f"Запит: {query}")
                print(f"Параметри: {params}")

                # Виконуємо SQL-запит
                cursor.execute(query, params)
                connection.commit()
    def get_payment_by_id(self, id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT id_payment, stages_id_stages, matherial_purchased_id_matherial, matherial_name, unit, amount, price, sum FROM payment WHERE id_payment = %s",
                (id_matherial,))
            rows = cursor.fetchall()
            matherial = [
                Payment(
                    id_payment=row[0],
                    stages_id_stages=row[1],
                    matherial_purchased_id_matherial=row[2],
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
    def delete_payment(self, id_payment):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM payment WHERE id_payment = %s", (id_payment,))
        connection.commit()
        cursor.close()
        connection.close()
