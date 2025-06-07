
import os
import json
import psycopg2

# STEP 1: Database connection
def connect_db():
    return psycopg2.connect(
        dbname="phonepe_pulse",
        user="postgres",       # ⬅️ Replace with your PostgreSQL username
        password="123456",   # ⬅️ Replace with your PostgreSQL password
        host="localhost",
        port="5432"
    )

# STEP 2: Insert function
def insert_data(cursor, state, year, quarter, txn_type, count, amount):
    query = """
        INSERT INTO aggregated_transaction (state, year, quarter, transaction_type, transaction_count, transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (state, year, quarter, txn_type, count, amount))

# STEP 3: Process JSON files
def process_files():
    base_path = "C:/Users/Vidhya R/Desktop/project/project1/pulse/data/aggregated/transaction/country/india/state"
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
                    data = json_data.get("data", {}).get("transactionData", [])

                    for entry in data:
                        txn_type = entry.get("name")
                        count = entry.get("paymentInstruments")[0]["count"]
                        amount = entry.get("paymentInstruments")[0]["amount"]

                        insert_data(cursor, state, int(year), quarter, txn_type, count, amount)

    conn.commit()
    cursor.close()
    conn.close()

# Run everything
process_files()