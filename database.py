import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )

    return connection


if __name__ == "__main__":
    try:
        connection = get_db_connection()

        if connection.is_connected():
            print("✅ MySQL connection successful!")

            print("Database:", connection.database)
            print("User:", connection.user)

        connection.close()
        print("✅ MySQL connection closed.")

    except mysql.connector.Error as error:
        print("❌ MySQL connection failed!")
        print("Error:", error)