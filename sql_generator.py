from ollama import chat
from schema_tool import get_database_schema


def generate_sql(user_question):
    """
    Generate a safe and simple MySQL SELECT query
    using the local Ollama model.
    """

    schema = get_database_schema()

    schema_text = ""

    for table_name, columns in schema.items():
        schema_text += f"\nTABLE: {table_name}\n"

        for column in columns:
            schema_text += (
                f"- {column['name']} "
                f"({column['type']})\n"
            )

    prompt = f"""
You are a MySQL SQL generation assistant.

Database schema:
{schema_text}

Rules:
1. Generate ONLY SELECT queries.
2. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, TRUNCATE, CREATE, RENAME, REPLACE,
   GRANT, or REVOKE.
3. Use only tables and columns available in the schema.
4. Use valid MySQL syntax.
5. Return ONLY the SQL query.
6. Do not use markdown code fences.
7. Prefer SIMPLE SQL queries.
8. Avoid unnecessary subqueries and derived tables.
9. If you use a derived table, ALWAYS give it an alias.
10. Use JOIN when information comes from multiple tables.
11. Use GROUP BY for aggregation.
12. Use ORDER BY ... DESC LIMIT 1 for highest-value questions.
13. Do not invent columns or tables.
14. Do not calculate revenue incorrectly.
15. When the user asks for "quantity sold",
    "units sold", "number of units", or "total quantity",
    use SUM(s.quantity), NOT COUNT(s.sale_id).

16. COUNT(s.sale_id) means number of sales transactions,
    not number of units sold.

17. When the user asks for total revenue,
    use SUM(s.quantity * p.price).

18. When the user asks for highest revenue product,
    group by product and use SUM(s.quantity * p.price).

19. When the user asks for highest quantity product,
    group by product and use SUM(s.quantity).


20. When the user asks which city generated the highest
    revenue, join customers c, sales s, and products p.

    Correct SQL pattern:

    SELECT c.city,
           SUM(s.quantity * p.price) AS revenue
    FROM customers c
    JOIN sales s
        ON c.customer_id = s.customer_id
    JOIN products p
        ON s.product_id = p.product_id
    GROUP BY c.city
    ORDER BY revenue DESC
    LIMIT 1;

21. Never reference a table alias unless that alias is
    defined in the FROM or JOIN clauses.

22. For city revenue questions, return both city and revenue.


23. For total revenue questions, use this exact SQL pattern:

    SELECT SUM(s.quantity * p.price) AS total_revenue
    FROM sales s
    JOIN products p
        ON s.product_id = p.product_id;

24. Always use meaningful aliases for calculated columns.
    For total revenue, the alias must be total_revenue.


25. For a total revenue question, return only one column
    named total_revenue.

26. For a total revenue question, do not return any
    additional columns or duplicate calculations.

27. For highest-revenue product questions, return
    product_name and revenue.

28. For highest-quantity product questions, return
    product_name and quantity_sold.

29. For a top customer by revenue question, return
    customer_name and revenue.

Important business rule:
Revenue = quantity * product price.

For questions asking for the highest revenue product,
prefer this SQL pattern:

SELECT p.product_name,
       SUM(s.quantity * p.price) AS revenue
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 1;

User question:
{user_question}
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response["message"]["content"].strip()

    # Remove accidental markdown code fences
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


if __name__ == "__main__":

    question = input("\nAsk your business question: ")

    sql = generate_sql(question)

    print("\n===== GENERATED SQL =====\n")
    print(sql)