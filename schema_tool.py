from database import get_db_connection


def get_database_schema():
    connection = get_db_connection()
    cursor = connection.cursor()

    schema = {}

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()

        schema[table_name] = []

        for column in columns:
            schema[table_name].append({
                "name": column[0],
                "type": column[1],
                "nullable": column[2],
                "key": column[3],
                "default": column[4],
                "extra": column[5],
            })

    cursor.close()
    connection.close()

    return schema


if __name__ == "__main__":
    schema = get_database_schema()

    print("\n===== DATABASE SCHEMA =====\n")

    for table_name, columns in schema.items():
        print(f"TABLE: {table_name}")

        for column in columns:
            print(
                f"  - {column['name']} "
                f"({column['type']}) "
                f"[Key: {column['key']}]"
            )

        print()