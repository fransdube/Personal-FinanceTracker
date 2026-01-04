import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import database
from src import auth
from src import analytics

def main():
    print("Welcome to Personal Finance Tracker")

    # Initialize Database
    # NOTE: You must provide a valid serviceAccountKey.json file in the root directory.
    database.initialize_firestore()

    current_user = None

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user['email']}")
            print("1. Add a transaction")
            print("2. View all transactions")
            print("3. Edit a transaction")
            print("4. Delete a transaction")
            print("5. View summary")
            print("6. Logout")
            print("7. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                t_type = input("Type (income/expense): ").lower()
                amount = input("Amount: ")
                category = input("Category: ")
                date = input("Date (YYYY-MM-DD): ")
                description = input("Description: ")

                database.create_transaction(current_user['uid'], t_type, amount, category, date, description)

            elif choice == '2':
                transactions = database.get_transactions(current_user['uid'])
                print(f"\n--- Transactions ({len(transactions)}) ---")
                for t in transactions:
                    print(f"ID: {t.get('id')} | Date: {t.get('date')} | {t.get('type')} | ${t.get('amount')} | {t.get('category')} | {t.get('description')}")

            elif choice == '3':
                t_id = input("Enter Transaction ID to edit: ")
                field = input("Field to update (amount/category/date/description/type): ")
                value = input(f"New value for {field}: ")

                database.update_transaction(t_id, {field: value})

            elif choice == '4':
                t_id = input("Enter Transaction ID to delete: ")
                database.delete_transaction(t_id)

            elif choice == '5':
                transactions = database.get_transactions(current_user['uid'])
                analytics.generate_summary(transactions)

            elif choice == '6':
                current_user = None
                print("Logged out.")

            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid option.")

        else:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                email = input("Email: ")
                password = input("Password: ")
                user_data = auth.login_user(email, password)
                if user_data:
                    current_user = user_data

            elif choice == '2':
                email = input("Email: ")
                password = input("Password: ")
                uid = auth.register_user(email, password)
                if uid:
                    print("Registration successful. Please login.")

            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()
