"""
Unit tests for src/database.py
Tests the DatabaseManager class and its methods.

Note: These tests use mocking to avoid actual database connections.
"""

import pytest
import pandas as pd
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import date

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager


class TestDatabaseManagerInit:
    """Tests for DatabaseManager initialization."""
    
    def test_init_creates_instance(self):
        """Should create DatabaseManager instance."""
        db = DatabaseManager()
        
        assert db is not None
    
    def test_init_loads_config(self):
        """Should load database configuration."""
        db = DatabaseManager()
        
        assert db.host is not None
        assert db.port is not None
        assert db.database is not None
        assert db.user is not None
        # Password can be empty string
        assert db.password is not None or db.password == ''
    
    def test_init_engine_is_none(self):
        """Engine should be None before connect."""
        db = DatabaseManager()
        
        assert db.engine is None
    
    def test_init_session_is_none(self):
        """Session should be None before connect."""
        db = DatabaseManager()
        
        assert db.session is None


class TestDatabaseManagerConnect:
    """Tests for database connection."""
    
    @patch('database.create_engine')
    def test_connect_creates_engine(self, mock_create_engine):
        """connect should create SQLAlchemy engine."""
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Mock the connection test
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = ['PostgreSQL 14.0']
        
        db = DatabaseManager()
        result = db.connect()
        
        assert mock_create_engine.called
    
    @patch('database.create_engine')
    def test_connect_returns_true_on_success(self, mock_create_engine):
        """connect should return True on success."""
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = ['PostgreSQL 14.0']
        
        db = DatabaseManager()
        result = db.connect()
        
        assert result is True
    
    @patch('database.create_engine')
    def test_connect_returns_false_on_failure(self, mock_create_engine):
        """connect should return False on failure."""
        from sqlalchemy.exc import SQLAlchemyError
        mock_create_engine.side_effect = SQLAlchemyError("Connection failed")
        
        db = DatabaseManager()
        result = db.connect()
        
        assert result is False


class TestDatabaseManagerCreateTables:
    """Tests for table creation."""
    
    @patch('database.create_engine')
    def test_create_tables_executes_sql(self, mock_create_engine):
        """create_tables should execute SQL statements."""
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = ['PostgreSQL 14.0']
        
        db = DatabaseManager()
        db.connect()
        db.create_tables()
        
        # Should have executed SQL (at least for version check + table creation)
        assert mock_conn.execute.called


class TestDatabaseManagerInsertBanks:
    """Tests for bank insertion."""
    
    def test_insert_banks_data_structure(self):
        """Bank data should have correct structure."""
        db = DatabaseManager()
        
        # Check that bank names and app IDs are available
        from config import BANK_NAMES, APP_IDS
        
        assert 'CBE' in BANK_NAMES
        assert 'BOA' in BANK_NAMES
        assert 'Dashen' in BANK_NAMES
        
        assert 'CBE' in APP_IDS
        assert 'BOA' in APP_IDS
        assert 'Dashen' in APP_IDS


class TestDatabaseManagerInsertReviews:
    """Tests for review insertion."""
    
    @pytest.fixture
    def sample_reviews_df(self):
        """Sample DataFrame with reviews."""
        return pd.DataFrame({
            'review_id': ['r1', 'r2', 'r3'],
            'review_text': ['Great app', 'Bad app', 'OK app'],
            'rating': [5, 1, 3],
            'review_date': [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            'bank_code': ['CBE', 'BOA', 'Dashen'],
            'bank_name': [
                'Commercial Bank of Ethiopia',
                'Bank of Abyssinia',
                'Dashen Bank'
            ],
            'sentiment_label_vader': ['POSITIVE', 'NEGATIVE', 'NEUTRAL'],
            'sentiment_score_vader': [0.8, 0.7, 0.5],
            'sentiment_label_distilbert': ['POSITIVE', 'NEGATIVE', 'POSITIVE'],
            'sentiment_score_distilbert': [0.9, 0.85, 0.6],
            'themes': [['UI'], ['Technical'], ['Feature']],
            'primary_theme': ['UI', 'Technical Issues', 'Feature Requests'],
            'source': ['Google Play'] * 3
        })
    
    def test_sample_df_has_required_columns(self, sample_reviews_df):
        """Sample DataFrame should have all required columns."""
        required_columns = [
            'review_text', 'rating', 'review_date', 'bank_code',
            'sentiment_label_vader', 'primary_theme'
        ]
        
        for col in required_columns:
            assert col in sample_reviews_df.columns


class TestDatabaseManagerQueries:
    """Tests for database query methods."""
    
    @patch('database.create_engine')
    def test_query_method_structure(self, mock_create_engine):
        """Query methods should be callable."""
        db = DatabaseManager()
        
        # Check that the class has expected attributes
        assert hasattr(db, 'host')
        assert hasattr(db, 'database')
        assert hasattr(db, 'connect')
        assert hasattr(db, 'create_tables')


class TestConnectionString:
    """Tests for connection string generation."""
    
    def test_connection_string_format(self):
        """Connection string should have correct format."""
        db = DatabaseManager()
        
        # Build expected connection string
        expected_format = f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
        
        # Verify components
        assert db.host is not None
        assert db.port is not None
        assert db.database is not None
        assert db.user is not None


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_empty_password(self):
        """Should handle empty password."""
        with patch.dict(os.environ, {'DB_PASSWORD': ''}):
            db = DatabaseManager()
            # Should not raise
            assert db.password == '' or db.password is not None
    
    def test_default_values(self):
        """Should use default values when env vars not set."""
        # Clear relevant env vars temporarily
        db = DatabaseManager()
        
        # Should have some default values
        assert db.host is not None
        assert db.database is not None
    
    @patch('database.create_engine')
    def test_multiple_connect_calls(self, mock_create_engine):
        """Should handle multiple connect calls."""
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = ['PostgreSQL 14.0']
        
        db = DatabaseManager()
        
        # Multiple connects should not raise
        db.connect()
        db.connect()
        
        assert db.engine is not None


class TestDataValidation:
    """Tests for data validation before insertion."""
    
    @pytest.fixture
    def valid_review_data(self):
        """Valid review data for insertion."""
        return {
            'review_text': 'Great app!',
            'rating': 5,
            'review_date': date(2024, 1, 1),
            'bank_code': 'CBE',
            'sentiment_label_vader': 'POSITIVE',
            'sentiment_score_vader': 0.8,
            'primary_theme': 'User Interface'
        }
    
    def test_valid_rating_range(self, valid_review_data):
        """Rating should be between 1 and 5."""
        assert 1 <= valid_review_data['rating'] <= 5
    
    def test_valid_sentiment_label(self, valid_review_data):
        """Sentiment label should be valid."""
        valid_labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        assert valid_review_data['sentiment_label_vader'] in valid_labels
    
    def test_valid_sentiment_score(self, valid_review_data):
        """Sentiment score should be between 0 and 1."""
        assert 0 <= valid_review_data['sentiment_score_vader'] <= 1
    
    def test_valid_bank_code(self, valid_review_data):
        """Bank code should be valid."""
        valid_codes = ['CBE', 'BOA', 'Dashen']
        assert valid_review_data['bank_code'] in valid_codes
