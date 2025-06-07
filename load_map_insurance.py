import os
import json
import psycopg2


def create_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",       # 🔁 Replace with your actual PostgreSQL username
        password="123456",   # 🔁 Replace with your actual password
        dbname="phonepe_pulse"      # 🔁 Replace with your actual DB name
    )


def insert_map_insurance(cursor, state, year, quarter, lat, lng, metric, label):
    cursor.execute(
        """
        INSERT INTO map_insurance (state, year, quarter, lat, lng, metric, label)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (state, year, quarter, lat, lng, metric, label)
    )


def process_files(base_path, cursor):
    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter_path = os.path.join(year_path, quarter_file)
                quarter = int(quarter_file.split(".")[0])

                try:
                    with open(quarter_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Navigate nested structure: data -> data -> columns, data
                    if not isinstance(data.get("data"), dict) or "data" not in data["data"]:
                        print(f"Skipping {quarter_path}: Nested 'data' key missing")
                        continue

                    inner_data = data["data"]["data"]
                    if "columns" not in inner_data or "data" not in inner_data:
                        print(f"Skipping {quarter_path}: 'columns' or 'data' missing in nested data")
                        continue

                    for row in inner_data["data"]:
                        try:
                            lat = float(row[0])
                            lng = float(row[1])
                            metric = float(row[2])
                            label = str(row[3])
                            insert_map_insurance(cursor, state, int(year), quarter, lat, lng, metric, label)
                        except Exception as e:
                            print(f"Skipping invalid entry in {state} {year} Q{quarter}: {e}")
                except Exception as e:
                    print(f"Error loading {quarter_path}: {e}")


def main():
    conn = create_connection()
    cursor = conn.cursor()
    base_path = "pulse/data/map/insurance/country/india/state"
    process_files(base_path, cursor)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data load complete.")


if __name__ == "__main__":
    main()
