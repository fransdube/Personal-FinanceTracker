import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from datetime import datetime

# Global variable to hold the Firestore client
db = None

def initialize_firestore(service_account_path='serviceAccountKey.json'):
    """
    Initializes the Firestore client.

    Args:
        service_account_path (str): Path to the service account JSON file.
    """
    global db

    # Check if already initialized
    if not firebase_admin._apps:
        if os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            print(f"Firestore initialized with {service_account_path}")
        else:
            # Fallback for testing or environment variable based setup
            # or if the user hasn't provided the key yet.
            print(f"Warning: {service_account_path} not found.")
            # In a real scenario, we might raise an error or try default credentials
            # firebase_admin.initialize_app()
            return None

    if db is None:
        try:
             db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firestore client: {e}")

def create_transaction(user_id, type, amount, category, date, description):
    """
    Creates a new transaction document in Firestore.

    Args:
        user_id (str): The ID of the user.
        type (str): 'income' or 'expense'.
        amount (float): The amount of the transaction.
        category (str): The category of the transaction.
        date (str or datetime): The date of the transaction.
        description (str): A brief description.

    Returns:
        str: The ID of the created document.
    """
    if db is None:
        raise ConnectionError("Firestore not initialized.")

    try:
        transaction_data = {
            'user_id': user_id,
            'type': type,
            'amount': float(amount),
            'category': category,
            'date': date,
            'description': description,
            'created_at': firestore.SERVER_TIMESTAMP
        }

        # Add a new document to the 'transactions' collection
        update_time, doc_ref = db.collection('transactions').add(transaction_data)

        # Update the document with its own ID (optional, but requested in prompt as 'id' field)
        # The prompt says "fields: id, ...". Firestore generates an ID.
        # Often it's cleaner to store the ID in the doc too.
        doc_ref.update({'id': doc_ref.id})

        print(f"Transaction created with ID: {doc_ref.id}")
        return doc_ref.id
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return None

def get_transactions(user_id):
    """
    Retrieves all transactions for a given user_id, sorted by date.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of dictionaries representing the transactions.
    """
    if db is None:
        raise ConnectionError("Firestore not initialized.")

    try:
        transactions_ref = db.collection('transactions')
        query = transactions_ref.where('user_id', '==', user_id).order_by('date', direction=firestore.Query.DESCENDING)
        results = query.stream()

        transactions = []
        for doc in results:
            transactions.append(doc.to_dict())

        return transactions
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return []

def update_transaction(transaction_id, updates):
    """
    Updates a transaction by ID.

    Args:
        transaction_id (str): The ID of the transaction document to update.
        updates (dict): A dictionary of fields to update.

    Returns:
        bool: True if successful, False otherwise.
    """
    if db is None:
        raise ConnectionError("Firestore not initialized.")

    try:
        doc_ref = db.collection('transactions').document(transaction_id)
        # Check if exists first? Or just update.
        # update() will fail if document doesn't exist? No, usually creates if not exists unless specified?
        # firestore update() fails if doc does not exist.
        doc_ref.update(updates)
        print(f"Transaction {transaction_id} updated.")
        return True
    except Exception as e:
        print(f"Error updating transaction: {e}")
        return False

def delete_transaction(transaction_id):
    """
    Deletes a transaction by ID.

    Args:
        transaction_id (str): The ID of the transaction document to delete.

    Returns:
        bool: True if successful, False otherwise.
    """
    if db is None:
        raise ConnectionError("Firestore not initialized.")

    try:
        db.collection('transactions').document(transaction_id).delete()
        print(f"Transaction {transaction_id} deleted.")
        return True
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False
