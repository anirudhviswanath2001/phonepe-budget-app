from pdf_to_csv import convert_pdf_to_csv
from categorize import categorization
from analysis import top_spends,total_expenses,total_incomes,net_savings
from visualizations import category_chart,monthly_chart,category_month_chart,daily_chart,budget_chart,monthly_income_chart,income_category_chart,income_expense_chart
import streamlit as st
import pandas as pd

st.title("Transaction Lookup")
file=st.file_uploader("Upload your statement",type=["pdf"])
password=st.text_input("Enter your password",type="password")
if st.button("Process"):
    st.session_state.pop("category1", None)
    st.session_state.pop("category2", None)
    with st.spinner("Loading ..."):
        if file and password:
            try:
                debits,credits=convert_pdf_to_csv(file,password=password)
                category1,category2=categorization(debits,credits)
                if category1.empty and category2.empty:
                     st.error("No transactions were categorized.")
                else:
                    st.session_state["category1"] = category1
                    st.session_state["category2"] = category2
                    st.success(f"Processed {len(category1)} debit and {len(category2)} credit transactions!")
            except Exception as e:
                st.error(str(e))
        else:
            st.error("PDF or password is missing ")


if "category1" in st.session_state or "category2" in st.session_state:
    debit_df = st.session_state.get("category1", pd.DataFrame())
    credit_df = st.session_state.get("category2", pd.DataFrame())

    options = ["Categorized Transactions"]

    if not debit_df.empty:
        options.extend([
        "Total Expenses",
        "Top Spends",
        "Category-wise Expenses",
        "Monthly Spending",
        "Category-wise Monthly Spending",
        "Daily Spending",
        "Budget Analysis"
        ])

    if not credit_df.empty:
        options.extend([
        "Total Incomes",
        "Monthly Income",
        "Income by Category",
        "Category-wise Monthly Income"
        ])

    if not debit_df.empty and not credit_df.empty:
        options.extend([
            "Total Savings",
            "Income and Expense Comparison"
        ])

    selection = st.selectbox("Select an option", options=options)
    
    if selection == "Categorized Transactions":
        if not debit_df.empty:
            st.subheader("Debit Transactions")
            st.dataframe(debit_df)

        if not credit_df.empty:
            st.subheader("Credit Transactions")
            st.dataframe(credit_df)

    elif selection=="Total Expenses":
        st.metric("Total Expenses", f"₹{total_expenses(debit_df):,.2f}")

    elif selection=="Total Incomes":
        st.metric("Total Incomes",f"₹{total_incomes(credit_df):,.2f}")

    elif selection=="Total Savings":
        st.metric("Total Savings",f"₹{net_savings(debit_df,credit_df):,.2f}")

    elif selection=="Top Spends":
        n=st.number_input("Number of Top spends",min_value=1,max_value=20,value=5,step=1)
        top_data = top_spends(debit_df, int(n))
        st.dataframe(top_data)

    elif selection=="Category-wise Expenses":
        category_chart(debit_df)

    elif selection=="Monthly Spending":
        monthly_chart(debit_df)

    elif selection=="Monthly Income":
        monthly_income_chart(credit_df)

    elif selection == "Income by Category":
        income_category_chart(credit_df)

    elif selection=="Category-wise Monthly Spending":
        category_month_chart(debit_df)

    elif selection == "Category-wise Monthly Income":
        category_month_chart(credit_df,"Monthly Income by Category","Income (₹)")

    elif selection=="Daily Spending":
        daily_chart(debit_df)

    elif selection == "Income and Expense Comparison":
        income_expense_chart(debit_df, credit_df)

    elif selection == "Budget Analysis":
        budget=st.number_input("Enter the Budget",min_value=1.0)
        budget_chart(debit_df,budget)
        


