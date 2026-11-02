import pandas as pd

def category_totals(df: pd.DataFrame):
    category_total=df.groupby("Category")["Amount"].sum().reset_index()
    return category_total

def monthly_totals(df: pd.DataFrame):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly_total=df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    return monthly_total

def category_by_month(df: pd.DataFrame):
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"], errors="coerce")
    df_copy["month"]=df_copy["Date"].dt.to_period("M")
    category_by_month_total=pd.pivot_table(df_copy,values="Amount",index="Category",columns="month",aggfunc="sum").fillna(0)
    return category_by_month_total

def top_spends(df: pd.DataFrame,n: int):
    top_spend_list=df.sort_values("Amount",ascending=False).head(n)
    return top_spend_list

def total_expenses(df: pd.DataFrame):
    total=df["Amount"].sum()
    return total

def daily_totals(df: pd.DataFrame):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    daily_total=df.groupby("Date")["Amount"].sum().reset_index()
    return daily_total

def budget_analysis(df: pd.DataFrame, budget: float):
    monthly_spending = monthly_totals(df)

    budget_status = pd.DataFrame({
        "Month": monthly_spending["Date"],
        "Budget": budget,
        "Actual Spending": monthly_spending["Amount"]
    })

    budget_status["difference"] = (
        budget_status["Budget"] - budget_status["Actual Spending"]
    )

    budget_status["status"] = budget_status["difference"].apply(
        lambda x: "within budget" if x >= 0 else "Exceeded"
    )

    return budget_status

def total_incomes(df: pd.DataFrame):
    income_total=df["Amount"].sum()
    return income_total

def monthly_incomes(df: pd.DataFrame):
    df=df.copy()
    df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
    monthly_income=df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    return monthly_income

def monthly_cash_flow(df1: pd.DataFrame,df2: pd.DataFrame):
    df_expense,df_income=monthly_totals(df1.copy()),monthly_incomes(df2.copy())
    df_merged=pd.merge(df_expense,df_income,on='Date',how='outer',suffixes=("_Expense","_Income")).fillna(0)
    df_merged["Savings"]=(df_merged["Amount_Income"]-df_merged["Amount_Expense"])
    return df_merged

def net_savings(df1: pd.DataFrame,df2: pd.DataFrame):
    Total_Expenses=total_expenses(df1)
    Total_Income=total_incomes(df2)
    return Total_Income-Total_Expenses
    

if __name__ == "__main__":
    debit_df = pd.read_csv("categorized_debits.csv")
    credit_df = pd.read_csv("categorized_credits.csv")
    print(total_incomes(credit_df))
    print(monthly_incomes(credit_df))
    print(monthly_cash_flow(debit_df, credit_df))
    print("Net Savings:", net_savings(debit_df, credit_df))