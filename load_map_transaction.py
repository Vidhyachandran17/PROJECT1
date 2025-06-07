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

def insert_data(cursor, state, year, quarter, district, count, amount):
    query = """
        INSERT INTO map_transaction (state, year, quarter, district, transaction_count, transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (state, year, quarter, district, count, amount))

def process_files():
    base_path = "C:/Users/Vidhya R/Desktop/project/project1/pulse/data/map/transaction/hover/country/india/state"
    conn = connect_db()
    cursor = conn.cursor()

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                quarter = int(file.strip("quarter.json"))
                file_path = os.path.join(year_path, file)

                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    data = json_data.get("data", {}).get("hoverDataList", [])

                    for entry in data:
                        district = entry.get("name")
                        count = entry.get("metric")[0]["count"]
                        amount = entry.get("metric")[0]["amount"]

                        insert_data(cursor, state, int(year), quarter, district, count, amount)

    conn.commit()
    cursor.close()
    conn.close()

process_files()
