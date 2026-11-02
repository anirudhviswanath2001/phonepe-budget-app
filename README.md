# PhonePe Expense Tracker & Budget Dashboard

A local Python-based expense tracking and budgeting application that converts PhonePe PDF statements into categorized financial insights using rule-based classification and a locally running LLM.

## Features

- **PDF Extraction:** Extract debit and credit transactions from password-protected PhonePe PDF statements.
- **Transaction Categorization:** Categorize transactions using predefined merchant keywords, with Ollama (Qwen3 4B) as a fallback for unmatched transactions.
- **Expense Analysis:** Calculate total expenses, category-wise spending, monthly spending, daily spending, and top transactions.
- **Income Analysis:** Track total income, monthly income, and income by category.
- **Budget Tracking:** Compare actual monthly expenses against a user-defined budget.
- **Cash Flow Analysis:** Compare monthly income and expenses and calculate net savings.
- **Interactive Dashboard:** Explore financial insights through Streamlit and Apache ECharts visualizations.

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas
- **PDF Extraction:** pdfplumber
- **Local LLM:** Ollama – Qwen3 4B
- **Dashboard:** Streamlit
- **Visualizations:** Apache ECharts (streamlit-echarts)

## Project Structure

```text
phonepe-budget-app/
├── app.py
├── pdf_to_csv.py
├── categorize.py
├── analysis.py
├── visualizations.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.10 or later
- Ollama installed
- Qwen3 4B model downloaded

Download the model:

```bash
ollama pull qwen3:4b
```

## Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
cd phonepe-budget-app
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start Ollama:

```bash
ollama serve
```

In another terminal, launch the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## How It Works

1. Upload your password-protected PhonePe PDF statement.
2. Enter the PDF password.
3. The application extracts debit and credit transactions into separate CSV files.
4. Transactions are categorized using keyword-based rules.
5. Unmatched transactions are sent to the locally running Qwen3 model through Ollama.
6. Pandas processes the categorized transactions to calculate financial metrics.
7. The Streamlit dashboard displays interactive charts and financial summaries.

## Privacy

- Transaction categorization runs locally through Ollama.
- Financial statements and generated CSV files are processed on the local machine.
- No cloud-based LLM API is required.
- Do not upload personal statements, generated transaction CSVs, passwords, or other sensitive financial information to GitHub.

## Future Improvements

- Custom category management
- Category-specific monthly budgets
- Transaction search and filtering
- Exportable monthly financial reports
