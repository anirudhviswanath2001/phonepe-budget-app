import pandas as pd
from analysis import total_expenses,category_totals,monthly_totals,category_by_month,daily_totals,top_spends,net_savings,monthly_incomes,monthly_cash_flow,total_incomes,budget_analysis

def test_total_expenses():
    df=pd.DataFrame({"Amount":[100,200,200,500]})
    result=total_expenses(df)
    assert result==1000

def test_category_totals():
    df=pd.DataFrame({"Category":["Food and Dining","Groceries","Fuel","Groceries","Fuel"],"Amount":[200,500,100,50,20]})
    result=category_totals(df)
    assert result.loc[result["Category"]=="Groceries","Amount"].iloc[0]==550

def test_monthly_totals():
    df=pd.DataFrame({"Date":["2025-05-10","2025-05-20","2025-06-18","2025-06-18"],"Amount":[200,300,500,500]})
    result=monthly_totals(df)
    assert result.loc[result["Date"]=="2025-05","Amount"].iloc[0]==500
    assert result.loc[result["Date"]=="2025-06","Amount"].iloc[0]==1000

def test_category_month_totals():
    df=pd.DataFrame({"Date":["2025-05-10","2025-05-20","2025-06-18","2025-06-18"],"Amount":[200,300,500,500],"Category":["Food and Dining","Groceries","Fuel","Groceries"]})
    result=category_by_month(df)
    assert result.loc["Groceries", pd.Period("2025-05", freq="M")] == 300
    assert result.loc["Groceries", pd.Period("2025-06", freq="M")] == 500
    assert result.loc["Fuel", pd.Period("2025-06", freq="M")] == 500

def test_daily_totals():
    df=pd.DataFrame({"Date":["2025-05-10","2025-05-10","2025-06-20","2025-06-20","2025-07-10"],"Amount":[200,300,500,500,500]})
    result=daily_totals(df)
    assert result.loc[result["Date"]=="2025-05-10","Amount"].iloc[0]==500
    assert result.loc[result["Date"]=="2025-06-20","Amount"].iloc[0]==1000
    assert result.loc[result["Date"]=="2025-07-10","Amount"].iloc[0]==500

def test_top_spends():
    df=pd.DataFrame({"Amount":[200,300,500,500],"Category":["Food and Dining","Groceries","Fuel","Groceries"]})
    result=top_spends(df,1)
    assert result["Amount"].iloc[0] == 500

def test_net_savings():
    expenses = pd.DataFrame({"Amount": [200, 300, 100]})
    income = pd.DataFrame({"Amount": [1000, 500]})
    result = net_savings(expenses, income)
    assert result == 900

def test_monthly_incomes():
    df = pd.DataFrame({"Date": ["2025-05-10", "2025-05-20", "2025-06-18", "2025-06-18"],"Amount": [200, 300, 500, 500]})
    result = monthly_incomes(df)
    assert result.loc[result["Date"] == "2025-05", "Amount"].iloc[0] == 500
    assert result.loc[result["Date"] == "2025-06", "Amount"].iloc[0] == 1000

def test_monthly_cash_flow():
    expenses = pd.DataFrame({"Date": ["2025-05-10", "2025-05-20", "2025-06-18"],"Amount": [200, 300, 500]})
    income = pd.DataFrame({"Date": ["2025-05-15", "2025-06-20", "2025-06-25"],"Amount": [1000, 1500, 500]})
    result = monthly_cash_flow(expenses, income)
    assert result.loc[result["Date"] == "2025-05", "Amount_Expense"].iloc[0] == 500
    assert result.loc[result["Date"] == "2025-05", "Amount_Income"].iloc[0] == 1000
    assert result.loc[result["Date"] == "2025-05", "Savings"].iloc[0] == 500    

def test_total_incomes():
    df = pd.DataFrame({"Amount": [1000, 500, 200]})
    result = total_incomes(df)
    assert result == 1700

def test_budget_analysis():
    df = pd.DataFrame({"Date": ["2025-05-10", "2025-05-20", "2025-06-18"],"Amount": [200, 300, 500]})

    result = budget_analysis(df, 600)

    assert result.loc[result["Month"] == pd.Period("2025-05", freq="M"), "Actual Spending"].iloc[0] == 500
    assert result.loc[result["Month"] == pd.Period("2025-05", freq="M"), "difference"].iloc[0] == 100
    assert result.loc[result["Month"] == pd.Period("2025-05", freq="M"), "status"].iloc[0] == "within budget"
    assert result.loc[result["Month"] == pd.Period("2025-06", freq="M"), "status"].iloc[0] == "within budget"