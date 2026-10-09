
import re


BLOCKED_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "RENAME",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "CALL",
    "EXECUTE",
    "INTO",
    "OUTFILE",
    "DUMPFILE",
    "LOAD_FILE",
    "SLEEP",
    "BENCHMARK",
    "GET_LOCK",
    "RELEASE_LOCK",
]


def validate_sql(sql):
    """
    Apply conservative checks to AI-generated MySQL queries.
    Only simple, single SELECT statements are accepted.
    """

    if not isinstance(sql, str) or not sql.strip():
        return False, "SQL query is empty or invalid."

    cleaned_sql = sql.strip()

    # Reject markdown fences instead of silently modifying SQL.
    if "```" in cleaned_sql:
        return False, "Markdown code fences are not allowed."

    # Reject SQL comments to reduce hidden-payload risk.
    if re.search(r"--|#|/\*|\*/", cleaned_sql):
        return False, "SQL comments are not allowed."

    # Allow one optional semicolon at the end only.
    query_without_semicolon = cleaned_sql.rstrip().rstrip(";").strip()

    if ";" in query_without_semicolon:
        return False, "Multiple SQL statements are not allowed."

    # Only SELECT statements are accepted.
    if not re.match(r"(?is)^SELECT\b", query_without_semicolon):
        return False, "Only SELECT queries are allowed."

    # Reject blocked operations and risky functions.
    for keyword in BLOCKED_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, query_without_semicolon, re.IGNORECASE):
            return False, f"Blocked SQL keyword detected: {keyword}"

    # Reject locking reads.
    if re.search(
        r"\bFOR\s+UPDATE\b|\bLOCK\s+IN\s+SHARE\s+MODE\b",
        query_without_semicolon,
        re.IGNORECASE,
    ):
        return False, "Locking reads are not allowed."

    return True, "SQL query passed basic guardrail checks."


if __name__ == "__main__":

    test_queries = [
        (
            "Safe SELECT",
            "SELECT product_name FROM products;",
            True,
        ),
        (
            "UPDATE attack",
            "UPDATE products SET price = 0",
            False,
        ),
        (
            "DELETE attack",
            "DELETE FROM products",
            False,
        ),
        (
            "Multiple statements",
            "SELECT * FROM products; DELETE FROM products",
            False,
        ),
        (
            "File write attempt",
            "SELECT * FROM products INTO OUTFILE 'test.txt'",
            False,
        ),
        (
            "Risky function",
            "SELECT SLEEP(10)",
            False,
        ),
        (
            "Comment payload",
            "SELECT * FROM products -- hidden payload",
            False,
        ),
        (
            "Locking read",
            "SELECT * FROM products FOR UPDATE",
            False,
        ),
    ]

    print("\n===== SQL GUARDRAIL TESTS =====\n")

    all_passed = True

    for name, sql, expected in test_queries:
        is_safe, message = validate_sql(sql)
        passed = is_safe == expected

        print(
            f"{'PASS' if passed else 'FAIL'} | {name} "
            f"| {'ALLOWED' if is_safe else 'BLOCKED'} "
            f"| {message}"
        )

        if not passed:
            all_passed = False

    print(
        "\nRESULT:",
        "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    )
