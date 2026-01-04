"""
Project: Personal Finance Tracker
Author: Frans Dube
Date: 2023-10-27
Description: This module handles user authentication using Firebase Admin SDK
             for user creation and Firebase REST API for login.
"""

import firebase_admin
from firebase_admin import auth
import requests
import os
import json

# Retrieve API Key from environment variable or define it here
# Note: For security, API keys should be in environment variables.
# Since this is a sandbox and I cannot rely on user providing it immediately,
# I will use a placeholder or check env.
WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "AIzaSyC4q2bwsk7eCBmgZ_-1fuuN4b6V5A6iOUc")

def register_user(email, password):
    """
    Registers a new user using Firebase Admin SDK.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        str: The User ID (uid) of the created user, or None if failed.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Successfully created user: {user.uid}")
        return user.uid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def login_user(email, password):
    """
    Logs in a user using Firebase Auth REST API (Identity Toolkit).
    This is required because Admin SDK does not support client-side password login.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        dict: A dictionary containing 'idToken', 'localId' (uid), etc., or None if failed.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={WEB_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if "error" in data:
            print(f"Login failed: {data['error']['message']}")
            return None

        print("Login successful.")
        return {
            'idToken': data['idToken'],
            'uid': data['localId'],
            'email': data['email']
        }
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def verify_token(id_token):
    """
    Verifies the ID token using Admin SDK.

    Args:
        id_token (str): The ID token returned from login.

    Returns:
        dict: The decoded token claims, or None if invalid.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
