import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import database, auth, analytics

# --- Fixtures ---

@pytest.fixture
def mock_firestore():
    with patch('src.database.firestore') as mock:
        yield mock

@pytest.fixture
def mock_creds():
    with patch('src.database.credentials') as mock:
        yield mock

@pytest.fixture
def mock_admin():
    with patch('src.database.firebase_admin') as mock:
        # Ensure _apps is empty so initialization proceeds
        mock._apps = []
        yield mock

@pytest.fixture
def mock_db():
    with patch('src.database.db') as mock:
        yield mock

@pytest.fixture
def mock_auth_create_user():
    with patch('src.auth.auth.create_user') as mock:
        yield mock

@pytest.fixture
def mock_requests_post():
    with patch('src.auth.requests.post') as mock:
        yield mock

# --- Database Tests ---

def test_initialize_firestore(mock_admin, mock_creds, mock_firestore):
    # Mock file existence
    with patch('os.path.exists', return_value=True):
        database.initialize_firestore('dummy.json')
        mock_admin.initialize_app.assert_called()
        mock_firestore.client.assert_called()

def test_create_transaction(mock_db):
    mock_coll = mock_db.collection.return_value
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "test_doc_id"
    mock_coll.add.return_value = (None, mock_doc_ref)

    tid = database.create_transaction("user1", "expense", 100, "food", "2023-10-01", "lunch")

    assert tid == "test_doc_id"
    mock_coll.add.assert_called_once()
    args, _ = mock_coll.add.call_args
    assert args[0]['amount'] == 100.0
    assert args[0]['user_id'] == "user1"

def test_get_transactions(mock_db):
    mock_query = mock_db.collection.return_value.where.return_value.order_by.return_value

    mock_doc1 = MagicMock()
    mock_doc1.to_dict.return_value = {'amount': 100, 'type': 'expense'}
    mock_doc2 = MagicMock()
    mock_doc2.to_dict.return_value = {'amount': 200, 'type': 'income'}

    mock_query.stream.return_value = [mock_doc1, mock_doc2]

    txs = database.get_transactions("user1")
    assert len(txs) == 2
    assert txs[0]['amount'] == 100

# --- Auth Tests ---

def test_register_user(mock_auth_create_user):
    mock_user = MagicMock()
    mock_user.uid = "new_user_id"
    mock_auth_create_user.return_value = mock_user

    uid = auth.register_user("test@example.com", "password")
    assert uid == "new_user_id"

def test_login_user_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'idToken': 'fake_token',
        'localId': 'user_123',
        'email': 'test@example.com'
    }
    mock_requests_post.return_value = mock_response

    result = auth.login_user("test@example.com", "password")
    assert result['uid'] == 'user_123'
    assert result['idToken'] == 'fake_token'

def test_login_user_failure(mock_requests_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'error': {'message': 'INVALID_PASSWORD'}
    }
    mock_requests_post.return_value = mock_response

    result = auth.login_user("test@example.com", "wrongpass")
    assert result is None

# --- Analytics Tests ---

def test_generate_summary():
    transactions = [
        {'type': 'income', 'amount': 1000, 'category': 'salary'},
        {'type': 'expense', 'amount': 100, 'category': 'food'},
        {'type': 'expense', 'amount': 50, 'category': 'transport'},
        {'type': 'expense', 'amount': 50, 'category': 'food'},
    ]

    from io import StringIO
    with patch('sys.stdout', new=StringIO()):
        summary = analytics.generate_summary(transactions)

    assert summary['total_income'] == 1000
    assert summary['total_expense'] == 200
    assert summary['net_balance'] == 800
    assert summary['category_spending']['food'] == 150
    assert summary['category_spending']['transport'] == 50

def test_generate_summary_empty():
     from io import StringIO
     with patch('sys.stdout', new=StringIO()):
        summary = analytics.generate_summary([])

     assert summary['total_income'] == 0
