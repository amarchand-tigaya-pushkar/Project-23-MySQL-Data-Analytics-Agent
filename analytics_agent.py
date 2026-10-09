from sql_generator import generate_sql
from query_tool import execute_readonly_query
from insight_generator import (
    generate_business_insight,
    validate_insight_numbers
)


def run_analytics_agent(user_question):
    """
    Complete MySQL Data Analytics Agent workflow.

    Flow:
    User Question
        ↓
    SQL Generation
        ↓
    SQL Safety Check
        ↓
    MySQL Query Tool
        ↓
    Query Result
        ↓
    Business Insight
        ↓
    Numeric Validation
        ↓
    Final Answer
    """

    print("\n🤖 Analytics Agent Started...")
    print(f"🧑 User Question: {user_question}")

    # STEP 1: Generate SQL
    print("\n🧠 Generating SQL...")

    sql = generate_sql(user_question)

    print("\n===== GENERATED SQL =====")
    print(sql)

    # STEP 2: Execute SQL
    print("\n🔐 Sending SQL to Read-Only MySQL Tool...")

    try:
        results = execute_readonly_query(sql)

    except Exception as error:
        print("\n❌ Database Error:")
        print(error)
        return None

    # STEP 3: Show database result
    print("\n===== DATABASE RESULT =====")

    if not results:
        print("No data found.")
        return None

    for row in results:
        print(row)

    # STEP 4: Generate business insight
    print("\n💡 Generating Business Insight...")

    try:
        insight = generate_business_insight(
            user_question,
            results
        )

    except Exception as error:
        print("\n❌ Insight Generation Error:")
        print(error)
        return None

    print("\n===== GENERATED INSIGHT =====")
    print(insight)

    # STEP 5: Validate numeric values
    print("\n🔎 Validating Numeric Accuracy...")

    valid, message = validate_insight_numbers(
        results,
        insight
    )

    if not valid:

        print("❌ Numeric Validation Failed!")
        print("Reason:", message)

        print("\n⚠️ AI-generated insight rejected.")

        return None

    print("✅ Numeric validation passed.")

    # STEP 6: Final answer
    print("\n========================================")
    print("        🎯 FINAL BUSINESS INSIGHT")
    print("========================================")

    print(insight)

    print("\n✅ Agent Workflow Completed!")

    return insight


if __name__ == "__main__":

    print("\n========================================")
    print("   🤖 MYSQL DATA ANALYTICS AGENT")
    print("========================================")

    question = input("\nAsk your business question: ")

    run_analytics_agent(question)