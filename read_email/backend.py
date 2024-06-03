import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import pickle5 as pickle

df=pd.read_pickle("/Users/ankitjha/Downloads/expense-tracker/dataframe.pkl")


# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Define the date variable
start_date = '2024-05-24'
end_date='2024-05-26'

# Filter the DataFrame by the target date
df_filtered = df[(df['date'].dt.date >= pd.to_datetime(start_date).date()) & (df['date'].dt.date <= pd.to_datetime(end_date).date())]
df_filtered 
# Calculate total Debit and Credit amounts by transaction method
debit_summary = df_filtered[df_filtered['credit_debit'] == 'Debit'].groupby('txn method')['amount'].sum().reset_index()
credit_summary = df_filtered[df_filtered['credit_debit'] == 'Credit'].groupby('txn method')['amount'].sum().reset_index()

print("Debit Summary for range")
print(debit_summary)
print("\nCredit Summary for range")
print(credit_summary)


# # Bar chart for Debit Summary
# plt.figure(figsize=(10, 5))
# sns.barplot(x='txn method', y='amount', data=debit_summary, palette='viridis')
# plt.title('Debit Summary by Transaction Method')
# plt.xlabel('Transaction Method')
# plt.ylabel('Amount')
# plt.show()

# # Bar chart for Credit Summary
# plt.figure(figsize=(10, 5))
# sns.barplot(x='txn method', y='amount', data=credit_summary, palette='viridis')
# plt.title('Credit Summary by Transaction Method')
# plt.xlabel('Transaction Method')
# plt.ylabel('Amount')
# plt.show()