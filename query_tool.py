from database import get_db_connection
from sql_guardrail import validate_sql


def execute_readonly_query(sql):
    """
    Execute a validated SELECT query
    using the read-only MySQL user.
    """

    # Step 1: Validate SQL
    is_safe, message = validate_sql(sql)

    if not is_safe:
        raise ValueError(f"❌ Query blocked: {message}")

    connection = None
    cursor = None

    try:
        # Step 2: Connect to MySQL
        connection = get_db_connection()

        # Step 3: Create cursor
        cursor = connection.cursor(dictionary=True)

        # Step 4: Execute SELECT query
        cursor.execute(sql)

        # Step 5: Get results
        results = cursor.fetchall()

        return results

    except Exception as error:
        raise RuntimeError(
            f"❌ Database query failed: {error}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()



if __name__ == "__main__":

    tests = [
        (
            "Safe SELECT",
            "SELECT product_name FROM products LIMIT 1",
            True,
        ),
        (
            "UPDATE blocked",
            "UPDATE products SET price = 0",
            False,
        ),
        (
            "DELETE blocked",
            "DELETE FROM products",
            False,
        ),
        (
            "Multiple statements blocked",
            "SELECT product_name FROM products; DELETE FROM products",
            False,
        ),
        (
            "File export blocked",
            "SELECT * FROM products INTO OUTFILE 'test.txt'",
            False,
        ),
    ]

    print("\n===== QUERY TOOL SECURITY TESTS =====\n")

    all_passed = True

    for name, sql, expected_success in tests:
        try:
            result = execute_readonly_query(sql)
            actual_success = True

            if expected_success:
                print(f"PASS | {name} | Query executed | Rows: {len(result)}")
            else:
                print(f"FAIL | {name} | Unsafe query was not blocked")
                all_passed = False

        except ValueError as error:
            actual_success = False
            if not expected_success:
                print(f"PASS | {name} | Blocked before database execution")
            else:
                print(f"FAIL | {name} | {error}")
                all_passed = False

        except Exception as error:
            actual_success = False
            print(f"FAIL | {name} | Unexpected error: {error}")
            all_passed = False

    print(
        "\nRESULT:",
        "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    )
