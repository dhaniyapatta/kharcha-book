from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


class EmailParser:

    def email_to_dataframe(email_data):
        for email in email_data:
            soup = BeautifulSoup(email["body"], "html.parser")
            text = soup.get_text()
            pattern1 = r'Dear.*?reference number is \d+'
            pattern2= r'Dear.*?account XX5090'
            
            matches = re.findall(pattern1, text, re.DOTALL)
            if len(matches)==0:   
                matches = re.findall(pattern2, text, re.DOTALL)
            email["body"]=''.join(matches)
            
            
            # Check for debit or credit
            if re.search(r'\bcredited\b', email["body"], re.IGNORECASE):
                email["credit_debit"] = 'Credit'
            elif re.search(r'\bdebited\b',  email["body"], re.IGNORECASE):
                email["credit_debit"] = 'Debit'
            
            # Check for payment method category
            if re.search(r'\bUPI transaction\b',  email["body"], re.IGNORECASE):
                email["txn method"] = 'UPI'
                if re.search(r'\bcredit card\b',  email["body"], re.IGNORECASE):
                    email["txn method"] = 'Credit Card UPI'

            elif re.search(r'\bcredit card\b',  email["body"], re.IGNORECASE):
                email["txn method"] = 'Credit Card'
            elif re.search(r'\bdebit card\b',  email["body"], re.IGNORECASE):
                email["txn method"] = 'Debit Card'

        
            # Extract amount
            amount_match = re.search(r'Rs\.(\d+(\.\d+)?)', email["body"]) 
            if amount_match:
                email["amount"] = float(amount_match.group(1))
            else:
                pattern = r'INR\s([\d,]+\.\d{2})'
                matches = re.findall(pattern, email["body"])
                # Process the matches to convert them to floats
                if matches:
                    amount_str = matches[0]
                    amount_float = float(amount_str.replace(',', ''))
                    email["amount"] = amount_float

            date_obj = datetime.strptime(email["date"], "%a, %d %b %Y %H:%M:%S %z")
            naive_date_obj = date_obj.replace(tzinfo=None)
            formatted_date = naive_date_obj.strftime("%Y-%m-%d %H:%M:%S")
            email["date"]=formatted_date

        df = pd.DataFrame(email_data)
        return df
        

  