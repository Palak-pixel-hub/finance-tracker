import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Finance Tracker: Planned vs Actual")

# Upload CSV
uploaded_file = st.file_uploader("Upload your budget_data.csv", type=["csv"])

if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Calculate Difference
    df["Difference"] = df["Actual"] - df["Planned"]

    # Show Data
    st.subheader("📋 Budget Data")
    st.dataframe(df)

    # Summary
    total_planned = df["Planned"].sum()
    total_actual = df["Actual"].sum()
    total_diff = total_actual - total_planned

    st.subheader("📊 Summary")
    st.write(f"*Total Planned:* ₹{total_planned}")
    st.write(f"*Total Actual:* ₹{total_actual}")
    if total_diff > 0:
        st.warning(f"⚠ Overspent by ₹{total_diff}")
    else:
        st.success(f"✅ Saved ₹{-total_diff}")

    # Save to Excel (in memory)
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    st.download_button("📥 Download Excel Report", output.getvalue(), file_name="budget_report.xlsx")

    # Bar Chart
    st.subheader("📈 Spending Chart")
    fig, ax = plt.subplots(figsize=(8, 4))
    bar_width = 0.35
    index = range(len(df))

    ax.bar(index, df["Planned"], bar_width, label="Planned", color="skyblue")
    ax.bar([i + bar_width for i in index], df["Actual"], bar_width, label="Actual", color="salmon")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(df["Category"])
    ax.set_ylabel("Amount")
    ax.set_title("Planned vs Actual Spending")
    ax.legend()
    st.pyplot(fig)