import pdfplumber
import re
import csv
def convert_pdf_to_csv(pdf_file,password):
    with pdfplumber.open(pdf_file,password=password) as pdf:
        debits=[]
        credits=[]
        transactions=[]
        current_transaction=[]
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines=text.splitlines()
                for line in lines:
                    if re.match(r"^[A-Z][a-z]{2} \d{1,2}, \d{4}",line):
                        if current_transaction:
                            transactions.append(" ".join(current_transaction))
                        current_transaction=[line]
                    elif current_transaction:
                        current_transaction.append(line)
        if current_transaction:
            transactions.append(" ".join(current_transaction))

        for transaction in transactions:
            debt_pattern=re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4}) (Paid to .*) (Debit) INR .*?(\d+\.\d{2})",transaction)
            if debt_pattern:
                debt_order=list(debt_pattern.groups())
                debits.append(debt_order)
            cred_pattern=re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4}) (Received ?.*) (Credit) INR .*?(\d+\.\d{2})",transaction)
            if cred_pattern:
                cred_order=list(cred_pattern.groups())
                credits.append(cred_order)
    for filename,data in [("debits.csv",debits),("credits.csv",credits)]:
        with open(filename,"w",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(["Date","Transaction Details","Type","Amount"])
            writer.writerows(data)
    return "debits.csv","credits.csv"
                

