from db import get_connection
from models.history import History

class HistoryRepository:
    def get_history_by_matherial_and_date(self, start_date, end_date, matherial_purch_id=None, payment_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            if matherial_purch_id:
                cursor.execute(
                    "SELECT id_history, matherial_purchased_id_matherial, payment_id_payment, provider, amount, price, sum, time_buy "
                    "FROM history WHERE matherial_purchased_id_matherial = %s AND DATE(time_buy) BETWEEN %s AND %s",
                    (matherial_purch_id, start_date, end_date)
                )
            elif payment_id:
                cursor.execute(
                    "SELECT id_history, matherial_purchased_id_matherial, payment_id_payment, provider, amount, price, sum, time_buy "
                    "FROM history WHERE payment_id_payment = %s AND DATE(time_buy) BETWEEN %s AND %s",
                    (payment_id, start_date, end_date)
                )
            else:
                cursor.execute(
                    "SELECT id_history, matherial_purchased_id_matherial, payment_id_payment, provider, amount, price, sum, time_buy "
                    "FROM history WHERE DATE(time_buy) BETWEEN %s AND %s",
                    (start_date, end_date)
                )

            rows = cursor.fetchall()
            history = [
                History(
                    id_history=row[0],
                    matherial_purchased_id_matherial=row[1],
                    payment_id_payment=row[2],
                    provider=row[3],
                    amount=row[4],
                    price=row[5],
                    sum=row[6],
                    time_buy=row[7]
                )
                for row in rows
            ]
        finally:
            cursor.close()
            connection.close()
        return history

    def get_history_by_matherial(self, matherial_purch_id=None, payment_id=None):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            if matherial_purch_id:
                cursor.execute("SELECT id_history, matherial_purchased_id_matherial, payment_id_payment, provider, "
                               "amount, price, sum, time_buy FROM history WHERE matherial_purchased_id_matherial = %s",
                               (matherial_purch_id,))
            else:
                cursor.execute(
                    "SELECT id_history, matherial_purchased_id_matherial, payment_id_payment, provider, amount, price,"
                    " sum, time_buy FROM history WHERE payment_id_payment = %s",
                    (payment_id,))
            rows = cursor.fetchall()
            history = [
                History(
                    id_history=row[0],
                    matherial_purchased_id_matherial=row[1],
                    payment_id_payment=row[2],
                    provider=row[3],
                    amount=row[4],
                    price=row[5],
                    sum=row[6],
                    time_buy=row[7]
                )
                for row in rows
            ]
        finally:
            cursor.close()
            connection.close()
        return history

    def add_material(self, provider, unit, amount, price, sum, id_matherial_purch=None, payment_id=None):
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                # Формуємо списки для динамічного SQL-запиту
                columns = []
                values = []
                params = []

                if id_matherial_purch is not None:
                    columns.append("matherial_purchased_id_matherial")
                    values.append("%s")
                    params.append(id_matherial_purch)
                if payment_id is not None:
                    columns.append("payment_id_payment")
                    values.append("%s")
                    params.append(payment_id)
                if provider is not None:
                    columns.append("provider")
                    values.append("%s")
                    params.append(provider)
               #
                if amount is not None:
                    columns.append("amount")
                    values.append("%s")
                    params.append(amount)
                if price is not None:
                    columns.append("price")
                    values.append("%s")
                    params.append(price)
                if sum is not None:
                    columns.append("sum")
                    values.append("%s")
                    params.append(sum)

                if not columns:
                    print("Немає значень для створення.")
                    return

                # Формуємо SQL-запит
                query = f"INSERT INTO history ({', '.join(columns)}) VALUES ({', '.join(values)})"

                # Лог для перевірки запиту та параметрів
                print(f"Запит: {query}")
                print(f"Параметри: {params}")

                # Виконуємо SQL-запит
                cursor.execute(query, params)
                connection.commit()

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

    def get_martherial_by_id(self, id_matherial):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT id_matherial, matherial_id_matherial, stages_id_matherial, matherial_name, unit, amount, price, sum FROM matherial_purchased WHERE id_matherial = %s",
                (id_matherial,))
            rows = cursor.fetchall()
            history = [
                History(
                    id_history=row[0],
                    matherial_purchased_id_matherial=row[1],
                    payment_id_payment=row[2],
                    provider=row[3],
                    unit=row[4],
                    amount=row[5],
                    price=row[6],
                    sum=row[7],
                    time_buy=row[8]
                )
                for row in rows
            ]
        finally:
            cursor.close()
            connection.close()
        return history
    def delete_history(self, id_history):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM history WHERE id_history = %s", (id_history,))
        connection.commit()
        cursor.close()
        connection.close()
