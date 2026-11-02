import pandas as pd
import ollama
import re

DEBIT_RULES = {
    "Food & Dining": ["swiggy", "zomato", "mcdonald", "kfc", "dominos", "bhandar", "cafe", "restaurant", "tiffin", "chaat", "food", "pizza", "bakery", "subway", "burger king", "chai", "coffee", "dine"],
    "Groceries": ["dmart", "instamart", "blinkit", "ratnadeep", "bigbasket", "zepto", "supermarket", "kirana", "reliance fresh", "more retail", "organic store"],
    "Transportation": ["uber", "rapido", "irctc", "metro", "ola", "redbus", "abhibus", "bus", "railway", "parking", "toll"],
    "Fuel": ["indian oil", "bharat petroleum", "hp petrol", "petrol", "iocl", "bpcl", "hpcl", "fuel", "shell", "nayara"],
    "Shopping": ["amazon", "flipkart", "myntra", "westside", "h&m", "zudio", "reliance trends", "ajio", "meesho", "nykaa", "decathlon", "ikea", "lifestyle", "pantaloons", "shoppers stop"],
    "Subscriptions": ["netflix", "spotify", "hotstar", "google play", "google one", "youtube", "prime video", "apple.com/bill", "icloud", "canva", "adobe", "microsoft 365"],
    "Bills & Utilities": ["airtel", "jio", "electricity", "recharge", "act fibernet", "fibernet", "broadband", "water bill", "gas bill", "bescom", "tsspdcl", "tsnpdcl", "internet bill", "postpaid"],
    "Healthcare & Pharmacy": ["apollo", "pharmacy", "medplus", "clinic", "hospital", "medical", "diagnostic", "1mg", "pharmeasy", "netmeds", "practo", "lab test", "pathology", "dental", "optical"],
    "Entertainment": ["bookmyshow", "pvr", "inox", "cinepolis", "paytm movies", "gaming", "steam", "playstation", "xbox"],
    "Education": ["udemy", "coursera", "unacademy", "byju", "upgrad", "college", "university", "tuition"],
    "Personal Care": ["salon", "barber", "spa", "parlour", "urban company", "haircut", "grooming"],
    "Travel": ["makemytrip", "goibibo", "air india", "indigo", "vistara", "akasa", "hotel booking", "oyo", "airbnb"],
    "Household Expenses": ["furniture", "hardware", "plumber", "electrician"],
    "Insurance": ["lic", "insurance", "policybazaar", "hdfc life", "star health"],
    "Investments": ["zerodha", "groww", "upstox", "mutual fund"],
    "Loan & EMI Payments": ["emi", "loan", "bajaj finance"],
    "ATM & Cash Withdrawals": ["atm", "cash withdrawal"],
}

CREDIT_RULES = {
    "Salary & Income": ["salary", "payroll", "wages", "income", "freelance", "consulting", "professional fees", "employer", "stipend"],
    "Received from Person": ["received from", "money received", "upi received", "paid by", "transfer from", "credited by"],
    "Refunds": ["refund", "reversal", "reversed", "amazon refund", "flipkart refund", "merchant refund", "cash refund"],
    "Cashback & Rewards": ["cashback", "cash back", "reward", "rewards", "phonepe cashback", "scratch card", "cashback offer"],
    "Interest Income": ["interest", "savings interest", "fd interest", "fixed deposit interest", "rd interest"],
    "Investment Returns": ["dividend", "mutual fund redemption", "redemption", "investment maturity", "stock dividend", "capital gains"],
    "Loan Received": ["loan disbursement", "loan credited", "personal loan", "loan amount", "loan credit"],
    "Bank Transfers": ["self transfer", "own account transfer", "account transfer", "neft", "imps", "rtgs", "fund transfer"],
    "Other Credits": []
}

def rule_category(text,rules: dict):
    t=str(text).lower()
    for cat,keywords in rules.items():
        for k in keywords:
            if len(k)<=4:
                if re.search(rf"\b{re.escape(k)}\b",t):
                    return cat
            elif k in t:
                return cat
    return None

debit_prompt="""
                    You are a transaction categorization assistant.
 
                    Identify the most likely category based on the transaction description.
 
                    Choose exactly ONE category from:
 
                    Food & Dining
                    Groceries
                    Shopping
                    Transportation
                    Fuel
                    Bills & Utilities
                    Healthcare & Pharmacy
                    Entertainment
                    Travel
                    Education
                    Personal Care
                    Household Expenses
                    Subscriptions
                    Insurance
                    Investments
                    Loan & EMI Payments
                    Bank Transfers
                    Sent to Person
                    Received from Person
                    ATM & Cash Withdrawals
                    Other
 
                    Examples:
 
                    Input: Paid to McDonald's Hyderabad
                    Output: Food & Dining
 
                    Input: Paid to Swiggy
                    Output: Food & Dining
 
                    Input: Paid to DMart
                    Output: Groceries
 
                    Input: Paid to Amazon
                    Output: Shopping
 
                    Input: Paid to Uber India
                    Output: Transportation
 
                    Input: Paid to Indian Oil
                    Output: Fuel
 
                    Input: Paid electricity bill
                    Output: Bills & Utilities
 
                    Input: Paid to Apollo Pharmacy
                    Output: Healthcare & Pharmacy
 
                    Input: Paid Netflix subscription
                    Output: Subscriptions
 
                    Input: Paid to Rahul
                    Output: Sent to Person
 
                    Input: Received from Rahul
                    Output: Received from Person
 
                    Input: Transferred to bank account
                    Output: Bank Transfers
 
                    Rules:
                    - Return ONLY the category name.
                    - Return exactly ONE category.
                    - Do not provide explanations.
                    - Do not invent merchant information.
                    - If the transaction is unclear, return Other.
"""

credit_prompt="""
                    You are a transaction categorization assistant.
                    Identify the most likely credit transaction category.

                    Choose exactly ONE category from:

                    Salary & Income
                    Received from Person
                    Refunds
                    Cashback & Rewards
                    Interest Income
                    Investment Returns
                    Loan Received
                    Bank Transfers
                    Other Credits

                    Rules:
                    - Return ONLY the category name.
                    - Return exactly ONE category.
                    - Do not provide explanations.
                    - If unclear, return Other Credits.
                    """

def model_category(text,prompt: str):
    try:
        response = ollama.chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "system",
                    "content":prompt
                },
                {
                    "role": "user",
                    "content": f"Input: {text}\nOutput:"
                }
            ],
            options={"temperature": 0, "seed": 42},
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Model error for '{text}': {e}")
        raise


def category(text,prompt,rules):
    rule_result=rule_category(text,rules)
    if rule_result:
        print(f"RULE  : {text} -> {rule_result}")
        return rule_result
    result=model_category(text,prompt)
    print(f"Model: {text} -> {result}")
    return result

def categorization(file1, file2):
    df_debit = pd.read_csv(file1)
    df_credit = pd.read_csv(file2)
    if df_debit.empty and df_credit.empty:
        raise ValueError("No transactions found in either CSV file.")
    for df, rules, prompt, output_file in [(df_debit, DEBIT_RULES, debit_prompt, "categorized_debits.csv"),(df_credit, CREDIT_RULES, credit_prompt, "categorized_credits.csv")]:
        if df.empty:
            df["Category"] = pd.Series(dtype="object")
            df.to_csv(output_file, index=False)
            continue

        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        
        df["Date"] = pd.to_datetime(
            df["Date"], format="%b %d, %Y", errors="coerce"
        )

        mapping = {
            text: category(text,prompt,rules)
            for text in df["Transaction Details"].dropna().unique()
        }

        df["Category"] = df["Transaction Details"].map(mapping)
        df.to_csv(output_file, index=False)

    return df_debit, df_credit


if __name__ == "__main__":
    debit_df, credit_df = categorization("debits.csv", "credits.csv")

    print(debit_df["Category"].unique())
    print(credit_df["Category"].unique())