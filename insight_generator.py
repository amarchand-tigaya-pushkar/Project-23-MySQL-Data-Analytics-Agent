
from decimal import Decimal


def format_value(value, is_money=False):
    """Format numbers using Indian digit grouping."""

    number = Decimal(str(value))
    fixed = f"{number:.2f}" if number % 1 else f"{number:.0f}"

    whole, dot, fraction = fixed.partition(".")
    sign = ""

    if whole.startswith("-"):
        sign = "-"
        whole = whole[1:]

    if len(whole) > 3:
        last_three = whole[-3:]
        remaining = whole[:-3]
        groups = []

        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        whole = ",".join(groups + [last_three])

    formatted = sign + whole

    if dot:
        formatted += "." + fraction

    return f"₹{formatted}" if is_money else formatted



def generate_business_insight(user_question, query_result):
    """Format one-row and multi-row analytics results."""

    if not query_result:
        return "No data found."

    fields_list = [
        {str(key).lower(): value for key, value in row.items()}
        for row in query_result
    ]

    name_candidates = (
        "customer_name",
        "product_name",
        "city",
        "name"
    )

    metric_candidates = (
        "total_revenue",
        "revenue",
        "quantity_sold",
        "highest_quantity",
        "total_quantity",
        "count"
    )

    first_fields = fields_list[0]

    name_key = next(
        (key for key in name_candidates if key in first_fields),
        None
    )

    metric_key = next(
        (key for key in metric_candidates if key in first_fields),
        None
    )

    answer_lines = []

    for index, fields in enumerate(fields_list, start=1):
        if name_key and metric_key:
            value = fields[metric_key]
            is_money = "revenue" in metric_key

            formatted_value = (
                format_value(value, is_money)
                if value is not None
                else "N/A"
            )

            answer_lines.append(
                f"{index}. {fields[name_key]}: {formatted_value}"
            )

        else:
            row_parts = []

            for key, value in fields.items():
                if value is None:
                    formatted = "N/A"
                elif isinstance(value, (int, float, Decimal)):
                    formatted = format_value(
                        value,
                        is_money=("revenue" in key)
                    )
                else:
                    formatted = str(value)

                row_parts.append(f"{key}: {formatted}")

            answer_lines.append(
                f"{index}. " + " | ".join(row_parts)
            )

    if len(fields_list) > 1:
        observation = (
            f"The query returned {len(fields_list)} results, "
            "ordered according to the requested SQL ranking."
        )
    elif name_key and metric_key:
        metric_name = (
            "revenue"
            if "revenue" in metric_key
            else "quantity sold"
            if "quantity" in metric_key
            else "reported value"
        )

        observation = (
            f"{first_fields[name_key]} has the highest "
            f"{metric_name} in this query result."
        )
    else:
        observation = "This answer reflects the available database result."

    return (
        "Answer:\n"
        + "\n".join(answer_lines)
        + "\n\nData Insight:\n"
        + observation
    )



def validate_insight_numbers(query_result, insight):
    """Check that numeric database values appear in the answer."""

    if not isinstance(insight, str) or not insight.strip():
        return False, "Insight is empty or invalid."

    normalized_insight = (
        insight.replace(",", "")
        .replace("₹", "")
        .replace(" ", "")
    )

    for row in query_result:
        for value in row.values():
            if value is None:
                continue

            if isinstance(value, (int, float, Decimal)):
                integer_part = str(value).split(".")[0]

                if integer_part not in normalized_insight:
                    return False, (
                        f"Numeric value {value} "
                        "was not preserved in the answer."
                    )

    return True, "Numeric validation passed."


if __name__ == "__main__":
    question = "What is the total revenue?"

    result = [
        {
            "total_revenue": Decimal("530000.00")
        }
    ]

    insight = generate_business_insight(question, result)

    print("\n===== CLEAN BUSINESS INSIGHT =====\n")
    print(insight)

    valid, message = validate_insight_numbers(result, insight)

    print("\n===== NUMERIC VALIDATION =====\n")
    print("✅" if valid else "❌", message)

    print("\n===== CURRENCY FORMAT CHECKS =====")
    print(format_value(190000, True))
    print(format_value(260000, True))
    print(format_value(530000, True))
