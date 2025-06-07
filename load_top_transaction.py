import os
import json
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="phonepe_pulse",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )

def insert_data(cursor, state, year, quarter, name, count, amount):
    query = """
        INSERT INTO top_transaction (state, year, quarter, name, transaction_count, transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (state, year, quarter, name, count, amount))

def process_files():
    base_path = "C:/Users/Vidhya R/Desktop/project/project1/pulse/data/top/transaction/country/india/state"
    conn = connect_db()
    cursor = conn.cursor()

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                quarter = int(file.replace("quarter", "").replace(".json", ""))
                file_path = os.path.join(year_path, file)

                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    districts = json_data.get("data", {}).get("districts", [])

                    for entry in districts:
                        name = entry.get("entityName")
                        metric = entry.get("metric", {})
                        count = metric.get("count")
                        amount = metric.get("amount")

                        if name and count is not None and amount is not None:
                            insert_data(cursor, state, int(year), quarter, name, count, amount)

    conn.commit()
    cursor.close()
    conn.close()

process_files()
