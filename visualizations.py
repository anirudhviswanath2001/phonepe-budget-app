import streamlit as st
from streamlit_echarts import st_echarts
from analysis import category_totals,category_by_month,monthly_totals,daily_totals,budget_analysis,monthly_incomes,monthly_cash_flow
import pandas as pd

def category_chart(df):
    data=category_totals(df).rename(columns={"Category":"name","Amount":"value"}).to_dict("records")
    options = {
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}<br/>₹{c} ({d}%)",
            "textStyle": {"fontSize": 16}
        },
        "legend": {
            "top": "1%",
            "left": "center",
            "width": "92%",
            "itemWidth": 18,
            "itemHeight": 18,
            "itemGap": 14,
            "textStyle": {"fontSize": 16}
        },
        "series": [
            {
                "name": "Category-wise Expenses",
                "type": "pie",
                "radius": ["38%", "68%"],
                "center": ["50%", "55%"],
                "avoidLabelOverlap": True,
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 20,
                        "fontWeight": "bold",
                        "formatter": "{b}\n{d}%"
                        }
                          },
                "labelLine": {"show": False},
                "data": data
                }
                ]
    }
    return st_echarts(options=options, height="800px")


def monthly_chart(df):
    monthly_data = monthly_totals(df)

    options = {
        "tooltip": {
            "trigger": "axis"
        },
        "title": {
            "text": "Monthly Spending Trend",
            "left": "center"
            },
        "xAxis": {
            "type": "category",
            "name": "Month",
            "nameLocation": "middle",
            "nameGap": 30,
            "data": monthly_data["Date"].astype(str).tolist()
            },
        "yAxis": {
            "type": "value",
            "name": "Expenses (₹)",
            "nameLocation": "middle",
            "nameGap": 55
            },
        "grid": {
            "left": "12%",
            "right": "5%",
            "bottom": "15%",
            "containLabel": True
            },
        "series":[
            {
                "name": "Monthly Expenses",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "data": monthly_data["Amount"].tolist()
            }
            ]
    }

    st_echarts(options=options, height="400px")

def category_month_chart(df,title="Monthly Spending by Category",y_axis_name="Expenses (₹)"):
    monthly_category_data = category_by_month(df)
    months = monthly_category_data.columns.astype(str).to_list()
    series = [
        {
            "name": category,
            "type": "bar",
            "stack": "total",
            "barWidth": "55%",
            "data": monthly_category_data.loc[category].round(2).to_list()
        }
        for category in monthly_category_data.index
    ]
    options = {
        "title": {
            "text": title,
            "left": "center",
            "top": "1%",
            "textStyle": {"fontSize": 20}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "textStyle": {"fontSize": 14}
        },
        "legend": {
            "top": "9%",
            "left": "center",
            "width": "94%",
            "itemWidth": 14,
            "itemHeight": 14,
            "itemGap": 10,
            "textStyle": {"fontSize": 13}
        },
        "grid": {
            "left": "8%",
            "right": "4%",
            "top": "30%",
            "bottom": "12%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "name": "Month",
            "nameLocation": "middle",
            "nameGap": 35,
            "nameTextStyle": {"fontSize": 14},
            "axisLabel": {"fontSize": 14},
            "data": months
        },
        "yAxis": {
            "type": "value",
            "name": y_axis_name,
            "nameLocation": "middle",
            "nameGap": 60,
            "nameTextStyle": {"fontSize": 14},
            "axisLabel": {"fontSize": 13}
        },
        "series": series
    }
    st_echarts(options=options, height="800px")

def daily_chart(df):
    daily_data = daily_totals(df)
    dates = daily_data["Date"].dt.strftime("%d %b").tolist()
    amounts = daily_data["Amount"].round(0).astype(int).tolist()

    options = {
        "title": {
            "text": "Daily Spending Trend",
            "left": "center",
            "top": "1%",
            "textStyle": {"fontSize": 20}
        },
        "tooltip": {
            "trigger": "axis",
            "textStyle": {"fontSize": 14}
        },
        "grid": {
            "left": "4%",
            "right": "6%",
            "top": "14%",
            "bottom": "20%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "axisLabel": {"fontSize": 12, "hideOverlap": True},
            "data": dates
        },
        "yAxis": {
            "type": "value",
            "name": "Expenses (₹)",
            "nameLocation": "middle",
            "nameGap": 55,
            "nameTextStyle": {"fontSize": 14},
            "axisLabel": {"fontSize": 12},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}
        },
        "dataZoom": [
            {"type": "inside"},
            {"type": "slider", "height": 20, "bottom": "2%"}
        ],
        "series": [
            {
                "name": "Daily Expenses",
                "type": "line",
                "smooth": False,
                "showSymbol": False,
                "lineStyle": {"width": 2.5, "color": "#5B8FF9"},
                "areaStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(91,143,249,0.40)"},
                            {"offset": 1, "color": "rgba(91,143,249,0.02)"}
                        ]
                    }
                },
                "markPoint": {
                    "data": [{"type": "max", "name": "Highest"}],
                    "symbolSize": 45,
                    "label": {"fontSize": 11}
                },
                "data": amounts
            }
        ]
    }

    st_echarts(options=options, height="450px")

def budget_chart(df, budget):
    budget_data = budget_analysis(df, budget)

    options = {
        "title": {
            "text": "Monthly Budget vs Actual Spending",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "top": "12%"
        },
        "xAxis": {
            "type": "category",
            "name": "Month",
            "data": budget_data["Month"].astype(str).tolist()
        },
        "yAxis": {
            "type": "value",
            "name": "Amount (₹)"
        },
        "series": [
            {
                "name": "Budget",
                "type": "bar",
                "data": budget_data["Budget"].tolist()
            },
            {
                "name": "Actual Spending",
                "type": "bar",
                "data": budget_data["Actual Spending"].tolist()
            }
        ]
    }

    st_echarts(options=options, height="400px")

def monthly_income_chart(df):
    monthly_data = monthly_incomes(df)
    months = monthly_data["Date"].astype(str).tolist()
    amounts = monthly_data["Amount"].round(0).astype(int).tolist()

    options = {
        "title": {
            "text": "Monthly Income Trend",
            "left": "center",
            "top": "1%",
            "textStyle": {"fontSize": 20}
        },
        "tooltip": {
            "trigger": "axis",
            "textStyle": {"fontSize": 14}
        },
        "grid": {
            "left": "4%",
            "right": "6%",
            "top": "18%",
            "bottom": "10%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "axisLabel": {"fontSize": 14},
            "data": months
        },
        "yAxis": {
            "type": "value",
            "name": "Income (₹)",
            "nameLocation": "middle",
            "nameGap": 60,
            "nameTextStyle": {"fontSize": 14},
            "axisLabel": {"fontSize": 13},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}
        },
        "series": [
            {
                "name": "Monthly Income",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 10,
                "lineStyle": {"width": 3, "color": "#2EC4B6"},
                "itemStyle": {"color": "#2EC4B6", "borderColor": "#FFFFFF", "borderWidth": 2},
                "areaStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(46,196,182,0.40)"},
                            {"offset": 1, "color": "rgba(46,196,182,0.02)"}
                        ]
                    }
                },
                "label": {"show": True, "position": "top", "fontSize": 12},
                "data": amounts
            }
        ]
    }

    st_echarts(options=options, height="450px")

def income_category_chart(df):
    data = category_totals(df).rename(columns={"Category": "name", "Amount": "value"}).to_dict("records")
    options = {
        "title": {
            "text": "Income by Category",
            "left": "center",
            "top": "1%",
            "textStyle": {"fontSize": 20}
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}<br/>₹{c} ({d}%)",
            "textStyle": {"fontSize": 14}
        },
        "legend": {
            "top": "9%",
            "left": "center",
            "width": "94%",
            "itemWidth": 14,
            "itemHeight": 14,
            "itemGap": 12,
            "textStyle": {"fontSize": 14}
        },
        "series": [
            {
                "name": "Category-wise Income",
                "type": "pie",
                "radius": ["35%", "65%"],
                "center": ["50%", "64%"],
                "avoidLabelOverlap": True,
                "itemStyle": {"borderRadius": 6, "borderColor": "transparent", "borderWidth": 2},
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 20,
                        "fontWeight": "bold",
                        "formatter": "{b}\n{d}%"
                    }
                },
                "labelLine": {"show": False},
                "data": data
            }
        ]
    }
    return st_echarts(options=options, height="600px")

def income_expense_chart(debit_df, credit_df):
    cash_flow = monthly_cash_flow(debit_df, credit_df)
    months = cash_flow["Date"].astype(str).tolist()
    income = cash_flow["Amount_Income"].round(0).astype(int).tolist()
    expense = cash_flow["Amount_Expense"].round(0).astype(int).tolist()

    options = {
        "title": {
            "text": "Monthly Income vs Expenses",
            "left": "center",
            "top": "1%",
            "textStyle": {"fontSize": 20}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "textStyle": {"fontSize": 14}
        },
        "legend": {
            "top": "9%",
            "left": "center",
            "itemWidth": 14,
            "itemHeight": 14,
            "itemGap": 20,
            "textStyle": {"fontSize": 14}
        },
        "grid": {
            "left": "4%",
            "right": "5%",
            "top": "22%",
            "bottom": "8%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "axisTick": {"show": False},
            "axisLabel": {"fontSize": 14},
            "data": months
        },
        "yAxis": {
            "type": "value",
            "name": "Amount (₹)",
            "nameLocation": "middle",
            "nameGap": 60,
            "nameTextStyle": {"fontSize": 14},
            "axisLabel": {"fontSize": 13},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}
        },
        "series": [
            {
                "name": "Income",
                "type": "bar",
                "barMaxWidth": 36,
                "itemStyle": {"color": "#2EC4B6", "borderRadius": [6, 6, 0, 0]},
                "label": {"show": True, "position": "top", "fontSize": 11},
                "data": income
            },
            {
                "name": "Expenses",
                "type": "bar",
                "barMaxWidth": 36,
                "itemStyle": {"color": "#FF7A59", "borderRadius": [6, 6, 0, 0]},
                "label": {"show": True, "position": "top", "fontSize": 11},
                "data": expense
            }
        ]
    }

    st_echarts(options=options, height="500px")


if __name__=="__main__":
    debit_df=pd.read_csv("categorized_debits.csv")
    credit_df = pd.read_csv("categorized_credits.csv")
    print(income_expense_chart(debit_df,credit_df))