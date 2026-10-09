
import streamlit as st
import pandas as pd
import html

from sql_generator import generate_sql
from query_tool import execute_readonly_query
from insight_generator import (
    generate_business_insight,
    validate_insight_numbers,
)

st.set_page_config(
    page_title="Moto AI | Data Analytics",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #111c32);
    color: #f1f5f9;
}
[data-testid="stSidebar"] {
    background: #101a2c;
}
.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}
.hero {
    padding: 26px;
    border: 1px solid #263852;
    border-radius: 18px;
    background: linear-gradient(120deg, #172943, #142033);
    margin-bottom: 22px;
}
.hero h1 { color: #f8fafc; margin-bottom: 8px; }
.hero p { color: #a9bbd3; margin-bottom: 0; }
.kpi {
    background: #17243a;
    border: 1px solid #2a3c56;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
}
.kpi-label { color: #a9bbd3; font-size: 14px; }
.kpi-value {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 700;
    margin-top: 12px;
    overflow-wrap: anywhere;
}
div.stButton > button[kind="primary"] {
    background: #4778ff;
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


def format_indian_number(value):
    """Format numbers using Indian comma grouping."""
    try:
        number = float(value)
        integer = int(round(number))
        sign = "-" if integer < 0 else ""
        digits = str(abs(integer))

        if len(digits) <= 3:
            return sign + digits

        last_three = digits[-3:]
        remaining = digits[:-3]
        groups = []

        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        return sign + ",".join(groups + [last_three])
    except (ValueError, TypeError):
        return str(value)


def is_revenue_column(column):
    name = column.lower()
    return any(word in name for word in (
        "revenue", "sales", "amount", "total", "price"
    ))


def format_metric(value, column):
    """Format a KPI value before rendering the HTML card."""
    if pd.api.types.is_number(value):
        formatted = format_indian_number(value)
        if is_revenue_column(column):
            return f"₹{formatted}"
        return formatted

    return str(value)


with st.sidebar:
    st.title("⚙️ Workspace")
    st.markdown("**Moto AI Analytics Agent**")
    st.caption("Natural-language business analytics")
    st.divider()
    st.markdown("🔐 SQL validation enabled")
    st.markdown("🛡️ Read-only database access")
    st.markdown("🧠 Local Ollama model")
    st.divider()
    st.caption("Built by AMARCHAND TIGAYA PUSHKAR")


st.markdown("""
<div class="hero">
  <h1>📊 MySQL Data Analytics Agent</h1>
  <p>AI-powered business intelligence · MySQL · Ollama · Llama 3.2</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Ask your business question")

examples = [
    "What is the total revenue?",
    "Which product generated the highest revenue?",
    "Who is the top customer by revenue?",
    "Which city generated the highest revenue?",
    "Which product sold the highest quantity?",
    "Show the top five customers by revenue.",
]

selected_example = st.selectbox(
    "Choose an example question",
    ["Select an example..."] + examples,
)

question_input = st.text_input(
    "Or enter your own question",
    placeholder="e.g. What is the total revenue?",
)

question = question_input.strip()

if not question and selected_example != "Select an example...":
    question = selected_example

if st.button("🚀 Analyze Business Data", type="primary"):
    if not question:
        st.warning("Enter a business question or choose an example.")
    else:
        try:
            with st.spinner("🧠 Generating SQL with Ollama..."):
                sql = generate_sql(question)

            with st.expander("🔍 View generated SQL", expanded=True):
                st.code(sql, language="sql")

            with st.spinner("🔐 Validating and querying MySQL..."):
                results = execute_readonly_query(sql)

            if not results:
                st.info("No data found for this question.")
            else:
                df = pd.DataFrame(results)

                st.subheader("📈 Query Results")

                # KPI cards: format the original Decimal/numeric value
                # before putting it into the HTML.
                if len(df) == 1:
                    row = df.iloc[0]
                    columns_to_show = list(df.columns[:3])
                    metric_columns = st.columns(len(columns_to_show))

                    for index, column in enumerate(columns_to_show):
                        value = row[column]
                        display_value = html.escape(
                            format_metric(value, column)
                        )
                        label = html.escape(
                            str(column).replace("_", " ").title()
                        )

                        with metric_columns[index]:
                            st.markdown(
                                f'<div class="kpi">'
                                f'<div class="kpi-label">{label}</div>'
                                f'<div class="kpi-value">{display_value}</div>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

                # Result table
                display_df = df.copy()

                for column in display_df.columns:
                    if is_revenue_column(column):
                        display_df[column] = display_df[column].map(
                            lambda value: (
                                "₹" + format_indian_number(value)
                                if pd.api.types.is_number(value)
                                else str(value)
                            )
                        )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                )

                # Business insight and numeric validation
                st.subheader("💡 Business Insight")

                insight = generate_business_insight(question, results)
                valid, message = validate_insight_numbers(results, insight)

                if valid:
                    st.success("✅ Numeric validation passed")
                    st.markdown(insight)
                else:
                    st.error(f"Insight rejected: {message}")

                # Charts for multi-row results
                numeric_columns = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                if len(df) > 1 and numeric_columns:
                    st.subheader("📊 Data Visualization")

                    label_column = st.selectbox(
                        "Category",
                        df.columns.tolist(),
                    )
                    value_column = st.selectbox(
                        "Numeric metric",
                        numeric_columns,
                    )

                    chart_df = df[[label_column, value_column]].copy()
                    chart_df[value_column] = pd.to_numeric(
                        chart_df[value_column],
                        errors="coerce",
                    )
                    chart_df = chart_df.dropna().set_index(label_column)

                    if not chart_df.empty:
                        st.bar_chart(chart_df)

        except Exception:
            st.error(
                "Analysis failed. Check MySQL, Ollama, and SQL validation."
            )
            with st.expander("Technical error details"):
                import traceback
                st.code(traceback.format_exc())

st.divider()
st.caption("MySQL Data Analytics Agent · Local AI · Read-only analytics")
