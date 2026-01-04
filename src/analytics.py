"""
Project: Personal Finance Tracker
Author: Frans Dube
Date: 2023-10-27
Description: This module provides analytics functions to calculate budget summaries
             and category spending breakdowns using Pandas.
"""

import pandas as pd

def generate_summary(transactions):
    """
    Calculates and prints a summary of the transactions.

    Args:
        transactions (list): A list of transaction dictionaries.

    Returns:
        dict: A dictionary containing summary statistics.
    """
    if not transactions:
        print("No transactions found to summarize.")
        return {
            'total_income': 0,
            'total_expense': 0,
            'net_balance': 0,
            'category_spending': {}
        }

    df = pd.DataFrame(transactions)

    # Ensure amount is numeric
    df['amount'] = pd.to_numeric(df['amount'])

    # Calculate Totals
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    net_balance = total_income - total_expense

    # Category Spending (Expenses only)
    expense_df = df[df['type'] == 'expense']
    if not expense_df.empty:
        category_spending = expense_df.groupby('category')['amount'].sum().to_dict()
    else:
        category_spending = {}

    print("\n--- Budget Summary ---")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Net Balance: ${net_balance:.2f}")
    print("\nSpending by Category:")
    for cat, amt in category_spending.items():
        print(f"  - {cat}: ${amt:.2f}")

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'category_spending': category_spending
    }
