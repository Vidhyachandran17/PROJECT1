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

def insert_agg_user(cursor, state, year, quarter, registered_users, app_opens):
    query = """
        INSERT INTO aggregated_user (state, year, quarter, registered_users, app_opens)
        VALUES (%s, %s, %s, %s, %s)
    """
    print(f"Inserting: {state}, {year}, {quarter}, {registered_users}, {app_opens}")
    cursor.execute(query, (state, year, quarter, registered_users, app_opens))

def process_files():
    base_path = r"C:\Users\Vidhya R\Desktop\project\project1\pulse\data\aggregated\user\country\india\state"
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

                # Extract quarter from filename, e.g. "4.json" => 4
                quarter = int(file.split('.')[0])
                file_path = os.path.join(year_path, file)

                with open(file_path, 'r') as f:
                    json_data = json.load(f)

                    # Defensive check
                    if not json_data.get("success", False):
                        print(f"Skipping {file_path} because success=False")
                        continue

                    data = json_data.get("data", {})
                    aggregated = data.get("aggregated", {})

                    registered_users = aggregated.get("registeredUsers", 0)
                    app_opens = aggregated.get("appOpens", 0)

                    insert_agg_user(cursor, state, int(year), quarter, registered_users, app_opens)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_files()
    
