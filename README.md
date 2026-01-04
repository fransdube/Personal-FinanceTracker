# Personal Finance Tracker with Firebase

A CLI-based personal finance tracker built with Python and Google Firebase (Firestore & Authentication).

## Features
- User Registration & Login (Firebase Auth)
- Add, View, Edit, Delete Transactions (Firestore)
- Budget Summary (Total Income, Expenses, Balance, Category Breakdown)
- Secure Data Access (Firestore Security Rules)

## Prerequisites
- Python 3.7+
- A Google Firebase Project

## Setup Instructions

1. **Clone the repository** (if applicable) or download the source code.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Setup**:
   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Create a new project.
   - **Authentication**: Enable "Email/Password" provider in the Authentication section.
   - **Firestore**: Create a Firestore database in "Test Mode" (or use the provided rules).
   - **Service Account**:
     - Go to Project Settings > Service Accounts.
     - Generate a new private key.
     - Save the JSON file as `serviceAccountKey.json` in the project root directory.
   - **Web API Key**:
     - Go to Project Settings > General.
     - Copy the "Web API Key".
     - Set it as an environment variable: `export FIREBASE_WEB_API_KEY="your_api_key"` or edit `src/auth.py` (not recommended for production).

4. **Security Rules**:
   - Copy the contents of `firestore.rules` to your Firestore Rules tab in the console.

## How to Run

Run the main script:
```bash
python src/main.py
```

## Code Walkthrough

- `src/main.py`: The entry point. Handles the CLI menu loop and user input.
- `src/database.py`: Manages Firestore connection and CRUD operations.
- `src/auth.py`: Handles user registration (Admin SDK) and login (REST API).
- `src/analytics.py`: Uses Pandas to calculate financial summaries.

## Video Demonstration
[Link to Video Demo] (Placeholder)

## Future Improvements
- Add graphical charts for spending analysis.
- Export data to CSV.
- Add recurring transactions.
